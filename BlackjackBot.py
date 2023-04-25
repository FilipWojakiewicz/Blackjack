from Deck import Deck
from Hand import Hand
from enum import Enum
from Solution import Move


class BlackjackBot:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()
        self.player_score = 100
        self.solution = None
        self.win_count = 0
        self.lose_count = 0
        self.split_count = 0

    def deal(self):
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def split_turn(self):
        while True:
            if self.player_split_hand.get_value() >= 21:
                break

            action = self.split_determine_hand()

            if action == Move.SPLIT:
                action = Move.STAND

            if action == Move.HIT:
                self.player_split_hand.add_card(self.deck.deal())
            elif action == Move.DOUBLE:
                self.player_split_hand.add_card(self.deck.deal())
                break
            elif action == Move.STAND:
                break
        return True

    def split_determine_hand(self):
        num_of_cards = len(self.player_split_hand.cards)
        if num_of_cards == 1:
            return Move.HIT
        elif num_of_cards == 2:
            dealer_card = self.dealer_hand.cards[0]
            col = str(dealer_card.value)
            card1 = self.player_split_hand.cards[0]
            card2 = self.player_split_hand.cards[1]
            if (card1.value == 11 or card2.value == 11) and card1.value != card2.value:
                table = self.solution.soft_hands_table
                if card1.value > card2.value:
                    row = str(card2.value)
                else:
                    row = str(card1.value)
                action = table[col][row]
                return action
            elif card1.value == card2.value:
                table = self.solution.pairs_table
                row = str(card1.value)
                action = table[col][row]
                return action
            else:
                table = self.solution.hard_hands_table
                value = self.player_split_hand.get_value()
                row = str(value)
                action = table[col][row]
                return action
        elif num_of_cards >= 3:
            dealer_card = self.dealer_hand.cards[0]
            col = str(dealer_card.value)
            table = self.solution.hard_hands_table
            value = self.player_split_hand.get_value()
            row = str(value)
            action = table[col][row]
            return action

    def determine_hand(self):
        num_of_cards = len(self.player_hand.cards)
        if num_of_cards == 1:
            return Move.HIT
        elif num_of_cards == 2:
            dealer_card = self.dealer_hand.cards[0]
            col = str(dealer_card.value)
            card1 = self.player_hand.cards[0]
            card2 = self.player_hand.cards[1]
            if (card1.value == 11 or card2.value == 11) and card1.value != card2.value:
                table = self.solution.soft_hands_table
                if card1.value > card2.value:
                    row = str(card2.value)
                else:
                    row = str(card1.value)
                action = table[col][row]
                return action
            elif card1.value == card2.value:
                table = self.solution.pairs_table
                row = str(card1.value)
                action = table[col][row]
                return action
            else:
                table = self.solution.hard_hands_table
                value = self.player_hand.get_value()
                row = str(value)
                action = table[col][row]
                return action
        elif num_of_cards >= 3:
            dealer_card = self.dealer_hand.cards[0]
            col = str(dealer_card.value)
            table = self.solution.hard_hands_table
            value = self.player_hand.get_value()
            row = str(value)
            action = table[col][row]
            return action

    def player_turn(self):
        while True:
            if self.player_hand.get_value() >= 21:
                break

            action = self.determine_hand()

            if action == Move.HIT:
                self.player_hand.add_card(self.deck.deal())
            elif action == Move.DOUBLE:
                self.player_hand.add_card(self.deck.deal())
                break
            elif action == Move.SPLIT:
                self.split_count += 1
                self.player_split_hand = Hand()
                split = list()
                for i in self.player_hand.cards:
                    split.append(i.value)
                    if split.count(i.value) > 1:
                        self.player_hand.remove_card(i)
                        self.player_split_hand.add_card(i)
                        self.split_turn()
                        break
            elif action == Move.STAND:
                break
            else:
                break

    def dealer_turn(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())
        if self.dealer_hand.get_value() > 21:
            return False
        return True

    def determine_winner(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()

        if player_value > dealer_value and player_value <= 21:
            self.player_score += 10
            self.win_count += 1
        elif dealer_value > player_value and dealer_value <= 21:
            self.player_score -= 10
            self.lose_count += 1
        elif player_value > 21 and dealer_value <= 21:
            self.player_score -= 10
            self.lose_count += 1
        elif player_value < 21 and dealer_value > 21:
            self.player_score += 10
            self.win_count += 1

        if self.player_split_hand is None:
            return

        player_split_value = self.player_split_hand.get_value()
        if player_split_value > dealer_value and player_split_value <= 21:
            self.player_score += 10
            self.win_count += 1
        elif dealer_value > player_split_value and dealer_value <= 21:
            self.player_score -= 10
            self.lose_count += 1
        elif player_split_value > 21 and dealer_value <= 21:
            self.player_score -= 10
            self.lose_count += 1
        elif player_split_value < 21 and dealer_value > 21:
            self.player_score += 10
            self.win_count += 1

    def is_blackjack(self):
        card1 = self.player_hand.cards[0]
        card2 = self.player_hand.cards[1]
        if card1.value + card2.value == 21:
            return True
        else:
            return False

    def play(self, solution):
        self.solution = solution
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()

        self.deal()
        if self.is_blackjack():
            self.player_score += 15
            return

        self.player_turn()
        self.dealer_turn()

        self.determine_winner()

    def reset(self):
        self.player_score = 100
