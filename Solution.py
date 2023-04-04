import numpy as np
from enum import Enum
from random import choice
from IPython.display import display

import pandas as pd


class Move(Enum):
    STAND = 1
    HIT = 2
    DOUBLE = 3
    SPLIT = 4


class Solution:
    hard_hands_table_arr = np.zeros((16, 10), dtype=Move)
    soft_hands_table_arr = np.zeros((8, 10), dtype=Move)
    pairs_table_arr = np.zeros((10, 10), dtype=Move)

    hard_hands_table = None
    soft_hands_table = None
    pairs_table = None
    fitness_score = None

    def __init__(self):
        self.create_random_solution()
        self.hard_hands_table = pd.DataFrame(self.hard_hands_table_arr, index=['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.soft_hands_table = pd.DataFrame(self.soft_hands_table_arr, index=['9', '8', '7', '6', '5', '4', '3', '2'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.pairs_table = pd.DataFrame(self.pairs_table_arr, index=['11', '10', '9', '8', '7', '6', '5', '4', '3', '2'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.fitness_score = None
        # print(self.hard_hands_table_arr[1][0])  # row, col
        # print(self.hard_hands_table['2']['19'])  # col, row
        # display(self.hard_hands_table)
        # display(self.soft_hands_table)
        # display(self.pairs_table)

    def save_solution(self):
        self.hard_hands_table.to_csv('hard_hand.csv', index=True)
        self.soft_hands_table.to_csv('soft_hand.csv', index=True)
        self.pairs_table.to_csv('pairs.csv', index=True)

    def save_solution_path(self, path):
        self.hard_hands_table.to_csv(path + '/hard_hand.csv', index=True)
        self.soft_hands_table.to_csv(path + '/soft_hand.csv', index=True)
        self.pairs_table.to_csv(path + '/pairs.csv', index=True)

    def display_tables(self):
        print('      ######## Hard Hands Table ########')
        hard_hands = self.hard_hands_table
        for x in range(self.hard_hands_table.shape[0]):
            for y in range(self.hard_hands_table.shape[1]):
                if hard_hands[x][y] == Move.HIT:
                    hard_hands[x][y] = "H"
                elif hard_hands[x][y] == Move.STAND:
                    hard_hands[x][y] = "S"
                elif hard_hands[x][y] == Move.DOUBLE:
                    hard_hands[x][y] = "D"
                elif hard_hands[x][y] == Move.SPLIT:
                    hard_hands[x][y] = "P"

        print(hard_hands)
        print('      ######## Soft Hands Table ########')
        soft_hands = self.soft_hands_table
        for x in range(self.soft_hands_table.shape[0]):
            for y in range(self.soft_hands_table.shape[1]):
                if soft_hands[x][y] == Move.HIT:
                    soft_hands[x][y] = "H"
                elif soft_hands[x][y] == Move.STAND:
                    soft_hands[x][y] = "S"
                elif soft_hands[x][y] == Move.DOUBLE:
                    soft_hands[x][y] = "D"
                elif soft_hands[x][y] == Move.SPLIT:
                    soft_hands[x][y] = "P"

        print(soft_hands)
        print('      ######## Pairs Table ########')
        pairs = self.pairs_table
        for x in range(self.pairs_table.shape[0]):
            for y in range(self.pairs_table.shape[1]):
                if pairs[x][y] == Move.HIT:
                    pairs[x][y] = "H"
                elif pairs[x][y] == Move.STAND:
                    pairs[x][y] = "S"
                elif pairs[x][y] == Move.DOUBLE:
                    pairs[x][y] = "D"
                elif pairs[x][y] == Move.SPLIT:
                    pairs[x][y] = "P"

        print(pairs)

    def create_random_solution(self):
        for x in range(self.hard_hands_table_arr.shape[0]):
            for y in range(self.hard_hands_table_arr.shape[1]):
                l = list(Move)
                l.pop()
                move = choice(l)
                self.hard_hands_table_arr[x][y] = move

        for x in range(self.soft_hands_table_arr.shape[0]):
            for y in range(self.soft_hands_table_arr.shape[1]):
                l = list(Move)
                l.pop()
                move = choice(l)
                self.soft_hands_table_arr[x][y] = move

        for x in range(self.pairs_table_arr.shape[0]):
            for y in range(self.pairs_table_arr.shape[1]):
                move = choice(list(Move))
                self.pairs_table_arr[x][y] = move
