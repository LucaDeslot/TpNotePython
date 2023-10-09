class Memoization:
    def __init__(self):
        self.cache = {}

    def lookup(self, key):
        return self.cache.get(key, None)

    def insert(self, key, value):
        self.cache[key] = value


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


def rearrange(best_solution, nb_objets):
    reslut = ""
    for i in range(nb_objets):
        if i in best_solution:
            reslut += "1"
        else:
            reslut += "0"

    return reslut
