from random import *

from Blackjack import Blackjack


class GeneticAlgorithm:
    def __init__(self, population_size, chromosome_length, mutation_rate, elite_size, num_games):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.num_games = num_games
        self.population = []

    def create_individual(self):
        return [randint(0, 1) for _ in range(self.chromosome_length)]

    def create_population(self):
        self.population = [self.create_individual() for _ in range(self.population_size)]

    def calculate_fitness(self, individual):
        game = Blackjack()
        actions = [individual[i:i+2] for i in range(0, len(individual), 2)]
        total_profit = 0
        for _ in range(self.num_games):
            result = game.play(actions)
            if result == -1:
                total_profit -= 1
            elif result == 1:
                total_profit += 1
        avg_profit = total_profit / self.num_games
        return avg_profit

    def crossover(self, parent1, parent2):
        crossover_point = randint(1, self.chromosome_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, individual):
        for i in range(self.chromosome_length):
            if random() < self.mutation_rate:
                individual[i] = 1 - individual[i]

    def selection(self, fitness_scores):
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True)
        selected_indices = sorted_indices[:self.elite_size]
        return [self.population[i] for i in selected_indices]

    def evolve(self):
        fitness_scores = [self.calculate_fitness(individual) for individual in self.population]
        elite_population = self.selection(fitness_scores)
        offspring_population = []
        while len(offspring_population) < self.population_size - self.elite_size:
            parent1 = choice(elite_population)
            parent2 = choice(elite_population)
            child1, child2 = self.crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            offspring_population.append(child1)
            if len(offspring_population) < self.population_size - self.elite_size:
                offspring_population.append(child2)
        self.population = elite_population + offspring_population

    def get_best(self):
        fitness_scores = [self.calculate_fitness(individual) for individual in self.population]
        best_index = fitness_scores.index(max(fitness_scores))
        best_individual = self.population[best_index]
        best_fitness = fitness_scores[best_index]
        return best_individual, best_fitness
