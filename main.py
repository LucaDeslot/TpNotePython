# This is a sample Python script.
import copy
import time


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

class Objet:
    def __init__(self, valeur, p1, p2, id):
        self.valeur = valeur
        self.p1 = p1
        self.p2 = p2
        self.id = id

class Sac:
    def __init__(self, p1Max, p2Max):

        self.p1Max = p1Max
        self.p2Max = p2Max
        self.p1 = 0
        self.p2 = 0
        self.objets = []  # This should be a list of Objet instances
        self.valeur = 0

def get_sac_from_file(path):
    try:
        with open(path, 'r') as file:
            nbObjets, p1Max, p2Max = map(int, file.readline().split())
            objets = []
            for i in range(nbObjets):
                valeur, p1, p2 = map(int, file.readline().split())
                objets.append(Objet(valeur, p1, p2, i))
            sac = Sac(p1Max, p2Max)
            return sac, objets
    except FileNotFoundError:
        print(f"Failed to open file: {path}")
        exit(1)

def print_sac(sac):
    print(f"P1: {sac.p1}\nP2: {sac.p2}\nValeur: {sac.valeur}")
    for i, objet in enumerate(sac.objets):
        print(f"Objet {i}: {objet.valeur} {objet.p1} {objet.p2}")

def max_sac(a, b):
    return a if a.valeur >= b.valeur else b

def is_feasible(sac, objet):
    return sac.p1 + objet.p1 <= sac.p1Max and sac.p2 + objet.p2 <= sac.p2Max

def put(sac, objet):
    if is_feasible(sac, objet):
        sac.p1 += objet.p1
        sac.p2 += objet.p2
        sac.objets.append(objet)  # Ajoute l'objet à la liste (agrandit dynamiquement la liste)
        sac.valeur += objet.valeur
        return sac
    else:
        return None


def compute(sac, objets, memo=None):
    if memo is None:
        memo = {}

    key = tuple(sorted(objet.id for objet in sac.objets))

    if key in memo:
        return memo[key]

    if len(objets) == 0:
        return sac

    cp_objets = copy.deepcopy(objets)
    cp_objets.pop()
    dont_take = compute(sac, cp_objets, memo)

    takeSac = put(copy.deepcopy(sac), objets[-1])
    if takeSac:
        do_take = compute(takeSac, cp_objets, memo)
        result = max_sac(do_take, dont_take)
    else:
        result = max_sac(copy.deepcopy(sac), dont_take)

    memo[key] = result
    return result



if __name__ == "__main__":
    # Enregistrement du temps de début
    start_time = time.time()

    sac, objets = get_sac_from_file("objects/pb2.txt")
    sac_optimal = compute(sac, objets)
    print_sac(sac_optimal)

    # Enregistrement du temps de fin
    end_time = time.time()

    # Calcul et affichage de la durée d'exécution
    execution_time = end_time - start_time
    print(f"\nTemps d'exécution: {execution_time} secondes")