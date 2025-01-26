from constantes import *
import operator
import random
import numpy as np
from popavecclasses import Pop

def genetic_algorithm(pop_size, nb_gen, mutation_rate, crossover_rate, tournament_size, elitism, intervalle_min, intervalle_max, nombre_points, fonction_cible):
    #Initialisation de la population
    a = np.linspace(intervalle_min, intervalle_max, nombre_points)
    y = [(x, eval(fonction_cible)) for x in a]
    population = Pop("population")
    population.generate(pop_size, PROFONDEUR_MAX.c, RATIO_FULL_TREES.c)
    
    #Boucle principale
    for i in range(nb_gen):
        #Evaluation de la population
        population.evaluate(y)
        
        new_pop_content = []

        while len(new_pop_content) < pop_size - elitism:
            #Sélection des parents
            parent1 = population.tournament_selection(tournament_size)
            parent2 = population.tournament_selection(tournament_size)
            #Croisement
            children = parent1.crossover_func(parent2)
            if children == None:
                continue
            if random.random() < mutation_rate:
                children.mutation()
            #Ajout des enfants à la nouvelle population
            new_pop_content.append(children)
        #Elitisme
        new_pop_content += sorted(population.content, key=(lambda x :x.fitness))[:elitism]


        #Mise à jour de la population
        population.content = new_pop_content
        #Affichage de la meilleure fitness
        
        #Mise à jour de la génération
        population.gen += 1
        
    #Evaluation de la population
    population.evaluate(y)
    
    #Retourne le meilleur individu
    return sorted(population.content, key=(lambda x : x.fitness))[0]

