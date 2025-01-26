import random
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
        depth (int): The depth of the tree. A tree with one node has a depth of 1"""
        
    def __init__ (self, name):
        """Initializes a new Tree instance.
        
        Parameters:
            name (str): The name of the tree."""
        self.name = name
        self.content = []
        self.depth = 0
        self.fitness = 0

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
    
    def copy(self, other):
        self.content = other.content 
        self.depth = other.depth 
        self.fitness = other.fitness
    
    def generate_empty(self, depth):
        """Generates an empty tree with a specified depth.
        
        Parameters:
            depth (int): The depth of the tree."""
        for i in range((2**depth)-1):
            self.content.append(None)
        self.depth = depth
    
    def generate_tree_full(self, depth):
        """Generates a full tree with all nodes populated.
        
        Parameters:
            depth (int): The depth of the tree."""
        for i in range(2**(depth)-2**(depth-1)-1):
            self.content.append(random.choices(MULTI_OPERATORS_LIST.c+SGL_OPERATORS_LIST.c, k=1)[0])
        for i in range(2**(depth-1)):
            elt = random.choices(TERMINALS_LIST.c, k=1)[0]
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a),  "cst") if elt.noun == "cst" else elt)
        for i in range(2**(depth)-2**(depth-1)-1):
            
            if self.content[i] == None:
                self.content[i*2+1] = None
                self.content[i*2+2] = None
            else:
                if self.content[i].type == "sgl" :
                    self.content[i*2+2] = None
        self.depth = depth
        self.gen = 1
    
    def generate_tree_growth(self, depth):
        """Generates a tree using the growth method, with variable structure.
        
        Parameters:
            depth (int): The depth of the tree."""
        for i in range(2**(depth)-2**(depth-1)-1):
            elt = random.choices(MULTI_OPERATORS_LIST.c+SGL_OPERATORS_LIST.c+TERMINALS_LIST.c,  k=1)[0]
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a),  "cst") if elt.noun == "cst" else elt)
        for i in range(2**(depth-1)):
            elt = random.choices(TERMINALS_LIST.c,  k=1)[0]
            a = round(random.uniform(-5,5),1)
            self.content.append(fonction(a, str(a), "cst") if elt.noun == "cst" else elt)
        for i in range(2**(depth)-2**(depth-1)-1):
            
            if  self.content[i] == None or self.content[i].type == "terminals" or self.content[i].type == "cst":
                self.content[i*2+1] = None
                self.content[i*2+2] = None
            else:

                if self.content[i].type == "sgl" :
                    self.content[i*2+2] = None
        self.depth = depth
        self.gen = 1
        
    
    def crossover_point(self):
        """Selects a crossover point within the tree.
            
        Returns:
            int: The index of the crossover point."""
        l = []
        n=len(self.content)
        for i in range(1, n) :
            if self.content[i] is not None and (self.content[i].type == "sgl" or self.content[i].type == "multi"):
                l.append(i)
        if len(l) == 0 :
            return 0
        else :
            return(random.choice(l))
        
    def crossover_func(self, other):
        """Performs crossover with another tree to produce an offspring tree.
        
        Parameters:
            other (Tree): The other tree to crossover with.
            
        Returns:
            Tree: The resulting offspring tree."""
        depth = max(self.depth, other.depth)
        crossover_point_1 = self.crossover_point()
        crossover_point_2 = other.crossover_point()
        
        if crossover_point_1 == 0 and crossover_point_2 == 0:
            return self.crossover_leaves(other)
        elif crossover_point_1 == 0 :
            return other.crossover_func(self)
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
        
    def crossover_leaves(self, other):
        """Performs crossover at the leaf nodes with another tree.
        
        Parameters:
            other (Tree): The other tree to crossover with.
            
        Returns:
            Tree: The resulting offspring tree."""
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
    
    def mutation_point(self):
        """Selects a mutation point within the tree.
        
        Returns:
            int: The index of the mutation point."""
        l = []
        for i in range(1, 2**self.depth-1): 
            if self.content[i] is not None and (self.content[i].type == "sgl" or self.content[i].type == "multi"):
                l.append(i)
        if len(l) == 0:
            return 0
        else :
            return random.choices(l)[0]
    
    def mutation(self):
        """Applies mutation to a subtree within the tree."""

        mutation_point_1 = self.mutation_point()
        if mutation_point_1 == 0:
            return None
        else :
            sub_depth = 1
            while mutation_point_1 >= 2**sub_depth-1 :
                sub_depth += 1
            sub_depth = self.depth-sub_depth+1
            sub_tree = Tree(f"Sub_tree for {self.name} mutation")
            sub_tree.generate_tree_growth(sub_depth)
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
        depth (int): The depth of the population's trees."""
        
    def __init__(self, name):
        """Initializes a new Pop instance.
        
        Parameters:
            name (str): The name of the population."""
        self.name = name
        self.content = []
        self.gen = 0
        self.depth = 0
    def evaluate(self, point_set):
        """Evaluates the fitness of each tree in the population.
        
        Parameters:
            point_set (list): A list of dictionaries representing points."""
        for tree in self.content :
            tree.fitness_calc(point_set)

    def tournament_selection(self, tournament_size):
        """Selects the best tree from a random sample of trees.
        
        Parameters:
            tournament_size (int): The number of trees to sample.
            
        Returns:
            Tree: The best tree from the sample."""
        l = []
        for i in range(tournament_size):
            l.append(random.choice(self.content))
        l.sort(key=lambda x: x.fitness, reverse=False)
        return l[0]
    def generate(self, n, depth, ratio=0.5):
        """Generates a population of trees.
        
        Parameters:
            n (int): The number of trees in the population.
            depth (int): The depth of the trees.
            ratio (float): The ratio of full trees to growth trees. Defaults to 0.5."""
        for i in range(int(n*ratio)):
            tree = Tree(f"Tree number {i+1}")
            tree.generate_tree_full(depth)
            self.content.append(tree)
        for i in range(int(n-n*ratio)):
            tree = Tree(f"Tree number {int(n*ratio)+i+1}")
            tree.generate_tree_growth(depth)
            self.content.append(tree)
        self.depth = depth
        self.gen = 1
