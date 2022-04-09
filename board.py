from entry import Entry
import random


class Board:
    def __init__(self):
        self.matrix = [[Entry()] * 9 for _ in range(9)]

    def set(self, val, pos):
        self.matrix[pos.get_row][pos.get_col].set_val(val)

    def solve(self, pos, rand=False):
        vals = list(range(1, 10))
        if rand:
            random.shuffle(vals)
        for val in vals:
            pass




