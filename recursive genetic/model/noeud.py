class Noeud:
    def __init__(self, profondeur=0):
        self.profondeur = profondeur
    def update_profondeur(self, profondeur):
        pass

class NoeudExterne(Noeud):
    def __init__(self, terminal, profondeur=0):
        super().__init__(profondeur)
        self.terminal = terminal
    def evaluer(self, variables):
        return self.terminal.evaluer(variables)
    def update_profondeur(self, profondeur):
        self.profondeur = profondeur
    def __repr__(self):
        return repr(self.terminal)

class NoeudInterne(Noeud):
    def __init__(self, fonction, enfants, profondeur=0): #un enfant est soit un terminal soit une fonction sous la forme d'une listen donc soit un noeud interne ou externe
        super().__init__(profondeur)
        self.fonction = fonction
        self.enfants = enfants
    def update_profondeur(self, profondeur):
        self.profondeur = profondeur
        for enfant in self.enfants:
            enfant.update_profondeur(profondeur + 1)

    def evaluer(self, variables):
        valeurs = [enfant.evaluer(variables) for enfant in self.enfants]
        return self.fonction.apply(*valeurs)

    def __repr__(self):
        if self.fonction.argument == 1:
            return f"{self.fonction.nom}({self.enfants[0]})"
        elif self.fonction.argument == 2:  # Fonction binaire
            return f"({self.enfants[0]} {self.fonction.nom} {self.enfants[1]})"
        else:  # Fonction avec plus d'arguments
            args = ", ".join(map(str, self.enfants))
            return f"{self.fonction.nom}({args})"
