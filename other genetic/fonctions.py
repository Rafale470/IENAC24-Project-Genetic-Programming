class fonction:
    def __init__(self,noun,symbol,type):
        self.noun = noun
        self.symbol = symbol
        self.type = type
    def __repr__(self):
        return f" {self.noun, self.symbol, self.type}"