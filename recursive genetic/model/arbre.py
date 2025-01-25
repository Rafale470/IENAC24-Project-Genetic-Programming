import random
from model.noeud import NoeudInterne, NoeudExterne
from model.terminal import Terminal

class Arbre:

    def __init__(self, profondeur_max, term_set, func_set):
        """
        profondeur_max: Profondeur maximale de l'arbre.
        term_set: Liste des terminaux disponibles.
        func_set: Liste des fonctions disponibles.
        """
        self.profondeur_max = profondeur_max
        self.term_set = term_set
        self.func_set = func_set
        self.racine = None
        self.fitness_score = None
    
    def profondeur(self, racine):
        if racine is None:
            return 0
        if isinstance(racine, NoeudExterne):
            return 1
        if isinstance(racine, NoeudInterne):
            return 1 + max(self.profondeur(enfant) for enfant in racine.enfants)
    def generer_grow(self):
        self.racine = self._generer_noeud(self.profondeur_max, method="grow")

    def generer_full(self):
        self.racine = self._generer_noeud(self.profondeur_max, method="full")

    def _generer_noeud(self, profondeur, method):
        # Si la profondeur maximale est atteinte, on ajoute un terminal
        if profondeur == 0:
            terminal = random.choice(self.term_set)
            if terminal.valeur == "cst":
                    return NoeudExterne(Terminal(int(random.uniform(-10, 10))), profondeur=profondeur)
            return NoeudExterne(terminal, profondeur)

        if method == "grow":
            # On décide aléatoirement de créer un terminal ou un nœud interne
            if random.random() < len(self.term_set) / (len(self.term_set) + len(self.func_set)):
                terminal = random.choice(self.term_set)
                
                if terminal.valeur == "cst":
                    return NoeudExterne(Terminal(int(random.uniform(-10, 10))), profondeur=profondeur)
                return NoeudExterne(terminal, profondeur=profondeur)

        # Méthode full (ou grow qui décide de générer un nœud interne)
        fonction = random.choice(self.func_set)
        enfants = [self._generer_noeud(profondeur - 1, method) for _ in range(fonction.argument)]
        return NoeudInterne(fonction, enfants)
    def update_profondeur(self):
        self.racine.update_profondeur(0)

    def evaluer(self, variables):
        """
        Évalue l'arbre pour un dictionnaire de variables.
        :param variables: Dictionnaire associant des variables à leurs valeurs.
        :return: Résultat de l'évaluation.
        """
        if not self.racine:
            raise ValueError("L'arbre n'a pas été généré.")
        return self.racine.evaluer(variables)

    def __repr__(self):
        """
        Représente l'arbre sous forme d'une expression mathématique lisible.
        :return: Chaîne représentant l'expression.
        """
        if not self.racine:
            return "Arbre vide"
        return repr(self.racine)

    def fitness(self, fonction_cible, points):
        """
        Calcule l'erreur quadratique moyenne (fitness) entre l'arbre et une fonction cible.
        :param fonction_cible: Fonction cible (callable Python) à approximer.
        :param points: Liste de dictionnaires représentant les points d'échantillonnage
                       (par exemple [{"x": 1, "y": 2}, {"x": 3, "y": 4}]).
        :return: Erreur quadratique moyenne entre l'arbre et la fonction cible.
        """

        if not self.racine:
            raise ValueError("L'arbre n'a pas été généré.")

        if not (self.fitness_score is None):
            return self.fitness_score

        erreurs = []

        for point in points:
            try:
                # Évaluer l'arbre
                valeur_arbre = self.evaluer(point)
                # Évaluer la fonction cible
                valeur_cible = fonction_cible(**point)
                # Calculer la différence au carré
                erreur = (valeur_arbre - valeur_cible) ** 2
                erreurs.append(erreur)
            except Exception as e:
                # Si une évaluation échoue (ex. division par zéro), ajouter une pénalité élevée
                erreurs.append(float("inf"))

        # Retourner la moyenne des erreurs quadratiques
        self.fitness_score = sum(erreurs) / len(erreurs)
        return self.fitness_score

    def crossover(self, autre_arbre):
        """
        Réalise un crossover entre cet arbre et un autre arbre.
        :param autre_arbre: L'autre arbre avec lequel croiser cet arbre.
        :return: Un nouvel arbre (descendant).
        """
        # Copier les deux arbres pour préserver les originaux
        arbre1 = self._copier_arbre(self.racine)
        arbre2 = self._copier_arbre(autre_arbre.racine)

        # Sélectionner un sous-arbre aléatoire dans chaque arbre
        noeud1, parent1 = self._selectionner_noeud_aleatoire(arbre1)
        noeud2, _ = self._selectionner_noeud_aleatoire(arbre2, prof_min=noeud1.profondeur, interne=isinstance(noeud1, NoeudInterne))

        # Remplacer le sous-arbre sélectionné dans arbre1 par celui de arbre2
        if parent1 is None:
            # Si le parent est None, on remplace la racine
            descendant = noeud2
        else:
            index = parent1.enfants.index(noeud1)
            parent1.enfants[index] = noeud2
            descendant = arbre1

        # Créer un nouvel arbre pour le descendant
        nouvel_arbre = Arbre(self.profondeur_max, self.term_set, self.func_set)
        nouvel_arbre.racine = descendant
        return nouvel_arbre

    def mutation(self):
        """
        Applique une mutation à cet arbre en modifiant un sous-arbre ou un terminal.
        """
        if not self.racine:
            raise ValueError("L'arbre doit être généré avant d'appliquer une mutation.")

        # Sélectionner un nœud aléatoire
        noeud, parent = self._selectionner_noeud_aleatoire(self.racine)

        # Appliquer une mutation
        if isinstance(noeud, NoeudExterne):
            # Remplacer un terminal par un autre
            nouveau_terminal = random.choice(self.term_set)
            if nouveau_terminal.valeur == "cst":
                    nouveau_noeud = NoeudExterne(Terminal(random.uniform(-10, 10)))
            else: nouveau_noeud = NoeudExterne(nouveau_terminal)
        elif isinstance(noeud, NoeudInterne):
            # Remplacer un sous-arbre par un nouvel arbre généré
            nouveau_noeud = self._generer_noeud(self.profondeur_max-noeud.profondeur, method="grow")
        else:
            raise ValueError("Type de nœud inconnu pour mutation.")

        # Si le nœud est la racine
        if parent is None:
            self.racine = nouveau_noeud
        else:
            # Remplacer le nœud dans son parent
            index = parent.enfants.index(noeud)
            parent.enfants[index] = nouveau_noeud
        self.racine.update_profondeur(0)

    def _copier_arbre(self, noeud):
        """
        Copie récursivement un arbre à partir de son nœud racine.
        :param noeud: Nœud racine de l'arbre à copier.
        :return: Copie indépendante de l'arbre.
        """
        if isinstance(noeud, NoeudExterne):
            return NoeudExterne(noeud.terminal)
        elif isinstance(noeud, NoeudInterne):
            enfants_copies = [self._copier_arbre(enfant) for enfant in noeud.enfants]
            return NoeudInterne(noeud.fonction, enfants_copies)
        else:
            raise ValueError("Type de nœud inconnu lors de la copie.")

    def _selectionner_noeud_aleatoire(self, noeud, parent=None, prof_min=float("inf"), interne=None):
        """
        Sélectionne un nœud aléatoire dans un arbre avec une probabilité
        de 90 % pour choisir un nœud interne.
        :param noeud: Le nœud actuel.
        :param parent: Le parent du nœud actuel.
        :return: Tuple (nœud sélectionné, parent).
        """
        # Si le nœud est une feuille, on le retourne directement
        if isinstance(noeud, NoeudExterne):
            return noeud, parent

        # Construire une liste de tous les nœuds internes et externes
        noeuds_internes = [(noeud, parent)] if isinstance(noeud, NoeudInterne) else []
        noeuds_externes = []

        for enfant in noeud.enfants:
            if enfant.profondeur < prof_min:
                continue
            elif isinstance(enfant, NoeudInterne):
                noeuds_internes.append((enfant, noeud))
            elif isinstance(enfant, NoeudExterne):
                noeuds_externes.append((enfant, noeud))
            else:
                raise ValueError("Type de nœud inconnu lors de la sélection.")

        # Sélectionner un nœud avec 90% de chances pour un nœud interne
        if noeuds_internes and (not noeuds_externes or (interne==True or random.random() < 0.9)):
            return random.choice(noeuds_internes)

        # Sinon, retourner un nœud externe
        return random.choice(noeuds_externes)

    def point_mutation(self):
        """
        Applique une mutation ponctuelle (point mutation) sur cet arbre.
        Si un nœud interne est sélectionné, sa fonction est remplacée par une autre
        fonction avec le même nombre d'arguments.
        Si un nœud externe est sélectionné, son terminal est remplacé par un autre terminal.
        """
        if not self.racine:
            raise ValueError("L'arbre doit être généré avant d'appliquer une mutation.")

        # Sélectionner un nœud aléatoire
        noeud, _ = self._selectionner_noeud_aleatoire(self.racine)

        if isinstance(noeud, NoeudInterne):
            # Mutation de fonction : remplacer par une autre fonction avec le même nombre d'arguments
            nouvelle_fonction = random.choice(
                [f for f in self.func_set if f.argument == noeud.fonction.argument]
            )
            noeud.fonction = nouvelle_fonction
        elif isinstance(noeud, NoeudExterne):
            # Mutation de terminal : remplacer par un autre terminal
            noeud.terminal.value = random.uniform(-10, 10)
        else:
            raise ValueError("Type de nœud inconnu pour mutation.")
