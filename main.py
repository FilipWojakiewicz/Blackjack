from Blackjack import Blackjack
from Deck import Deck
from Solution import Solution
from GeneticAlgorithm import GeneticAlgorithm


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    game = Blackjack()
    for i in range(2):
        print(bcolors.WARNING + "################## NEW GAME ##################\n" + bcolors.ENDC)
        game.play()

    print(f'Player score = {game.player_score}')

    # solution = Solution()
    # solution.display_tables()

    # deck = Deck()
    # print(type(deck.cards[0]))
    # for card in deck.cards:
    #     print(card)

