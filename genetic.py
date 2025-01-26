#Algorithme évolutioniste (boucle principale) pour la population décrite dans populaiton.py

import operator
import random
import numpy as np
from population import Pop
x = np.linspace(0, 40, 100)
y = [(i, i**2 + i*2) for i in x]
def genetic_algorithm(pop_size, nb_gen, mutation_rate, crossover_rate, tournament_size, elitism):
    #Initialisation de la population
    population = Pop("population")
    population.generate(pop_size, 5, 0.5)
    print(population.content)
    
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

#Test

best = genetic_algorithm(300, 25, 0.1, 1, 10, 50)
print(best)
print(best.fitness)