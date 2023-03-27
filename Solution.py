from random import choice

import numpy as np
from enum import Enum


class Move(Enum):
    STAND = 1
    HIT = 2
    DOUBLE = 3
    SPLIT = 4


class Solution:
    hard_hands_table = np.zeros((16, 10), dtype=Move)
    soft_hands_table = np.zeros((8, 10), dtype=Move)
    pairs_table = np.zeros((10, 10), dtype=Move)

    def __init__(self):
        self.create_random_solution()

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
        for x in range(self.hard_hands_table.shape[0]):
            for y in range(self.hard_hands_table.shape[1]):
                l = list(Move)
                l.pop()
                move = choice(l)
                self.hard_hands_table[x][y] = move

        for x in range(self.soft_hands_table.shape[0]):
            for y in range(self.soft_hands_table.shape[1]):
                l = list(Move)
                l.pop()
                move = choice(l)
                self.soft_hands_table[x][y] = move

        for x in range(self.pairs_table.shape[0]):
            for y in range(self.pairs_table.shape[1]):
                move = choice(list(Move))
                self.pairs_table[x][y] = move
