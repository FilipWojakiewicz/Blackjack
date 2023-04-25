import os
from random import choices, choice

import pandas as pd
import time
from Solution import Solution
from BlackjackBot import BlackjackBot
import csv
import os


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
            # solution.display_tables()

        # for t in self.population:
        #     t.display_tables()

    def save_stats(self, bot, population, generation, i):
        stats = {
                'games':    i,
                'splits':   bot.split_count,
                'score':    bot.player_score,
                'wins':     bot.win_count,
                'loses':    bot.lose_count,
                'draws':    (i + bot.split_count) - (bot.win_count + bot.lose_count)
                }
        
        dir_name = str(f'Plots/{self.population_size}_{self.num_games}_{self.generations_number}')

        csv_file = f'{dir_name}/{population}_{generation}.csv'

        with open(csv_file, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(stats.values())

        '''
        print('--------------------------------')
        print('games:   ', i)
        print('splits:  ', bot.split_count)
        print('score:   ', bot.player_score)
        print('wins:    ', bot.win_count)
        print('loses:   ', bot.lose_count)
        print('draws:   ', (i + bot.split_count) - (bot.win_count + bot.lose_count))
        '''

    def results(self, individual, population, generation):
        bot = BlackjackBot()

        dir_name = str(f'Plots/stats/{self.population_size}_{self.num_games}_{self.generations_number}')
        csv_file = f'{dir_name}/{population}_{generation}.csv'
        if os.path.exists(dir_name) == False:
            os.mkdir(dir_name)

        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['games', 'splits', 'score', 'wins', 'loses', 'draws'])

        for i in range(self.num_games):
            bot.play(individual)
            if (i + 1) % 50 == 0:
                self.save_stats(bot, population, generation, i + 1)



    def calculate_fitness(self, individual):
        bot = BlackjackBot()
        for i in range(self.num_games):
            bot.play(individual)

        score = bot.player_score
        '''
        # score = 0
        #
        # for row in range(individual.hard_optimal_solution.shape[0]):
        #     for col in range(individual.hard_optimal_solution.shape[1]):
        #         if individual.hard_optimal_solution[row][col] == individual.hard_hands_table_arr[row][col]:
        #             # print("test")
        #             score += 1
        #
        # for row in range(individual.soft_optimal_solution.shape[0]):
        #     for col in range(individual.soft_optimal_solution.shape[1]):
        #         if individual.soft_optimal_solution[row][col] == individual.soft_hands_table_arr[row][col]:
        #             score += 1
        #
        # for row in range(individual.pairs_optimal_solution.shape[0]):
        #     for col in range(individual.pairs_optimal_solution.shape[1]):
        #         if individual.pairs_optimal_solution[row][col] == individual.pairs_table_arr[row][col]:
        #             score += 1
        #
        # print(score)
        '''
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

    def selection(self, n):
        choices = list()
        for x in range(n):
            choices.append(choice(self.population))
        choices = sorted(choices, key=lambda x: x.fitness_score, reverse=True)
        return choices[0]
        # return max(choices, key=lambda x: x.fitness_score)

    def evolve(self):
        selection_value = 4
        for i in range(self.generations_number):
            score = 0
            print(f"Generation : {i+1}")
            start_time = time.time()
            for genome in self.population:
                # genome.display_tables()
                score += self.calculate_fitness(genome)

            self.population = sorted(self.population, key=lambda x: x.fitness_score, reverse=True)


            txt_file = f'Plots/score/{self.population_size}_{self.num_games}_{self.generations_number}_{selection_value}.txt'
            if i == 0:
                if os.path.exists(txt_file) == True:
                    os.remove(txt_file)
            with open(txt_file, 'a') as file:
                file.write(str(score) + '\n')

            if os.path.exists('Data') == False:
                os.mkdir('Data')
            path = f'Data/Generation_{i+1}'
            os.mkdir(path)
            self.population[0].save_solution_path(path)
            self.next_generation = []
            for x in range(self.population_size):
                parent1 = self.selection(selection_value)  # Póki co n = 7 ale może potem będzie trzeba zmienić
                parent2 = self.selection(selection_value)  # Póki co n = 7 ale może potem będzie trzeba zmienić
                child = self.crossover(parent1, parent2)
                self.next_generation.append(child)

            print("--- %s seconds ---" % (time.time() - start_time))
            if i < self.generations_number - 1:
                self.population = self.next_generation

    def best_solution(self):
        test = self.population
        test = sorted(test, key=lambda x: x.fitness_score, reverse=True)
        return test[0]
