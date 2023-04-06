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
    # hard_hands_table_arr = np.zeros((16, 10), dtype=Move)
    # soft_hands_table_arr = np.zeros((8, 10), dtype=Move)
    # pairs_table_arr = np.zeros((10, 10), dtype=Move)

    # hard_hands_table = None
    # soft_hands_table = None
    # pairs_table = None
    # fitness_score = None

    def __init__(self):
        self.hard_hands_table_arr = np.zeros((16, 10), dtype=Move)
        self.soft_hands_table_arr = np.zeros((8, 10), dtype=Move)
        self.pairs_table_arr = np.zeros((10, 10), dtype=Move)
        self.create_random_solution()
        self.hard_hands_table = pd.DataFrame(self.hard_hands_table_arr, index=['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.soft_hands_table = pd.DataFrame(self.soft_hands_table_arr, index=['9', '8', '7', '6', '5', '4', '3', '2'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.pairs_table = pd.DataFrame(self.pairs_table_arr, index=['11', '10', '9', '8', '7', '6', '5', '4', '3', '2'], columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', '11'])
        self.fitness_score = None
        self.hard_optimal_solution = np.array([
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  #1
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  #2
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  #3
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  #4
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  #5
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],   #6
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],   #7
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],   #8
            [Move.HIT, Move.HIT, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],   #9
            [Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE],  #10
            [Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT],  #11
            [Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  #12
            [Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  #13
            [Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  #14
            [Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  #15
            [Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT]   #16
        ])

        self.soft_optimal_solution = np.array([
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  # 1
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.DOUBLE, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  # 2
            [Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT],  # 3
            [Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 4
            [Move.HIT, Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 5
            [Move.HIT, Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 6
            [Move.HIT, Move.HIT, Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 7
            [Move.HIT, Move.HIT, Move.HIT, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT] # 8
        ])

        self.pairs_optimal_solution = np.array([
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT],  # 1
            [Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND],  # 2
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.STAND, Move.SPLIT, Move.SPLIT, Move.STAND, Move.STAND],  # 3
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT],  # 4
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 5
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 6
            [Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.DOUBLE, Move.HIT, Move.HIT],  # 7
            [Move.HIT, Move.HIT, Move.HIT, Move.SPLIT, Move.SPLIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 8
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT],  # 9
            [Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.SPLIT, Move.HIT, Move.HIT, Move.HIT, Move.HIT]  # 10
        ])

        # print(self.hard_optimal_solution[0][9])  # y, x
        # print(self.pairs_optimal_solution[6][8])  # y, x
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
        hard_hands = self.hard_hands_table_arr
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
        soft_hands = self.soft_hands_table_arr
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
        pairs = self.pairs_table_arr
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
