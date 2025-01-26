import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow
from interface import Ui_MainWindow  # Généré à partir du fichier .ui
from model.population import Population
from model.terminal import Terminal
from fonctions_base import FONCTIONS_BASE
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt


def main(config_file):
    """
    Fonction principale pour exécuter une simulation à partir d'un fichier de configuration.
    :param config_file: Chemin du fichier contenant les paramètres de la simulation.
    """
    # Lire les paramètres depuis le fichier
    try:
        with open(config_file, "r") as f:
            params = {}
            for line in f:
                key, value = line.strip().split(" = ")
                params[key] = value
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        return

    # Convertir les paramètres dans les bons types
    try:
        fonction_cible_str = params["fonction_cible"]
        intervalle_min = float(params["intervalle_min"])
        intervalle_max = float(params["intervalle_max"])
        nombre_points = int(params["nombre_points"])
        taille_population = int(params["taille_population"])
        profondeur_max = int(params["profondeur_max"])
        proba_crossover = float(params["proba_crossover"])
        proba_mutation = float(params["proba_mutation"])
        proba_mutation_point = float(params["proba_mutation_point"])
        generations_max = int(params["generations_max"])
        fitness_cible = float(params["fitness_cible"])
        fonctions = [key for key, val in params.items() if val == "True"]
    except KeyError as e:
        print(f"Paramètre manquant dans le fichier de configuration : {e}")
        return
    except ValueError as e:
        print(f"Erreur de conversion de paramètre : {e}")
        return

    # Définir la fonction cible
    def fonction_cible(x):
        return eval(fonction_cible_str)

    # Créer les points d'échantillonnage
    points = [{"x": x} for x in np.linspace(intervalle_min, intervalle_max, nombre_points)]

    # Configurer les terminaux et les fonctions
    term_set = [Terminal("x")] + [Terminal(i) for i in range(-2, 2)]
    func_set = [f for f in FONCTIONS_BASE if f.nom in fonctions]

    # Créer et générer la population
    population = Population(
        taille=taille_population,
        profondeur_max=profondeur_max,
        term_set=term_set,
        func_set=func_set,
        fonction_cible=fonction_cible,
        points=points,
        proba_crossover=proba_crossover,
        proba_mutation=proba_mutation,
        proba_mutation_point=proba_mutation_point,
    )
    population.generer_population()

    # Lancer l'évolution
    meilleur_arbre = population.evoluer(generations_max=generations_max, fitness_cible=fitness_cible)

    # Afficher les résultats
    print("=== Résultat Final ===")
    print(f"Meilleur individu : {meilleur_arbre}")
    print(f"Fitness : {meilleur_arbre.fitness(fonction_cible, points)}")

    # Afficher le graphique
    #afficher_graphique(meilleur_arbre, fonction_cible, intervalle_min, intervalle_max)


