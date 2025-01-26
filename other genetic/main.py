import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow
from interface import Ui_MainWindow  # Généré à partir du fichier .ui
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
from genetic import genetic_algorithm, genetic_darwin
from fonctions import *
import operator
from fonctions_spec import *
from constantes import *

def main(config_file):
    """
    Fonction principale pour exécuter une simulation à partir d'un fichier de configuration.
    :param config_file: Chemin du fichier contenant les paramètres de la simulation.
    """

    MULTI_OPERATORS_INIT.c = {"+":(operator.add), "-":(operator.sub), "*":(operator.mul), "/":(div_with0), "^":(pow_with0), }
    SGL_OPERATORS_INIT.c = {"cos":(np.cos), "sin":(np.sin), "log" : (np.log), "exp" : (np.exp), "log": (np.log), "abs": (np.abs)}
    TERMINALS_INIT.c = {"x": ("x"), "cst":("cst")}

    TERMINALS_LIST.c = []
    SGL_OPERATORS_LIST.c = []
    MULTI_OPERATORS_LIST.c = []

    with open ("config_simulation.txt") as config:
        mylist = list(config)
        D = {}
        for i in range (0,12):
            L = mylist[i].split()
            D [L[0]] = L[2]
        
        for i in range (12,16):
            ligne = mylist[i].split()

            if ligne[2] == 'True':
                MULTI_OPERATORS_LIST.c.append(fonction(MULTI_OPERATORS_INIT.c[ligne[0]], ligne[0], "multi"))
        
        for j in range (17,21):
            ligne = mylist[j].split()

            if ligne[2]=='True':
                SGL_OPERATORS_LIST.c.append(fonction(SGL_OPERATORS_INIT.c[ligne[0]], ligne[0], "sgl"))


    TERMINALS_LIST.c = [fonction("x", "x" , "terminals"), fonction("cst","cst", "terminals")]    

    PROBA_MUTATION.c = float(D['proba_mutation'])
    PROBA_MUTATION_POINT.c = float(D['proba_mutation_point'])
    GENERATION_MAX.c = int(D['generations_max'])
    FITNESS_CIBLE.c = float(D['fitness_cible'])
    PROBA_CROSSOVER.c = float(D['proba_crossover'])
    PROFONDEUR_MAX.c = int(D['profondeur_max'])
    TAILLE_POPULATION.c = int(D['taille_population'])
    NOMBRE_POINTS.c = int(D['nombre_points'])
    INTERVALLE_MAX.c = float(D['intervalle_max'])
    INTERVALLE_MIN.c = float(D['intervalle_min'])
    FONCTION_CIBLE.c = D['fonction_cible']
    TOURNAMENT_SIZE.c = 10
    ELITISM.c = 50
    RATIO_FULL_TREES.c = 0.5
    SEED_RANGE.c = 9999
    PROBA_CROSSOVER_LEAVES.c = 0.10
    DARWIN_FACTOR.c = 0.5
    
    def fonction_cible(x):
        return eval(FONCTION_CIBLE.c)
    
    points = np.linspace(INTERVALLE_MIN.c, INTERVALLE_MAX.c, NOMBRE_POINTS.c)
    
    # Lancer l'évolution
    meilleur_arbre_elit = genetic_algorithm(TAILLE_POPULATION.c, GENERATION_MAX.c, PROBA_MUTATION.c, PROBA_CROSSOVER.c, TOURNAMENT_SIZE.c, ELITISM.c, INTERVALLE_MIN.c, INTERVALLE_MAX.c, NOMBRE_POINTS.c, FONCTION_CIBLE.c)
    meilleur_arbre_darwin = genetic_darwin(TAILLE_POPULATION.c, GENERATION_MAX.c, PROBA_MUTATION.c, PROBA_CROSSOVER.c, PROBA_CROSSOVER_LEAVES.c, INTERVALLE_MIN.c, INTERVALLE_MAX.c, NOMBRE_POINTS.c, FONCTION_CIBLE.c, DARWIN_FACTOR.c)

    # Afficher les résultats
    print("=== Résultat Final ===")
    print(f"Meilleur individu elitisme : {meilleur_arbre_elit}")
    print(f"Fitness : {meilleur_arbre_elit.fitness}")
    print(f"Meilleur individu darwin : {meilleur_arbre_darwin}")
    print(f"Fitness : {meilleur_arbre_darwin.fitness}")

    # Afficher le graphique
    afficher_graphique(meilleur_arbre_elit, meilleur_arbre_darwin, fonction_cible, INTERVALLE_MIN.c, INTERVALLE_MAX.c)


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

def afficher_graphique(meilleur_arbre_elit, meilleur_arbre_darwin, fonction_cible, intervalle_min, intervalle_max):
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
                y_vals.append(arbre.evaluate({"x": x}))
            except Exception:
                y_vals.append(float("inf"))  # En cas d'erreur (ex. division par zéro)
        return np.array(y_vals)

    y_trouvee_elit = evaluer_fonction_trouvee(meilleur_arbre_elit, x_vals)
    y_trouvee_darwin = evaluer_fonction_trouvee(meilleur_arbre_darwin, x_vals)

    # Tracer les graphiques
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_cible, label="Fonction cible", color="blue", linewidth=2)
    plt.plot(x_vals, y_trouvee_elit, label="Fonction trouvée elitisme", color="red", linestyle="--", linewidth=2)
    plt.plot(x_vals, y_trouvee_darwin, label="Fonction trouvée darwin", color="red", linestyle="--", linewidth=2)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("f(x)", fontsize=14)
    plt.title("Comparaison entre la fonction cible et la fonction trouvée", fontsize=16)
    plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
    plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.show()

if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #main_window = MainApp()
    #main_window.show()
    #sys.exit(app.exec_())
    main("config_simulation.txt")

