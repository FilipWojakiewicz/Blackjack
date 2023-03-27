class Card:
    def __init__(self, suit, value, rank):
        self.suit = suit
        self.value = value
        self.rank = rank

    def __repr__(self):
        return "{} of {}, {}".format(self.rank, self.suit, self.value)
