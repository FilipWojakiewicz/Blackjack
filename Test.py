import random

class BlackjackGame:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.winner = None

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.player_score = sum(self.player_hand)
        self.dealer_score = sum(self.dealer_hand)

    def hit(self, hand):
        hand.append(self.deck.pop())
        score = sum(hand)
        if score > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            score = sum(hand)
        return score

    def play_game(self):
        self.deal_cards()
        while True:
            if self.player_score == 21:
                self.winner = "player"
                break
            elif self.player_score > 21:
                self.winner = "dealer"
                break
            elif len(self.deck) == 0:
                if self.player_score > self.dealer_score:
                    self.winner = "player"
                elif self.dealer_score > 21:
                    self.winner = "player"
                else:
                    self.winner = "dealer"
                break
            else:
                choice = random.choice(["hit", "stand"])
                if choice == "hit":
                    self.player_score = self.hit(self.player_hand)
                else:
                    while self.dealer_score < 17:
                        self.dealer_score = self.hit(self.dealer_hand)
                    if self.dealer_score > 21:
                        self.winner = "player"
                    elif self.player_score > self.dealer_score:
                        self.winner = "player"
                    else:
                        self.winner = "dealer"
                    break


class BlackjackStrategy:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = []
            for i in range(22):
                self.genes.append(random.choice(["hit", "stand"]))
        else:
            self.genes = genes

    def play(self, game):
        for i in range(len(self.genes)):
            if game.player_score >= i:
                choice = self.genes[i]
                if choice == "hit":
                    game.hit(game.player_hand)
                else:
                    break


if __name__ == "__main__":
    population_size = 100
    mutation_rate = 0.01
    generations = 50

    # Initialize the population with random strategies
    population = [BlackjackStrategy() for i in range(population_size)]

    for i in range(generations):
        # Play a game for each strategy and calculate fitness
        fitness_scores = []
        for strategy in population:
            game = BlackjackGame()
            strategy.play(game)
            if game.winner == "player":
                fitness_scores.append(game.player_score)
            else:
                fitness_scores.append(0)

    # Print the average fitness score for this generation
    avg_fitness = sum(fitness_scores) / len(fitness_scores)
    print("Generation", i+1, "average fitness:", avg_fitness)

    # Select the top performers from the population
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
    top_performers = sorted_population[:int(population_size*0.2)]

    # Create a new population by breeding the top performers
    new_population = []
    for j in range(population_size):
        parent1 = random.choice(top_performers)
        parent2 = random.choice(top_performers)
        genes = []
        for k in range(len(parent1.genes)):
            if random.random() < mutation_rate:
                genes.append(random.choice(["hit", "stand"]))
            else:
                if random.random() < 0.5:
                    genes.append(parent1.genes[k])
                else:
                    genes.append(parent2.genes[k])
        new_population.append(BlackjackStrategy(genes))

    population = new_population

# Play a final game with the best strategy from the last generation
best_strategy = sorted_population[0]
game = BlackjackGame()
best_strategy.play(game)
print("Best strategy score:", game.player_score)

