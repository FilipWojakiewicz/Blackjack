import os
from random import choices, choice

import pandas as pd
import time
from Solution import Solution
from BlackjackBot import BlackjackBot


class GeneticAlgorithm:
    def __init__(self, population_size, num_games, generations_number):
        self.population_size = population_size
        self.num_games = num_games
        self.generations_number = generations_number
        self.population = []
        self.next_generation = []
        self.best = None
        self.create_population()

    def create_population(self):
        for i in range(self.population_size):
            solution = Solution()
            self.population.append(solution)

    def calculate_fitness(self, individual):
        bot = BlackjackBot()
        for i in range(self.num_games):
            bot.play(individual, False)

        score = bot.player_score
        individual.fitness_score = score
        return score

    def crossover(self, parent1, parent2):
        new_solution = Solution()

        for row in range(parent1.hard_hands_table.shape[0]):
            for col in range(parent1.hard_hands_table.shape[1]):
                r = choice(['parent1', 'parent2'])
                if r == 'parent1':
                    new_solution.hard_hands_table_arr[row][col] = parent1.hard_hands_table_arr[row][col]
                else:
                    new_solution.hard_hands_table_arr[row][col] = parent2.hard_hands_table_arr[row][col]

        for row in range(parent1.soft_hands_table.shape[0]):
            for col in range(parent1.soft_hands_table.shape[1]):
                r = choice(['parent1', 'parent2'])
                if r == 'parent1':
                    new_solution.soft_hands_table_arr[row][col] = parent1.soft_hands_table_arr[row][col]
                else:
                    new_solution.soft_hands_table_arr[row][col] = parent2.soft_hands_table_arr[row][col]

        for row in range(parent1.pairs_table.shape[0]):
            for col in range(parent1.pairs_table.shape[1]):
                r = choice(['parent1', 'parent2'])
                if r == 'parent1':
                    new_solution.pairs_table_arr[row][col] = parent1.pairs_table_arr[row][col]
                else:
                    new_solution.pairs_table_arr[row][col] = parent2.pairs_table_arr[row][col]

        new_solution.hard_hands_table = pd.DataFrame(new_solution.hard_hands_table_arr,
                                             index=['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10',
                                                    '9', '8', '7', '6', '5'],
                                             columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        new_solution.soft_hands_table = pd.DataFrame(new_solution.soft_hands_table_arr, index=['9', '8', '7', '6', '5', '4', '3', '2'],
                                             columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        new_solution.pairs_table = pd.DataFrame(new_solution.pairs_table_arr,
                                        index=['11', '10', '9', '8', '7', '6', '5', '4', '3', '2'],
                                        columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])

        return new_solution

    def mutate(self, individual):
        # Randomowo zmieniać jakieś ruchy na inne z możliwych z pewnym prawdopodobieństwem
        pass

    def selection(self, n):
        choices = list()
        for x in range(n):
            choices.append(choice(self.population))
        choices = sorted(choices, key=lambda x: x.fitness_score, reverse=True)
        return choices[0]
        # return max(choices, key=lambda x: x.fitness_score)

    def evolve(self):
        for i in range(self.generations_number):
            print(f"Generation : {i+1}")
            start_time = time.time()
            for genome in self.population:
                self.calculate_fitness(genome)

            self.population = sorted(self.population, key=lambda x: x.fitness_score, reverse=True)

            path = f'Data/Generation_{i+1}'
            os.mkdir(path)
            self.population[0].save_solution_path(path)
            self.next_generation = []
            for x in range(self.population_size):
                parent1 = self.selection(5)  # Póki co n = 10 ale może potem będzie trzeba zmienić
                parent2 = self.selection(5)  # Póki co n = 10 ale może potem będzie trzeba zmienić
                child = self.crossover(parent1, parent2)
                self.next_generation.append(child)

            print("--- %s seconds ---" % (time.time() - start_time))
            if i < self.generations_number - 1:
                self.population = self.next_generation

    def best_solution(self):
        test = self.population
        test = sorted(test, key=lambda x: x.fitness_score, reverse=True)
        return test[0]
