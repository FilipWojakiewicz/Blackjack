from Deck import Deck
from Hand import Hand
from Solution import Move


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()
        self.player_score = 100

    def deal(self):
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def split_turn(self):
        while True:
            if self.player_split_hand.get_value() >= 21:
                break

            print("Split's hand:", self.player_split_hand)
            print("Dealer's hand:", self.dealer_hand.cards[0])
            action = input("Make a move (split): ")
            print('\n')

            if action.lower() == "hit":
                self.player_split_hand.add_card(self.deck.deal())
            elif action.lower() == "double":
                self.player_split_hand.add_card(self.deck.deal())
                break
            elif action.lower() == "stand":
                break
        return True

    def player_turn(self):
        while True:
            if self.player_hand.get_value() >= 21:
                break

            print("Player's hand:", self.player_hand)
            print("Dealer's hand:", self.dealer_hand.cards[0])
            action = input("Make a move: ")
            print('\n')

            if action.lower() == "hit":
                self.player_hand.add_card(self.deck.deal())
            elif action.lower() == "double":
                self.player_hand.add_card(self.deck.deal())
                break
            elif action.lower() == "split":
                self.player_split_hand = Hand()
                split = list()
                for i in self.player_hand.cards:
                    split.append(i.value)
                    if split.count(i.value) > 1:
                        self.player_hand.remove_card(i)
                        self.player_split_hand.add_card(i)
                        self.split_turn()
                        break
            elif action.lower() == "stand":
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
        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand.cards[0])
        print("\n   ######### Results #########")
        print(f"            Player {player_value}")
        print(f"            Dealer {dealer_value}")

        if player_value > dealer_value and player_value <= 21:
            self.player_score += 10
            print("Player wins!")
        elif dealer_value > player_value and dealer_value <= 21:
            self.player_score -= 10
            print("Dealer wins!")
        elif player_value > 21 and dealer_value <= 21:
            self.player_score -= 10
            print("Dealer wins!")
        elif player_value < 21 and dealer_value > 21:
            self.player_score += 10
            print("Player wins!")

        if self.player_split_hand is None:
            return

        player_split_value = self.player_split_hand.get_value()
        print(f"            Split {player_split_value}")
        if player_split_value > dealer_value and player_split_value <= 21:
            self.player_score += 10
            print("Split wins!")
        elif dealer_value > player_split_value and dealer_value <= 21:
            self.player_score -= 10
            print("Dealer wins!")
        elif player_split_value > 21 and dealer_value <= 21:
            self.player_score -= 10
            print("Dealer wins!")
        elif player_split_value < 21 and dealer_value > 21:
            self.player_score += 10
            print("Split wins!")

    def is_blackjack(self):
        card1 = self.player_hand.cards[0]
        card2 = self.player_hand.cards[1]
        if card1.value + card2.value == 21:
            return True
        else:
            return False

    def play(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()

        self.deal()
        if self.is_blackjack():
            self.player_score += 15
            print("Blackjack! Player wins!")
            return

        self.player_turn()
        self.dealer_turn()

        self.determine_winner()

    def reset(self):
        self.player_score = 100
