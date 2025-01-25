class fonction:
    def __init__(self,noun,symbol,weight,type):
        self.noun = noun
        self.symbol = symbol
        self.weight = weight
        self.type = type
    def __repr__(self):
        return f" {self.noun, self.symbol, self.type}"