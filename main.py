# This is a sample Python script.
import copy
import time


class Objet:
    def __init__(self, valeur, p1, p2, id):
        self.valeur = valeur
        self.p1 = p1
        self.p2 = p2
        self.id = id

    def __eq__(self, other):
        return (self.valeur, self.p1, self.p2, self.id) == (other.valeur, other.p1, other.p2, other.id)

    def __hash__(self):
        return hash((self.valeur, self.p1, self.p2, self.id))


class Sac:
    def __init__(self, p1Max, p2Max):
        self.p1Max = p1Max
        self.p2Max = p2Max
        self.p1 = 0
        self.p2 = 0
        self.objets = []  # This should be a list of Objet instances
        self.valeur = 0

    def add_object(self, objet):
        if (self.p1 + objet.p1 <= self.p1Max) and (self.p2 + objet.p2 <= self.p2Max):
            self.p1 += objet.p1
            self.p2 += objet.p2
            self.objets.append(objet)
            self.valeur += objet.valeur
            self.objets.sort(key=lambda x: x.id)
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.p1Max, self.p2Max, self.p1, self.p2, self.valeur, tuple(self.objets)))

    def print(self):
        print(f"P1: {self.p1}\nP2: {self.p2}\nValeur: {self.valeur}")
        for i, objet in enumerate(self.objets):
            print(f"Objet {i}: {objet.valeur} {objet.p1} {objet.p2}")


class Memoization:
    def __init__(self):
        self.cache = {}

    def lookup(self, key):
        return self.cache.get(key, None)

    def insert(self, key, value):
        self.cache[key] = value


memoization = Memoization()


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


def biggest_sac(a, b):
    return a if a.valeur >= b.valeur else b


def compute(sac, objets):
    if len(objets) == 0:
        return sac

    # Utilisation du cache
    key = (sac.__hash__(), tuple(o.id for o in objets))
    cached_result = memoization.lookup(key)
    if cached_result is not None:
        return cached_result

    dont_take = compute(copy.deepcopy(sac), objets[:-1])

    take_sac = copy.deepcopy(sac)
    res = take_sac.add_object(objets[-1])

    if res:
        do_take = compute(take_sac, objets[:-1])
        best_sac = biggest_sac(do_take, dont_take)
    else:
        best_sac = dont_take

    # Insertion du résultat dans le cache avant de retourner la valeur
    memoization.insert(key, best_sac)
    return best_sac


if __name__ == "__main__":
    # Enregistrement du temps de début
    start_time = time.time()

    sac, objets = get_sac_from_file("objects/pb2.txt")
    sac_optimal = compute(sac, objets)

    sac_optimal.print()

    # Enregistrement du temps de fin
    end_time = time.time()

    # Calcul et affichage de la durée d'exécution
    execution_time = end_time - start_time
    print(f"\nTemps d'exécution: {execution_time} secondes")
