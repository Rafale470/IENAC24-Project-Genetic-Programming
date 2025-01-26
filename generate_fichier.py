import os
import numpy as np
import random

# Crée le dossier pour stocker les fichiers si ce n'est pas déjà fait
output_dir = "simulation_configs"
os.makedirs(output_dir, exist_ok=True)

# Liste des opérateurs et fonctions disponibles
operators = ["+", "-", "*", "/"]
functions = ["np.sin", "np.cos"]

# Fonction pour générer une fonction cible aléatoire avec un sens mathématique
def generate_function():
    terms = []
    num_terms = random.randint(2, 5)  # Nombre de termes dans la fonction cible

    for _ in range(num_terms):
        choice = random.choice(["function", "constant", "variable"])
        if choice == "function":
            func = random.choice(functions)
            if random.choice([True, False]):
                terms.append(f"{func}(x)")
            else:
                terms.append(f"{func}({random.randint(1, 10)})")
        elif choice == "constant":
            terms.append(str(random.randint(1, 10)))
        elif choice == "variable":
            terms.append("x")

    # Mélanger les termes avec des opérateurs pour assurer la validité mathématique
    while len(terms) > 1:
        left = terms.pop(0)
        right = terms.pop(0)
        operator = random.choice(operators)
        if operator == "/" and right == "0":
            right = str(random.randint(1, 10))  # Éviter la division par zéro
        terms.insert(0, f"({left}{operator}{right})")  # Retirer les espaces

    return terms[0]

# Génération des fichiers de configuration
for i in range(100):
    function_cible = generate_function()
    config_content = f"""
fonction_cible = {function_cible}
intervalle_min = -5.0
intervalle_max = 5.0
nombre_points = 40
taille_population = 100
profondeur_max = 4
proba_crossover = 0.5
proba_mutation = 0.3
proba_mutation_point = 0.2
generations_max = 100
fitness_cible = 0.001
+ = True
- = True
* = True
/ = True
^ = False
cos = True
sin = True
exp = False
log = False
abs = False
""".strip()

    # Nom du fichier
    file_name = f"config_simulation_{i}.txt"
    file_path = os.path.join(output_dir, file_name)

    # Écriture du fichier
    with open(file_path, "w") as file:
        file.write(config_content)

print(f"100 fichiers de configuration ont été générés dans le dossier '{output_dir}'.")
