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
        self.player_score = 1000
        self.solution = None
        self.display = None

    def deal(self):
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def split_turn(self):
        while True:
            if self.player_split_hand.get_value() == 21:
                break

            action = self.split_determine_hand()

            if action == Move.HIT:
                self.player_split_hand.add_card(self.deck.deal())
                # if self.display: print("\nSplits's hand:", self.player_split_hand, '\n')
                if self.player_split_hand.get_value() > 21:
                    # if self.display: print("Bust! Dealer wins.")
                    return True
                if self.player_split_hand.get_value() == 21:
                    return True
            elif action == Move.DOUBLE:
                self.player_split_hand.add_card(self.deck.deal())
                # if self.display: print("\nSplits's hand:", self.player_split_hand, '\n')
                return True
            elif action == Move.STAND:
                break
        return True

    def split_determine_hand(self):
        # if self.player_split_hand.get_value() == 21:
        #     return Move.STAND

        if len(self.player_split_hand.cards) == 1:
            return Move.HIT

        card1 = self.player_split_hand.cards[0]
        card2 = self.player_split_hand.cards[1]
        dealer_card = self.dealer_hand.cards[0]
        value = 0
        col = str(dealer_card.value)

        if len(self.player_split_hand.cards) == 2 and card1.value + card2.value == 21:
            return Move.STAND

        if len(self.player_split_hand.cards) >= 3:
            table = self.solution.hard_hands_table
            for card in self.player_split_hand.cards:
                value += card.value
            if value == 21:
                return Move.STAND
            row = str(value)
            action = table[col][row]
            # if self.display: print(f'Move = {action}, Hand = hard')
            return action
        else:
            if self.player_split_hand.get_value() == 21:
                return Move.STAND
            if (card1.value == 11 or card2.value == 11) and card1.value != card2.value:
                table = self.solution.soft_hands_table
                if card1.value > card2.value:
                    row = str(card2.value)
                else:
                    row = str(card1.value)
                action = table[col][row]
                # if self.display: print(f'Move = {action}, Hand = soft')
                return action
            elif card1.value == card2.value:
                table = self.solution.pairs_table
                row = str(card1.value)
                action = table[col][row]
                if action == Move.SPLIT:
                    v = str(card1.value + card2.value)
                    if card1.value + card2.value < 5:
                        return Move.HIT
                    if card1.value + card2.value > 20:
                        return Move.STAND
                    action = self.solution.hard_hands_table[col][v]
                # if self.display: print(f'Move = {action}, Hand = pair')
                return action
            else:
                table = self.solution.hard_hands_table
                for card in self.player_split_hand.cards:
                    value += card.value
                row = str(value)
                action = table[col][row]
                # if self.display: print(f'Move = {action}, Hand = hard')
                return action

    def determine_hand(self):
        # if self.player_hand.get_value() == 21:
        #     return Move.STAND

        if len(self.player_hand.cards) == 1:
            return Move.HIT

        card1 = self.player_hand.cards[0]
        card2 = self.player_hand.cards[1]
        dealer_card = self.dealer_hand.cards[0]
        value = 0
        col = str(dealer_card.value)

        if len(self.player_hand.cards) == 2 and card1.value + card2.value == 21:
            return Move.STAND

        if len(self.player_hand.cards) >= 3:
            table = self.solution.hard_hands_table
            for card in self.player_hand.cards:
                value += card.value

            if value == 21:
                return Move.STAND

            row = str(value)
            action = table[col][row]
            # if self.display: print(f'Move = {action}, Hand = hard')
            return action
        else:
            if (card1.value == 11 or card2.value == 11) and card1.value != card2.value:
                table = self.solution.soft_hands_table
                if card1.value > card2.value:
                    row = str(card2.value)
                else:
                    row = str(card1.value)
                action = table[col][row]
                # if self.display: print(f'Move = {action}, Hand = soft')
                return action
            elif card1.value == card2.value:
                table = self.solution.pairs_table
                row = str(card1.value)
                action = table[col][row]
                # if self.display: print(f'Move = {action}, Hand = pair')
                return action
            else:
                table = self.solution.hard_hands_table
                for card in self.player_hand.cards:
                    value += card.value
                row = str(value)
                action = table[col][row]
                # if self.display: print(f'Move = {action}, Hand = hard')
                return action

    def player_turn(self):
        while True:
            if self.player_hand.get_value() == 21:
                break

            action = self.determine_hand()

            if action == Move.HIT:
                self.player_hand.add_card(self.deck.deal())
                # if self.display: print("\nPlayer's hand:", self.player_hand, '\n')
                if self.player_hand.get_value() > 21:
                    # if self.display: print("Bust! Dealer wins.")
                    return True
                if self.player_hand.get_value() == 21:
                    return True
            elif action == Move.DOUBLE:
                self.player_hand.add_card(self.deck.deal())
                # if self.display: print("\nPlayer's hand:", self.player_hand, '\n')
                break
            elif action == Move.SPLIT:
                self.player_split_hand = Hand()
                split = list()
                for i in self.player_hand.cards:
                    split.append(i.value)
                    if split.count(i.value) > 1:
                        self.player_hand.remove_card(i)
                        self.player_split_hand.add_card(i)
                        # if self.display: print("Player's hand:", self.player_hand)
                        # if self.display: print("Split's hand:", self.player_split_hand)
                        self.split_turn()
                        break
            elif action == Move.STAND:
                break
        return True

    def dealer_turn(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())
            # if self.display: print("Dealer's hand:", self.dealer_hand)
        if self.dealer_hand.get_value() > 21:
            # if self.display: print("Dealer busts! Player wins.")
            return False
        return True

    def determine_winner(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        # if self.display: print("\n   ######### Results #########")
        # if self.display: print(f"            Player {player_value}")
        # if self.display: print(f"            Dealer {dealer_value}")
        if player_value > dealer_value and player_value <= 21:
            # if self.display: print("Player wins!")
            self.player_score += 10
        elif dealer_value > player_value and dealer_value <= 21:
            # if self.display: print("Dealer wins!")
            self.player_score -= 10
        elif player_value > 21 and dealer_value <= 21:
            # if self.display: print("Dealer wins!")
            self.player_score -= 10
        elif player_value < 21 and dealer_value > 21:
            # if self.display: print("Player wins!")
            self.player_score += 10
        else:
            if self.display: print("It's a tie!")

        if self.player_split_hand is None:
            return

        player_split_value = self.player_split_hand.get_value()
        # if self.display: print(f"            Split {player_split_value}")
        if player_split_value > dealer_value and player_split_value <= 21:
            # if self.display: print("Player wins!")
            self.player_score += 10
        elif dealer_value > player_split_value and dealer_value <= 21:
            # if self.display: print("Dealer wins!")
            self.player_score -= 10
        elif player_split_value > 21 and dealer_value <= 21:
            # if self.display: print("Dealer wins!")
            self.player_score -= 10
        elif player_split_value < 21 and dealer_value > 21:
            # if self.display: print("Player wins!")
            self.player_score += 10
        else:
            if self.display: print("It's a tie!")

    def is_blackjack(self):
        card1 = self.player_hand.cards[0]
        card2 = self.player_hand.cards[1]
        if card1.value + card2.value == 21:
            return True
        else:
            return False

    def play(self, solution, display):
        self.solution = solution
        self.display = display
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()

        self.deal()
        if self.is_blackjack():
            self.player_score += 15
            # if self.display: print('Blackjack! Player wins!')
            return
        # if self.display: print("Player's hand:", self.player_hand)
        # if self.display: print("Dealer's hand:", self.dealer_hand.cards[0])
        # if self.display: print('\n')

        self.player_turn()
        self.dealer_turn()

        self.determine_winner()

    def reset(self):
        self.player_score = 1000
