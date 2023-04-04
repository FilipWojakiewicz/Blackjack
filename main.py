from GeneticAlgorithm import GeneticAlgorithm
from Solution import Solution

if __name__ == '__main__':
    # Algorithm
    population_size = 500
    number_of_games = 50000
    generations_number = 100
    ga = GeneticAlgorithm(population_size, number_of_games, generations_number)
    ga.evolve()
    best = ga.best_solution()
    best.save_solution()

    # s = Solution()
    # print(s.hard_hands_table.shape[1])

    ## Deck cards
    # deck = Deck()
    # print(type(deck.cards[0]))
    # for card in deck.cards:
    #     print(card)

