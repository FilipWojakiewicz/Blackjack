from random import shuffle
from Card import Card


class Deck:
    def __init__(self):
        # self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] for v in range(1, 14)]
        self.cards = []
        self.build()

    def build(self):
        suits = ['Hearts ♥', 'Diamonds ♦', 'Clubs ♣', 'Spades ♠']
        ranks = {
            'Ace': 11,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 10,
            'Queen': 10,
            'King': 10
        }
        for suit in suits:
            for rank, value in ranks.items():
                c = Card(suit, value, rank)
                # self.cards.append((f'{rank} of {suit}', value))
                self.cards.append(c)

    def shuffle(self):
        if len(self.cards) > 1:
            shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