def sauvegarder_parametres(self, fichier="./genetique/config_simulation.txt", parametres=None):
    """
    Sauvegarde les paramètres de la simulation dans un fichier texte.
    :param fichier: Nom du fichier où écrire les paramètres (par défaut "config_simulation.txt").
    :param parametres: Liste des paramètres à écrire.
    """
    if parametres is None:
        return

    # Obtenir les fonctions sélectionnées
    fonctions_selectionnees = {
        "+": self.ui.checkBox_addition.isChecked(),
        "-": self.ui.checkBox_soustraction.isChecked(),
        "*": self.ui.checkBox_multiplication.isChecked(),
        "/": self.ui.checkBox_division.isChecked(),
        "^": self.ui.checkBox_puissance.isChecked(),
        "cos": self.ui.checkBox_cosinus.isChecked(),
        "sin": self.ui.checkBox_sinus.isChecked(),
        "exp": self.ui.checkBox_exponentielle.isChecked(),
        "log": self.ui.checkBox_logarithme.isChecked(),
        "abs": self.ui.checkBox_valeur_absolue.isChecked(),
    }

    try:
        with open(fichier, "w") as f:
            f.write("fonction_cible = " + str(parametres[0]) + "\n")
            f.write("intervalle_min = " + str(parametres[1]) + "\n")
            f.write("intervalle_max = " + str(parametres[2]) + "\n")
            f.write("nombre_points = " + str(parametres[3]) + "\n")
            f.write("taille_population = " + str(parametres[4]) + "\n")
            f.write("profondeur_max = " + str(parametres[5]) + "\n")
            f.write("proba_crossover = " + str(parametres[6]) + "\n")
            f.write("proba_mutation = " + str(parametres[7]) + "\n")
            f.write("proba_mutation_point = " + str(parametres[8]) + "\n")
            f.write("generations_max = " + str(parametres[9]) + "\n")
            f.write("fitness_cible = " + str(parametres[10]) + "\n")
            for nom, actif in fonctions_selectionnees.items():
                f.write(f"{nom} = {'True' if actif else 'False'}\n")
        print(f"Paramètres sauvegardés dans {fichier}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des paramètres : {e}")


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        # Connecter les boutons de l'interface
        self.ui.pushButton_lancer_simulation.clicked.connect(self.lancer_simulation)

    def lancer_simulation(self):
        try:
            # Récupérer les paramètres depuis l'interface
            fonction_cible_str = self.ui.lineEdit_fonction_cible.text()
            intervalle_min = float(self.ui.lineEdit_intervalle_min.text())
            intervalle_max = float(self.ui.lineEdit_intervalle_max.text())
            nombre_points = int(self.ui.lineEdit_nombre_points.text())
            taille_population = int(self.ui.lineEdit_taille_population.text())
            profondeur_max = int(self.ui.lineEdit_profondeur_max.text())
            proba_crossover = float(self.ui.lineEdit_proba_crossover.text())
            proba_mutation = float(self.ui.lineEdit_proba_mutation.text())
            proba_mutation_point = float(self.ui.lineEdit_proba_mutation_point.text())
            generations_max = int(self.ui.lineEdit_generations_max.text())
            fitness_cible = float(self.ui.lineEdit_fitness_cible.text())
        except ValueError:
            print("Veuillez entrer des valeurs valides.")
            return

        # Créer une liste contenant les paramètres
        parametres = [
            fonction_cible_str,
            intervalle_min,
            intervalle_max,
            nombre_points,
            taille_population,
            profondeur_max,
            proba_crossover,
            proba_mutation,
            proba_mutation_point,
            generations_max,
            fitness_cible,
        ]
        sauvegarder_parametres(self, fichier="config_simulation.txt", parametres=parametres)
        main("config_simulation.txt")

def afficher_graphique(meilleur_arbre, fonction_cible, intervalle_min, intervalle_max):
    """
    Affiche le graphique comparant la fonction cible et la fonction trouvée.
    :param meilleur_arbre: L'arbre trouvé par l'algorithme génétique.
    :param fonction_cible: La fonction cible à approximer.
    :param intervalle_min: Borne inférieure de l'intervalle d'échantillonnage.
    :param intervalle_max: Borne supérieure de l'intervalle d'échantillonnage.
    """

    # Générer les valeurs pour le graphique
    x_vals = np.linspace(intervalle_min, intervalle_max, 500)
    y_cible = [fonction_cible(x) for x in x_vals]

    def evaluer_fonction_trouvee(arbre, x_vals):
        y_vals = []
        for x in x_vals:
            try:
                y_vals.append(arbre.evaluer({"x": x}))
            except Exception:
                y_vals.append(float("inf"))  # En cas d'erreur (ex. division par zéro)
        return np.array(y_vals)

    y_trouvee = evaluer_fonction_trouvee(meilleur_arbre, x_vals)

    # Tracer les graphiques
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_cible, label="Fonction cible", color="blue", linewidth=2)
    plt.plot(x_vals, y_trouvee, label="Fonction trouvée", color="red", linestyle="--", linewidth=2)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("f(x)", fontsize=14)
    plt.title("Comparaison entre la fonction cible et la fonction trouvée", fontsize=16)
    plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
    plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
