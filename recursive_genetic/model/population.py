import random
from model.arbre import Arbre
from fonction import Fonction
from model.terminal import Terminal
import matplotlib.pyplot as plt

class Population:
    """Classe pour gérer une population d'arbres."""

    def __init__(self, taille, profondeur_max, term_set, func_set, fonction_cible, points,
                 taille_tournoi=3, proba_crossover=0.8, proba_mutation=0.1, proba_mutation_point=0.05):
        """
        Initialise la population d'arbres avec des probabilités pour les opérations génétiques.
        :param taille: Taille totale de la population.
        :param profondeur_max: Profondeur maximale des arbres.
        :param term_set: Ensemble des terminaux disponibles.
        :param func_set: Ensemble des fonctions disponibles.
        :param fonction_cible: Fonction cible à approximer.
        :param points: Points d'échantillonnage pour évaluer la fitness.
        :param taille_tournoi: Taille du tournoi pour la sélection.
        :param proba_crossover: Probabilité de réaliser un crossover (par défaut 0.8).
        :param proba_mutation: Probabilité de réaliser une mutation générale (par défaut 0.1).
        :param proba_mutation_point: Probabilité de réaliser une mutation ponctuelle (par défaut 0.05).
        """
        self.taille = taille
        self.profondeur_max = profondeur_max
        self.term_set = term_set
        self.func_set = func_set
        self.fonction_cible = fonction_cible
        self.points = points
        self.taille_tournoi = taille_tournoi
        self.proba_crossover = proba_crossover
        self.proba_mutation = proba_mutation
        self.proba_mutation_point = proba_mutation_point
        self.population = []

    def generer_population(self):
        """Génère une population avec 50 % d'arbres grow et 50 % full."""
        self.population = []
        for i in range(self.taille):
            arbre = Arbre(self.profondeur_max, self.term_set, self.func_set)
            if i < self.taille / 2:
                arbre.generer_grow()
            else:
                arbre.generer_full()
            self.population.append(arbre)

    def selection_tournoi(self):
        """Sélectionne un individu via un tournoi."""
        candidats = random.sample(self.population, self.taille_tournoi)
        return min(candidats, key=lambda arbre: arbre.fitness(self.fonction_cible, self.points))

    def meilleur_individu(self):
        """Trouve l'individu avec la meilleure fitness dans la population."""
        if not self.population:
            raise ValueError("La population est vide.")
        return min(self.population, key=lambda arbre: arbre.fitness(self.fonction_cible, self.points))

    def effectuer_crossover(self):
        """
        Effectue un crossover entre deux parents avec une probabilité donnée.
        """
        for _ in range(self.taille):
            if random.random() < self.proba_crossover:
                parent1 = self.selection_tournoi()
                parent2 = self.selection_tournoi()
                descendant = parent1.crossover(parent2)
                descendant.update_profondeur()
                # Remplacer le pire individu par le descendant
                pire_arbre = max(self.population, key=lambda arbre: arbre.fitness(self.fonction_cible, self.points))
                if descendant.fitness(self.fonction_cible, self.points) < pire_arbre.fitness(self.fonction_cible, self.points):
                    self.population.remove(pire_arbre)
                    self.population.append(descendant)
                    if random.random() < self.proba_mutation:
                        descendant.mutation()
                    if random.random() < self.proba_mutation_point:
                        descendant.point_mutation()

    def effectuer_mutation(self):
        """
        Applique une mutation générale sur un individu avec une probabilité donnée.
        """
        if random.random() < self.proba_mutation:
            individu = self.selection_tournoi()
            individu.mutation()

    def effectuer_mutation_point(self):
        """
        Applique une mutation ponctuelle sur un individu avec une probabilité donnée.
        """
        if random.random() < self.proba_mutation_point:
            individu = self.selection_tournoi()
            individu.point_mutation()

    def statistiques_fitness(self):
        """
        Calcule et affiche les statistiques de fitness de la population.
        :return: Dictionnaire contenant les statistiques de fitness.
        """
        if not self.population:
            raise ValueError("La population est vide.")

        fitness_values = [arbre.fitness(self.fonction_cible, self.points) for arbre in self.population]
        fitness_min = min(fitness_values)
        fitness_max = max(fitness_values)
        fitness_moyenne = sum(fitness_values) / len(fitness_values)

        stats = {
            "Fitness Moyenne": fitness_moyenne,
            "Fitness Minimale": fitness_min,
            "Fitness Maximale": fitness_max,
            "Distribution": fitness_values,
        }

        # Afficher les statistiques
        print("=== Statistiques de Fitness ===")
        print(f"Fitness Moyenne   : {fitness_moyenne} , prof = {self.meilleur_individu().profondeur(self.meilleur_individu().racine)}")
        print(f"Fitness Minimale  : {fitness_min}")
        print(f"Fitness Maximale  : {fitness_max}")
        print("===============================")

        return stats

    def evoluer(self, generations_max=100, fitness_cible=1e-6, afficher_stats=True):
        """
        Lance le processus évolutif pour atteindre la fonction cible.
        :param generations_max: Nombre maximal de générations.
        :param fitness_cible: Fitness minimale à atteindre (critère d'arrêt).
        :param afficher_stats: Si True, affiche les statistiques à chaque génération.
        :return: Le meilleur individu trouvé.
        """
        min_fit = []
        mean_fit = []
        worst_fit = []
        generations = []
        for generation in range(generations_max):
            # Évaluer la population
            meilleur = self.meilleur_individu()
            meilleure_fitness = meilleur.fitness(self.fonction_cible, self.points)

            # Afficher les statistiques de la génération
            if afficher_stats:
                print(f"Génération {generation + 1} :")
                print(f"  Meilleure fitness : {meilleure_fitness}")
                print(f"  Meilleur individu : {meilleur}")
                stat = self.statistiques_fitness()
                min_fit.append(stat["Fitness Minimale"])
                mean_fit.append(stat["Fitness Moyenne"])
                worst_fit.append(stat["Fitness Maximale"])
                generations.append(generation)

            # Critère d'arrêt
            if meilleure_fitness <= fitness_cible:
                plt.plot(generations, min_fit, label='Fitness Minimale', color='blue')
                plt.plot(generations, mean_fit, label='Fitness Moyenne', color='green')
                plt.plot(generations, worst_fit, label='Fitness Maximale', color='red')
                plt.legend()
                plt.xlabel('Génération')
                plt.ylabel('Fitness')
                plt.title('Évolution de la fitness')
                plt.show()
                print("Solution atteinte !")
                return meilleur

            # Appliquer les opérations génétiques
            self.effectuer_crossover()
            #self.effectuer_mutation()
            #self.effectuer_mutation_point()
        
        # Afficher l'évolution de la fitness sur un seul et même graphique
        plt.plot(generations, min_fit, label='Fitness Minimale', color='blue')
        plt.plot(generations, mean_fit, label='Fitness Moyenne', color='green')
        plt.plot(generations, worst_fit, label='Fitness Maximale', color='red')
        plt.legend()
        plt.xlabel('Génération')
        plt.ylabel('Fitness')
        plt.title('Évolution de la fitness')
        plt.show()

        # Si le critère d'arrêt n'est pas atteint
        print("Nombre maximal de générations atteint.")
        return self.meilleur_individu()
