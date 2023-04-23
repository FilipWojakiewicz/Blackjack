from BlackjackGame import BlackjackGame
from GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # Algorithm
    population_size = 1
    number_of_games = 100
    generations_number = 10
    ga = GeneticAlgorithm(population_size, number_of_games, generations_number)
    # ga.evolve()
    # best = ga.best_solution()
    # best.save_solution()

    for genome in ga.population:
        # genome.display_tables()
        ga.results(genome)

    # GRA
    #game = BlackjackGame()
    #game.play()



