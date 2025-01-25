class Terminal:
    def __init__(self, valeur):
        self.valeur = valeur

    def evaluer(self, variables):
        if isinstance(self.valeur, (int, float)):  #Constante
            return self.valeur
        return variables.get(self.valeur)

    def __repr__(self):
        return str(self.valeur)