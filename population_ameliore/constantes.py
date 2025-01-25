import numpy as np
import operator
from fonctions import *
def div_with0(a,b):
    """Safely performs division, avoiding division by zero.
    
    Parameters:
        a (float): The numerator.
        b (float): The denominator.
        
    Returns:
        float: The result of the division, or 0 if the denominator is 0."""
    return operator.truediv(a, b) if b!=0 else 1

def pow_with0(a,b):
    """Safely performs the power operation, handling edge cases with zero and negatives.
    
    Parameters:
        a (float): The base.
        b (float): The exponent.
        
    Returns:
        float: The result of the power operation, or 0 for invalid cases."""
    """ Managing complex number too"""
    if a < 0 and not(float(b).is_integer()):
        return 0.0
    res = operator.pow(a, b) if not(isinstance(b, complex)) and (b >=0 or a!=0) else 0.0

    if (isinstance(res, complex)):
        print("Alerte !")
    
    return res

MULTI_OPERATORS_INIT = {"+":(operator.add), "-":(operator.sub), "*":(operator.mul), "/":(div_with0), "^":(pow_with0), }
SGL_OPERATORS_INIT = {"cos":(np.cos), "sin":(np.sin), "log" : (np.log), "exp" : (np.exp), "log": (np.log), "abs": (np.abs)}
TERMINALS_INIT = {"x": ("x"), "cst":("cst")}

TERMINALS_LIST = []
SGL_OPERATORS_LIST = []
MULTI_OPERATORS_LIST = []

with open ("config_simulation.txt") as config:
    mylist = list(config)
    D = {}
    for i in range (0,12):
        L = mylist[i].split()
        D [L[0]] = L[2]
    
    for i in range (12,17):
        ligne = mylist[i].split()

        if ligne[2] == 'True':
            PROBA = 1
        else:
            PROBA = 0
        MULTI_OPERATORS_LIST.append(fonction(MULTI_OPERATORS_INIT[ligne[0]], ligne[0], PROBA, "multi"))
    
    for j in range (17,22):
        ligne = mylist[j].split()

        if ligne[2]=='True':
            PROBA = 1
        else:
            PROBA = 0
        SGL_OPERATORS_LIST.append(fonction(SGL_OPERATORS_INIT[ligne[0]], ligne[0], PROBA, "sgl"))

TERMINALS_LIST = [fonction("x", "x" , 1,"terminals"), fonction("cst","cst", 1,"terminals")]    

MULTI_OPERATORS_PROBA = [func.weight for func in MULTI_OPERATORS_LIST]
SGL_OPERATORS_PROBA = [func.weight for func in SGL_OPERATORS_LIST]
TERMINALS_PROBA = [func.weight for func in TERMINALS_LIST]

PROBA_MUTATION = float(D['proba_mutation'])
PROBA_MUTATION_POINT = float(D['proba_mutation_point'])
GENERATION_MAX = int(D['generations_max'])
FITNESS_CIBLE = float(D['fitness_cible'])
PROBA_CROSSOVER = float(D['proba_crossover'])
PROFONDEUR_MUTATION_MAX = int(D['profondeur_mutation_max'])
PROFONDEUR_MAX = int(D['profondeur_max'])
TAILLE_POPULATION = int(D['taille_population'])
NOMBRE_POINTS = int(D['nombre_points'])
INTERVALLE_MAX = float(D['intervalle_max'])
INTERVALLE_MIN = float(D['intervalle_min'])
FONCTION_CIBLE = D['fonction_cible']
TOURNAMENT_SIZE = 10
ELITISM = 50
RATIO_FULL_TREES = 0.5
SEED_RANGE = 9999