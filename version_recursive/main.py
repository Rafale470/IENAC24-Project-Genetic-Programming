import cProfile
import random
from terminaux import Terminal
from arbre import Arbre
from population import Population
from fonctions_base import FONCTIONS_BASE  # Import des fonctions de base
import numpy as np
import matplotlib.pyplot as plt

# Sélection des fonctions à utiliser
func_set = [
    f for f in FONCTIONS_BASE if f.nom in {"+", "-", "*", "/"}  # Inclut la fonction puissance
]

# Terminaux : uniquement "x" et quelques constantes
term_set = [Terminal("x")] + [Terminal(i) for i in range(-10, 10)]


# Fonction cible : f(x) = x^2 + x + 1
def fonction_cible(x):
    return x**2+x+1


# Points d'échantillonnage : dense autour de 0, répartis sur [-5, 5]
points = [{"x": random.uniform(-1, 1)} for _ in range(100)]

# Création de la population
population = Population(
    taille=4000,
    profondeur_max=2,  # Réduire la profondeur maximale pour limiter la complexité
    term_set=term_set,
    func_set=func_set,
    fonction_cible=fonction_cible,
    points=points,
    proba_crossover=0.5,
    proba_mutation=0,
    proba_mutation_point=0,
)

# Génération de la population initiale
population.generer_population()


def main():
    # Lancer l'évolution
    meilleur = population.evoluer(generations_max=100, fitness_cible=1e-3)

    # Résultats finaux
    print("=== Résultat Final ===")
    print(f"Meilleur individu : {meilleur}")
    print(f"Fitness : {meilleur.fitness(fonction_cible, points)}")

    return meilleur  # Retourne le meilleur arbre trouvé


# Appel de la fonction main et récupération du meilleur arbre
meilleur_arbre = main()

# Évaluer sur un intervalle [-5, 5]
x_vals = np.linspace(-5, 5, 500)  # 500 points entre -5 et 5

# Évaluer la fonction cible
y_cible = fonction_cible(x_vals)


# Évaluer la fonction trouvée
def evaluer_fonction_trouvee(arbre, x_vals):
    y_vals = []
    for x in x_vals:
        try:
            y_vals.append(arbre.evaluer({"x": x}))
        except Exception:
            y_vals.append(float("inf"))  # En cas d'erreur (ex. division par zéro)
    return np.array(y_vals)


# Évaluer la fonction trouvée par le meilleur arbre
y_trouvee = evaluer_fonction_trouvee(meilleur_arbre, x_vals)

# Tracer les graphiques
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_cible, label="Fonction cible $f(x) = x^2 + x + 1$", color="blue", linewidth=2)
plt.plot(x_vals, y_trouvee, label="Fonction trouvée par l'algorithme génétique", color="red", linestyle="--",
         linewidth=2)
plt.xlabel("x", fontsize=14)
plt.ylabel("f(x)", fontsize=14)
plt.title("Comparaison entre la fonction cible et la fonction trouvée", fontsize=16)
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.show()
