class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_value(self):
        value = 0
        has_ace = False
        for card in self.cards:
            if card.value > 10:
                value += 10
            elif card.value == 1:
                has_ace = True
                value += 11
            else:
                value += card.value

        if has_ace and value > 21:
            value -= 10

        return value

    def __repr__(self):
        return str(self.cards)
    