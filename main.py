from BlackjackGame import BlackjackGame
from GeneticAlgorithm import GeneticAlgorithm
import os
import shutil

if __name__ == '__main__':
    # Algorithm
    population_size = 40
    number_of_games = 1000
    generations_number = 100
    ga = GeneticAlgorithm(population_size, number_of_games, generations_number)
    ga.evolve()
    # best = ga.best_solution()
    # best.save_solution()

    #population = 1
    #for genome in ga.population:
    #    # genome.display_tables()
    #    ga.results(genome, population, generations_number)
    #    population += 1

    # GRA   
    #game = BlackjackGame()
    #game.play()



