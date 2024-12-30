import random
import operator
import sympy as sp
import numpy as np


def div_with0(a,b):
    return operator.truediv(a, b) if b!=0 else 0

def pow_with0(a,b):
    return operator.pow(a, b) if b >=0 or a!=0 else 0

MULTI_OPERATORS = {"+":(operator.add, 0.25), "-":(operator.sub, 0.25), "*":(operator.mul, 0.25), "/":(div_with0, 0.25), "**":(pow_with0, 0.25)} #objectif : Dans le futur, récupérer ce dictionnaire via un fichier de configuration
MULTI_OPERATORS_LIST = [item[0] for item in MULTI_OPERATORS.values()]
MULTI_OPERATORS_PROBA = [item[1] for item in MULTI_OPERATORS.values()]

SGL_OPERATORS = {"cos":(np.cos, 0.25), "sin":(np.sin, 0.25)}
SGL_OPERATORS_LIST = [item[0] for item in SGL_OPERATORS.values()]
SGL_OPERATORS_PROBA = [item[1] for item in SGL_OPERATORS.values()]

TERMINALS = {"x": (sp.Symbol("x"), 0.25), "cst":("cst", 0.25)}
TERMINALS_LIST = [item[0] for item in TERMINALS.values()]
TERMINALS_PROBA = [item[1] for item in TERMINALS.values()]

SEED_RANGE = 9999


class Tree(object):
    def __init__ (self, name):
        self.name = name
        self.content = []
        self.depth = 0
        self.gen_seed = None
        self.gen = 0
    
    def __repr__(self):
        def build_expression(i=0):
            if self.content[i] in MULTI_OPERATORS_LIST:
                op = self.content[i]
                left = build_expression((i+1)*2-1)
                right = build_expression((i+1)*2)
                return f"({left} {self.get_operator_symbol(op)} {right})"
            elif self.content[i] in SGL_OPERATORS_LIST:
                op = self.content[i]
                inside = build_expression((i+1)*2-1)
                return f"({self.get_operator_symbol(op)}({inside})"
            elif isinstance(self.content[i], (int, float)):
                return str(self.content[i])
            elif isinstance(self.content[i], sp.Symbol):
                return str(self.content[i])
        return build_expression()
    
    def get_operator_symbol(self, operator_func):
        for op_symbol, (op_func, _) in MULTI_OPERATORS.items():
            if op_func == operator_func:
                return op_symbol
        for op_symbol, (op_func, _) in SGL_OPERATORS.items():
            if op_func == operator_func:
                return op_symbol
        return "?"
    
    def generate_tree_full(self, depth, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, SEED_RANGE)
        else :
            self.gen_seed = seed
        seed = self.gen_seed
        for i in range(2**(depth)-2**(depth-1)-1):
            random.seed(seed)
            self.content.append(random.choices(MULTI_OPERATORS_LIST+SGL_OPERATORS_LIST, weights=MULTI_OPERATORS_PROBA+SGL_OPERATORS_PROBA, k=1)[0])
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth-1)):
            random.seed(seed)
            elt = random.choices(TERMINALS_LIST, weights=TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(-5,5),1) if elt == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth)-2**(depth-1)-1):
            if self.content[i] in SGL_OPERATORS_LIST :
                self.content[(i+1)*2] = None
        self.depth = depth
        self.gen = 1
    
    def generate_tree_growth(self, depth, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, SEED_RANGE)
        else :
            self.gen_seed = seed
        seed = self.gen_seed  
        for i in range(2**(depth)-2**(depth-1)-1):
            random.seed(seed)
            elt = random.choices(MULTI_OPERATORS_LIST+SGL_OPERATORS_LIST+TERMINALS_LIST, weights=MULTI_OPERATORS_PROBA+SGL_OPERATORS_PROBA+TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(-5,5),1) if elt == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth-1)):
            random.seed(seed)
            elt = random.choices(TERMINALS_LIST, weights=TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(-5,5),1) if elt == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth)-2**(depth-1)-1):
            if self.content[i] in SGL_OPERATORS_LIST :
                self.content[(i+1)*2] = None
            if self.content[i] in TERMINALS or self.content[i] is float :
                self.content[(i+1)*2-1] = None
                self.content[(i+1)*2] = None
        self.depth = depth
        self.gen = 1

    def crossover_point (self):
        l = []
        n=len(self.content)
        for i in range(1, n) :
            if self.content[i] in SGL_OPERATORS_LIST+MULTI_OPERATORS_LIST:
                l.append(i)
        return(random.choice(l))
        
    def crossover_func (self, other, seed=None):
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed = seed
        depth = max(self.depth, other.depth)
        crossover_point_1 = self.crossover_point()
        crossover_point_2 = other.crossover_point()
        offspring = Tree(f"Offspring of {self.name} and {other.name}")
        offspring.generate_empty(depth)
        offspring.gen = 1
        offspring.content[0] = self.content[crossover_point_1-1]
        def create_list (tree, indice):
            i = indice
            l = [i]
            while 2*i+1 < (2**tree.depth)-1 :
                l.append(i*2+1)
                l.Append(i*2+2)
                i += 1
            return l
        ls_1 = create_list(offspring, 2)
        ls_2 = create_list(self, crossover_point_1)
        lo_1 = create_list(offspring, 1)
        lo_2 = create_list(other, crossover_point_2)
        offspring.content[0] = self.content[crossover_point_1-1]
        index = 0
        for i in ls_1 :
            offspring.content[i] = self.content[ls_2[index]]
        index = 0
        for i in lo_1 :
            offspring.content[i] = other.content[lo_2[index]]
        return offspring
        
    def crossover_leaves (self, other):
        offspring = Tree(f"Offspring of {self.name} and {other.name}")
        offspring.content = self.content
        offspring.depth = self.depth
        offspring.gen = 1
        leave_1 = random.randint(1, 2**(offspring.depth-1))
        leave_2 = random.randint(1, 2**(other.depth-1))
        offspring.content[-leave_1] = other.content[-leave_2]
        return offspring

class Pop(object):
    def __init__(self, name):
        self.name = name
        self.content = []
        self.gen = 0
        self.depth = 0
        self.gen_seed = None
    
    def generate(self, n, depth, ratio=0.5, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, SEED_RANGE)
        else :
            self.gen_seed = seed
        seed = self.gen_seed
        for i in range(int(n*ratio)):
            random.seed(seed)
            tree = Tree(f"Tree number {i+1}")
            tree.generate_tree_full(depth, seed)
            self.content.append(tree)
            seed = random.randint(0, SEED_RANGE)
        for i in range(int(n-n*ratio)):
            random.seed(seed)
            tree = Tree(f"Tree number {int(n*ratio)+i+1}")
            tree.generate_tree_growth(depth, seed)
            self.content.append(tree)
            seed = random.randint(0, SEED_RANGE)
        self.depth = depth
        self.gen = 1


if __name__ == "__main__":
    seed = random.randint(0,SEED_RANGE)
    print(seed)
    test = Tree("test")
    test.generate_tree_full(3, seed)
    print(test)
    test2 = Tree("test3")
    test2.generate_tree_growth(3, seed)
    print(test2)
    seed = random.randint(0,SEED_RANGE)
    print(seed)
    final_test = Pop("final_test")
    final_test.generate(10, 3, 0.5, seed)
    print(final_test.content)
