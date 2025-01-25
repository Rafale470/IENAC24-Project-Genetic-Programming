import math
from fonction import Fonction

addition = Fonction("+", 2, lambda a, b: a + b)
soustraction = Fonction("-", 2, lambda a, b: a - b)
multiplication = Fonction("*", 2, lambda a, b: a * b)
division = Fonction("/", 2, lambda a, b: a / b if b != 0 else 1)
puissance = Fonction("^", 2, lambda a, b: a ** b if a >= 0 or (int(b) == b and b >= 0) else abs(a) ** b)
exponentielle = Fonction("exp", 1, math.exp)
cosinus = Fonction("cos", 1, math.cos)
sinus = Fonction("sin", 1, math.sin)
logarithme = Fonction("log", 1, lambda x: math.log(x) if x > 0 else 1)
valeur_absolue = Fonction("abs", 1, abs)


FONCTIONS_BASE = [
    addition,
    soustraction,
    multiplication,
    division,
    puissance,
    exponentielle,
    cosinus,
    sinus,
    logarithme,
    valeur_absolue,
]