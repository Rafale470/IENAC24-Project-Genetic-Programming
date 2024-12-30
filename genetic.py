#Algorithme évolutioniste (boucle principale) pour la population décrite dans populaiton.py
#Auteurs: Mathias ROBERT 

import numpy as np
from population import Pop

def genetic_algorithm(pop_size, nb_gen, mutation_rate, crossover_rate, tournament_size, elitism):
    #Initialisation de la population
    population = Pop("population")
    population.generate(pop_size, 5)
    
    #Boucle principale
    for i in range(nb_gen):
        #Evaluation de la population
        population.evaluate()
        
        #Sélection des parents
        parents = population.tournament_selection(tournament_size)
        
        #Croisement
        children = population.crossover(parents, crossover_rate)
        
        #Mutation
        population.mutate(children, mutation_rate)
        
        #Elitisme
        population.elitism(parents, children, elitism)
        
        #Mise à jour de la génération
        population.gen += 1
        
    #Evaluation de la population
    population.evaluate()
    
    #Retourne le meilleur individu
    return population.content[0]