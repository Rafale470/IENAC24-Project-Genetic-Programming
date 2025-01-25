class Fonction:
    def __init__(self, nom, argument, fonction):
        self.nom = nom
        self.argument = argument
        self.fonction = fonction

    def apply(self, *arguments): #applique à une liste d'arguments
        if len(arguments) != self.argument:
            raise ValueError(f"La fonction {self.nom} attend {self.argument} arguments, mais {len(arguments)} ont été fournis.")
        return self.fonction(*arguments)

    def __repr__(self):
        return f"Fonction(nom='{self.nom}', arguments={self.argument})"