import numpy as np
import operator
from fonctions import *

class GlobalConstant :
    def __init__(self, content):
        self.c = content

MULTI_OPERATORS_INIT = GlobalConstant(None)
SGL_OPERATORS_INIT = GlobalConstant(None)
TERMINALS_INIT = GlobalConstant(None)

TERMINALS_LIST = GlobalConstant(None)
SGL_OPERATORS_LIST = GlobalConstant(None)
MULTI_OPERATORS_LIST = GlobalConstant(None)

TERMINALS_LIST = GlobalConstant(None)    

PROBA_MUTATION = GlobalConstant(None)
PROBA_MUTATION_POINT = GlobalConstant(None)
GENERATION_MAX = GlobalConstant(None)
FITNESS_CIBLE = GlobalConstant(None)
PROBA_CROSSOVER = GlobalConstant(None)
PROFONDEUR_MAX = GlobalConstant(None)
TAILLE_POPULATION = GlobalConstant(None)
NOMBRE_POINTS = GlobalConstant(None)
INTERVALLE_MAX = GlobalConstant(None)
INTERVALLE_MIN = GlobalConstant(None)
FONCTION_CIBLE = GlobalConstant(None)
TOURNAMENT_SIZE = GlobalConstant(None)
ELITISM = GlobalConstant(None)
RATIO_FULL_TREES = GlobalConstant(None)
SEED_RANGE = GlobalConstant(None)
PROBA_CROSSOVER_LEAVES = GlobalConstant(None)
DARWIN_FACTOR = GlobalConstant(None)
