from Deck import Deck
from Hand import Hand


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()
        self.player_score = 1000

    def deal(self):
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def split_turn(self):
        while True:
            action = input("Do you want to hit or stand? ")
            if action.lower() == "hit":
                self.player_split_hand.add_card(self.deck.deal())
                print("\nPlayer's split hand:", self.player_split_hand, '\n')
                if self.player_split_hand.get_value() > 21:
                    print("Bust! Dealer wins.")
                    return True
            elif action.lower() == "double":
                self.player_split_hand.add_card(self.deck.deal())
                print("\nPlayer's split hand:", self.player_split_hand, '\n')
                return True
            elif action.lower() == "stand":
                break
            else:
                print("Invalid action. Please enter 'hit' or 'stand'.")
        return True

    def player_turn(self):
        while True:
            action = input("Do you want to hit or stand? ")
            if action.lower() == "hit":
                self.player_hand.add_card(self.deck.deal())
                print("\nPlayer's hand:", self.player_hand, '\n')
                if self.player_hand.get_value() > 21:
                    print("Bust! Dealer wins.")
                    return True
            elif action.lower() == "double":
                self.player_hand.add_card(self.deck.deal())
                print("\nPlayer's hand:", self.player_hand, '\n')
                return True
            elif action.lower() == "split":
                self.player_split_hand = Hand()
                test = list()
                for i in self.player_hand.cards:
                    test.append(i.value)
                    print(test)
                    if test.count(i.value) > 1:
                        self.player_hand.remove_card(i)
                        self.player_split_hand.add_card(i)
                        print(test.count(i.value))
                        print("Player's hand:", self.player_hand)
                        print("Split's hand:", self.player_split_hand)
                        self.split_turn()
                        break
            elif action.lower() == "stand":
                break
            else:
                print("Invalid action. Please enter 'hit' or 'stand'.")
        return True

    def dealer_turn(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())
            print("Dealer's hand:", self.dealer_hand)
        if self.dealer_hand.get_value() > 21:
            print("Dealer busts! Player wins.")
            return False
        return True

    def determine_winner(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        print("\n   ######### Results #########")
        print(f"            Player {player_value}")
        print(f"            Dealer {dealer_value}")
        if player_value > dealer_value and player_value <= 21:
            print("Player wins!")
            self.player_score += 100
        elif dealer_value > player_value and dealer_value <= 21:
            print("Dealer wins!")
            self.player_score -= 100
        else:
            print("It's a tie!")

        if self.player_split_hand is None:
            return

        player_split_value = self.player_split_hand.get_value()
        print(f"            Split {player_split_value}")
        if player_split_value > dealer_value and player_split_value <= 21:
            print("Player wins!")
            self.player_score += 100
        elif dealer_value > player_split_value and dealer_value <= 21:
            print("Dealer wins!")
        else:
            print("It's a tie!")

    def play(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.player_split_hand = None
        self.dealer_hand = Hand()

        self.deal()
        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand.cards[0])
        print('\n')

        self.player_turn()
        self.dealer_turn()

        self.determine_winner()
