import random
import operator
import sympy as sp

def div_with0(a,b):
    return operator.truediv(a, b) if b != 0 else 0

OPERATORS = {"+":(operator.add, 0.25), "-":(operator.sub, 0.25), "*":(operator.mul, 0.25), "/":(div_with0, 0.25)} #objectif : Dans le futur, récupérer ce dictionnaire via un fichier de configuration
OPERATORS_LIST = [item[0] for item in OPERATORS.values()]
OPERATORS_PROBA = [item[1] for item in OPERATORS.values()]
TERMINALS = {"x": (sp.Symbol("x"), 0.25), "cst":("cst", 0.25)}
TERMINALS_LIST = [item[0] for item in TERMINALS.values()]
TERMINALS_PROBA = [item[1] for item in TERMINALS.values()]
CST_RANGE = [-5, 5]

class Tree(object):
    def __init__ (self, name):
        self.name = name
        self.content = []
        self.depth = 0
        self.gen_seed = None
    
    def __repr__(self):
        def build_expression(index=0):
            if self.content[index] in OPERATORS_LIST:
                op = self.content[index]
                left = build_expression(index + 1)
                right = build_expression(index + 2)
                return f"({left} {self.get_operator_symbol(op)} {right})"
            elif isinstance(self.content[index], (int, float)):
                return str(self.content[index])
            elif isinstance(self.content[index], sp.Symbol):
                return str(self.content[index])
        return build_expression()
    
    def get_operator_symbol(self, operator_func):
        for op_symbol, (op_func, _) in OPERATORS.items():
            if op_func == operator_func:
                return op_symbol
        return "?"
    
    def generate_tree_full(self, depth, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, 9999)
        else :
            self.gen_seed = seed
        seed = self.gen_seed
        for i in range(2**(depth)-2**(depth-1)-1):
            random.seed(seed)
            self.content.append(random.choices(OPERATORS_LIST, weights=OPERATORS_PROBA, k=1)[0])
            seed = random.randint(0, 9999)
        for i in range(2**(depth-1)):
            random.seed(seed)
            elt = random.choices(TERMINALS_LIST, weights=TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(CST_RANGE[0, CST_RANGE[1]),1) if elt == "cst" else elt)
            seed = random.randint(0, 9999)
        self.depth = depth
    
    def generate_tree_growth(self, depth, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, 9999)
        else :
            self.gen_seed = seed
        seed = self.gen_seed  
        for i in range(2**(depth)-2**(depth-1)-1):
            random.seed(seed)
            elt = random.choices(OPERATORS_LIST+TERMINALS_LIST, weights=OPERATORS_PROBA+TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(CST_RANGE[0], CST_RANGE[1]),1) if elt == "cst" else elt)
            seed = random.randint(0, 9999)
        for i in range(2**(depth-1)):
            random.seed(seed)
            elt = random.choices(TERMINALS_LIST, weights=TERMINALS_PROBA, k=1)[0]
            self.content.append(round(random.uniform(CST_RANGE[0], CST_RANGE[1]),1) if elt == "cst" else elt)
            seed = random.randint(0, 9999)
        for i in range(2**(depth)-2**(depth-1)-1):
            if not self.content[i] in OPERATORS_LIST :
                self.content[(i+1)*2-1] = None
                self.content[(i+1)*2] = None
        self.depth = depth

class Pop(object):
    def __init__(self, name):
        self.name = name
        self.content = []
        self.gen = 0
        self.depth = 0
        self.gen_seed = None
    
    def generate(self, n, depth, ratio=0.5, seed=None):
        if seed == None :
            self.gen_seed=random.randint(0, 9999)
        else :
            self.gen_seed = seed
        seed = self.gen_seed
        for i in range(int(n*ratio)):
            random.seed(seed)
            tree = Tree(f"Tree number {i+1}")
            tree.generate_tree_full(depth, seed)
            self.content.append(tree)
            seed = random.randint(0, 9999)
        for i in range(int(n-n*ratio)):
            random.seed(seed)
            tree = Tree(f"Tree number {int(n*ratio)+i+1}")
            tree.generate_tree_growth(depth, seed)
            self.content.append(tree)
            seed = random.randint(0, 9999)
        self.depth = depth
        self.gen = 1


if __name__ == "__main__":
    seed = random.randint(0,9999)
    print(seed)
    test = Tree("test")
    test.generate_tree_full(3, seed)
    print(test)
    test2 = Tree("test2")
    test2.generate_tree_full(3, seed)
    print(test2)
    test3 = Tree("test3")
    test3.generate_tree_growth(3, seed)
    print(test3)
    test4 = Tree("test4")
    test4.generate_tree_growth(3, seed)
    print(test4)
    seed = random.randint(0,9999)
    print(seed)
    final_test = Pop("final_test")
    final_test.generate(10, 3, 0.5, seed)
    print(final_test.content)
