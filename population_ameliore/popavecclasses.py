import random
import operator
import numpy as np
from fonctions import fonction
from constantes import *

"""population.py

This module provides a framework for genetic programming, including tree-based representations 
and operations such as crossover, mutation, and evaluation of expressions. The key components 
are the `Tree` class, which models individual solutions as trees, and the `Pop` class, which 
manages populations of trees."""

def create_list(tree_obj, i):
    """Constructs a list of indices for a node and its children in a tree.
    Parameters:
        tree_obj (Tree): The tree object containing nodes.
        i (int): The index of the starting node.
        
    Returns:
        list: A sorted list of indices for the node and its children."""
    tree = list(range(2**tree_obj.depth-1))
    if i >= len(tree) or tree[i] is None:
        return []
    left_child_index = 2 * i + 1
    right_child_index = 2 * i + 2
    children = [i]
    if left_child_index < len(tree) and tree[left_child_index] is not None:
        children += create_list(tree_obj, left_child_index)
    if right_child_index < len(tree) and tree[right_child_index] is not None:
        children += create_list(tree_obj, right_child_index)
    return sorted(children)


class Tree(object):
    """Represents a tree structure used in genetic programming.
    Attributes:
        name (str): The name of the tree.
        content (list): The nodes of the tree.
        depth (int): The depth of the tree. A tree with one node has a depth of 1
        gen_seed (int): The seed value used for random number generation.
        gen (int): The generation of the tree."""
        
    def __init__ (self, name):
        """Initializes a new Tree instance.
        
        Parameters:
            name (str): The name of the tree."""
        self.name = name
        self.content = []
        self.depth = 0
        self.fitness = 0
        self.gen_seed = None
        self.gen = 0
    def fitness_calc(self, point_set):
        """Evaluates the fitness of the tree based on a set of points.
        
        Parameters:
            point_set (list): A list of dictionaries representing points.
            
        Returns:
            float: The average fitness of the tree across all points."""
        fitness = 0
        for point in point_set :
            fitness += abs(self.evaluate({"x":point[0]}) - point[1])**2
        self.fitness = fitness/len(point_set)
    def __repr__(self):
        """Generates a string representation of the tree as a mathematical expression.
        
        Returns:
            str: The mathematical expression represented by the tree."""
        def build_expression(i=0):
            if self.content[i].type == "multi":
                op = self.content[i].noun
                left = build_expression(i*2+1)
                right = build_expression(i*2+2)
                return f"({left} {self.content[i].symbol} {right})"
            elif self.content[i].type == "sgl":
                op = self.content[i].noun
                inside = build_expression(i*2+1)
                return f"({self.content[i].symbol}({inside})"
            elif (self.content[i].type == "cst"):
                return self.content[i].symbol
            elif self.content[i].type == "terminals":
                return self.content[i].symbol
        return build_expression()

    def evaluate(self, vector_dict):
        """Evaluate a tree for a vector given.
        
        Parameters:
            vector_dict (dict): The vector.
            
        Returns:
            float: The result."""
        def build_eval(i=0):
            if self.content[i].type == "multi":
                left = build_eval(i*2+1)
                right = build_eval(i*2+2)
                return self.content[i].noun(left, right)
            elif self.content[i].type == "sgl":
                inside = build_eval(i*2+1)
                return self.content[i].noun(inside)
            elif self.content[i].type == "cst":
                return self.content[i].noun
            elif self.content[i].type == "terminals":
                return vector_dict[self.content[i].symbol]
        return build_eval()
            
    
    def generate_empty(self, depth):
        """Generates an empty tree with a specified depth.
        
        Parameters:
            depth (int): The depth of the tree."""
        for i in range((2**depth)-1):
            self.content.append(None)
        self.depth = depth
    
    def generate_tree_full(self, depth, seed=None):
        """Generates a full tree with all nodes populated.
        
        Parameters:
            depth (int): The depth of the tree.
            seed (int, optional): The seed for random number generation. Defaults to None."""
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
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a), TERMINALS_PROBA[-1], "cst") if elt.noun == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth)-2**(depth-1)-1):
            
            if self.content[i] == None:
                self.content[i*2+1] = None
                self.content[i*2+2] = None
            else:
                if self.content[i].type == "sgl" :
                    self.content[i*2+2] = None
        self.depth = depth
        self.gen = 1
    
    def generate_tree_growth(self, depth, seed=None):
        """Generates a tree using the growth method, with variable structure.
        
        Parameters:
            depth (int): The depth of the tree.
            seed (int, optional): The seed for random number generation. Defaults to None."""
        if seed == None :
            self.gen_seed=random.randint(0, SEED_RANGE)
        else :
            self.gen_seed = seed
        seed = self.gen_seed
        for i in range(2**(depth)-2**(depth-1)-1):
            random.seed(seed)
            elt = random.choices(MULTI_OPERATORS_LIST+SGL_OPERATORS_LIST+TERMINALS_LIST, weights=MULTI_OPERATORS_PROBA+SGL_OPERATORS_PROBA+TERMINALS_PROBA, k=1)[0]
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a), TERMINALS_PROBA[-1], "cst") if elt.noun == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth-1)):
            random.seed(seed)
            elt = random.choices(TERMINALS_LIST, weights=TERMINALS_PROBA, k=1)[0]
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a), TERMINALS_PROBA[-1], "cst") if elt.noun == "cst" else elt)
            seed = random.randint(0, SEED_RANGE)
        for i in range(2**(depth)-2**(depth-1)-1):
            
            if  self.content[i] == None or self.content[i].type == "terminals" or self.content[i].type == "cst":
                self.content[i*2+1] = None
                self.content[i*2+2] = None
            else:

                if self.content[i].type == "sgl" :
                    self.content[i*2+2] = None
        self.depth = depth
        self.gen = 1
        
    
    def crossover_point(self, seed=None):
        """Selects a crossover point within the tree.
        
        Parameters:
            seed (int, optional): The seed for random number generation. Defaults to None.
            
        Returns:
            int: The index of the crossover point."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        l = []
        n=len(self.content)
        for i in range(1, n) :
            if self.content[i] is not None and (self.content[i].type == "sgl" or self.content[i].type == "multi"):
                l.append(i)
        if len(l) == 0 :
            return 0
        else :
            return(random.choice(l))
        
    def crossover_func(self, other, seed=None):
        """Performs crossover with another tree to produce an offspring tree.
        
        Parameters:
            other (Tree): The other tree to crossover with.
            seed (int, optional): The seed for random number generation. Defaults to None.
            
        Returns:
            Tree: The resulting offspring tree."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        depth = max(self.depth, other.depth)
        crossover_point_1_seed = random.randint(0, SEED_RANGE)
        random.seed(crossover_point_1_seed)
        crossover_point_2_seed = random.randint(0, SEED_RANGE)
        crossover_point_1 = self.crossover_point(crossover_point_1_seed)
        crossover_point_2 = other.crossover_point(crossover_point_2_seed)
        
        if crossover_point_1 == 0 and crossover_point_2 == 0:
            return self.crossover_leaves(other, seed)
        elif crossover_point_1 == 0 :
            return other.crossover_func(self, seed)
        else :
            offspring = Tree(f"Offspring")
            offspring.generate_empty(depth)
            offspring.gen = 1
            offspring.content[0] = self.content[crossover_point_1-1]
            ls_1 = create_list(offspring, 2)
            ls_2 = create_list(self, crossover_point_1+crossover_point_1%2)
            lo_1 = create_list(offspring, 1)
            lo_2 = create_list(other, crossover_point_2)
            offspring.content[0] = self.content[int((crossover_point_1-1)/2) if crossover_point_1%2 != 0 else int((crossover_point_1-2)/2)]
            index = 0
            for i in lo_1[:len(lo_2)] :
                offspring.content[i] = other.content[lo_2[index]]
                index += 1
            index = 0
            for i in ls_1[:len(ls_2)] :
                offspring.content[i] = self.content[ls_2[index]]
                index += 1
            return offspring
        
    def crossover_leaves(self, other, seed=None):
        """Performs crossover at the leaf nodes with another tree.
        
        Parameters:
            other (Tree): The other tree to crossover with.
            seed (int, optional): The seed for random number generation. Defaults to None.
            
        Returns:
            Tree: The resulting offspring tree."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        offspring = Tree(f"Offspring")
        offspring.content = self.content                
        offspring.depth = self.depth
        offspring.gen = 1
        l1 = []
        for i in range(2**offspring.depth-1):
            if offspring.content[i] is not None and (offspring.content[i].type == "terminals" or offspring.content[i].type == "cst") :
                l1.append(i)
        l2 = []
        for i in range(2**other.depth-1):
            if other.content[i] is not None and (other.content[i].type == "terminals" or other.content[i].type == "cst") :
                l2.append(i)
        leave_1 = int(random.choices(l1)[0])
        leave_2 = int(random.choices(l2)[0])
        offspring.content[leave_1] = other.content[leave_2]
        return offspring
    
    def mutation_point(self, seed=None):
        """Selects a mutation point within the tree.
        
        Parameters:
            seed (int, optional): The seed for random number generation. Defaults to None.
            
        Returns:
            int: The index of the mutation point."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        l = []
        for i in range(1, 2**self.depth-1): 
            if self.content[i] is not None and (self.content[i].type == "sgl" or self.content[i].type == "multi"):
                l.append(i)
        if len(l) == 0:
            return 0
        else :
            return random.choices(l)[0]
    
    def mutation(self, seed=None):
        """Applies mutation to a subtree within the tree.
        
        Parameters:
            seed (int, optional): The seed for random number generation. Defaults to None."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        mutation_point_seed = random.randint(0, SEED_RANGE)
        mutation_point_1 = self.mutation_point(mutation_point_seed)
        if mutation_point_1 == 0:
            return None
        else :
            sub_depth = 1
            while mutation_point_1 >= 2**sub_depth-1 :
                sub_depth += 1
            sub_depth = self.depth-sub_depth+1
            sub_tree = Tree(f"Sub_tree for {self.name} mutation")
            random.seed(mutation_point_seed)
            sub_seed = random.randint(0, SEED_RANGE)
            sub_tree.generate_tree_growth(sub_depth, sub_seed)
            l1 = create_list(self, mutation_point_1)
            l2 = create_list(sub_tree, 0)
            index = 0
            for i in l1 :
                self.content[i] = sub_tree.content[l2[index]]
                index += 1


class Pop(object):
    """Represents a population of trees for genetic programming.
    
    Attributes:
        name (str): The name of the population.
        content (list): The list of trees in the population.
        gen (int): The generation number.
        depth (int): The depth of the population's trees.
        gen_seed (int): The seed value used for random number generation."""
        
    def __init__(self, name):
        """Initializes a new Pop instance.
        
        Parameters:
            name (str): The name of the population."""
        self.name = name
        self.content = []
        self.gen = 0
        self.depth = 0
        self.gen_seed = None
    def evaluate(self, point_set):
        """Evaluates the fitness of each tree in the population.
        
        Parameters:
            point_set (list): A list of dictionaries representing points."""
        for tree in self.content :
            tree.fitness_calc(point_set)

    def tournament_selection(self, tournament_size, seed=None):
        """Selects the best tree from a random sample of trees.
        
        Parameters:
            tournament_size (int): The number of trees to sample.
            seed (int, optional): The seed for random number generation. Defaults to None.
            
        Returns:
            Tree: The best tree from the sample."""
        if seed == None :
            seed = random.randint(0, SEED_RANGE)
        random.seed(seed)
        l = []
        for i in range(tournament_size):
            l.append(random.choice(self.content))
        l.sort(key=lambda x: x.fitness, reverse=False)
        return l[0]
    def generate(self, n, depth, ratio=0.5, seed=None):
        """Generates a population of trees.
        
        Parameters:
            n (int): The number of trees in the population.
            depth (int): The depth of the trees.
            ratio (float): The ratio of full trees to growth trees. Defaults to 0.5.
            seed (int, optional): The seed for random number generation. Defaults to None."""
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
    print("---------------------------")
    seed = random.randint(0,SEED_RANGE)
    print(seed)
    test = Tree("test")
    test.generate_tree_full(5, seed)
    print(test)
    test2 = Tree("test3")
    test2.generate_tree_growth(5, seed)
    print(test2)
    print("---------------------------")
    seed = random.randint(0,SEED_RANGE)
    print(seed)
    final_test = Pop("final_test")
    final_test.generate(10, 5, 0.5, seed)
    print(final_test.content)
    print("---------------------------")
    test3 = test2.crossover_func(test)
    print(test3)
    test4 = test2.crossover_leaves(test)
    print(test4)
    print("---------------------------")
    print(test)
    seed = random.randint(0,SEED_RANGE)
    print(seed)
    test.mutation(seed)
    print(test)
    print("---------------------------")
    print(test.gen_seed, test)
    print(test.evaluate({"x":0, "y":2}))
    print(test.evaluate({"x":1, "y":2}))
    print("---------------------------")
    pop = Pop("test")
    pop.generate(1000, 5, 0.5, 8941)
    print(pop.gen_seed)
    def error(tree):
        n = len(tree.content)-2**(tree.depth-1)
        for i in range(n):
            if tree.content[i] == None and (tree.content[2*i+1] != None or tree.content[2*i+2] != None):
                return True
        return False
    for i in range(999):
        offspring = pop.content[i].crossover_func(pop.content[i+1])
        if error(offspring):
            print(True)
    for i in range(999):
        pop.content[i].mutation()
        if error(pop.content[i]):
            print(True, i)