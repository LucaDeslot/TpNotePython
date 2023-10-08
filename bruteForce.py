# This is a sample Python script.
import copy
import time

from utils import Memoization, Objet, Sac

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
