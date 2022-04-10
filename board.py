from entry import Entry
from position import Position
import random


class Board:
    def __init__(self):
        self._matrix = [[Entry() for x in range(9)] for _ in range(9)]
        self._rows = [set() for _ in range(9)]
        self._cols = [set() for _ in range(9)]
        self._boxes = [[set() for x in range(3)] for _ in range(3)]

    def set_val(self, val, pos):
        if self.entry_is_valid(val):
            if val is None:
                self.remove_val(self.get_val(pos), pos)
            elif 1 <= val <= 9:
                self.add_val(val, pos)
        else:
            raise ValueError("Not a valid value (None or 1-9)")
        self._matrix[pos.get_row()][pos.get_col()].set_val(val)

    def remove_val(self, val, pos):
        if val in self.get_row(pos):
            self.get_row(pos).remove(val)
        if val in self.get_col(pos):
            self.get_col(pos).remove(val)
        if val in self.get_box(pos):
            self.get_box(pos).remove(val)

    def add_val(self, val, pos):
        self.get_row(pos).add(val)
        self.get_col(pos).add(val)
        self.get_box(pos).add(val)

    def solve(self, rand=False):
        solved = self._solve(Position(0, 0), rand)
        if not solved:
            raise ValueError("Given board is not solvable")

    def _solve(self, pos, rand=False):
        if pos.get_row() == 9:
            solved = True
        elif self.get_val(pos) is not None:
            solved = self._solve(pos.next(), rand)
        else:
            vals = list(range(1, 10))
            solved = False
            if rand:
                random.shuffle(vals)
            for val in vals:
                if self.entry_is_valid(val) and self.entry_non_conflicting(val, pos):
                    self.set_val(val, pos)
                    solved = self._solve(pos.next(), rand)
                    if solved:
                        break
                    self.remove_val(val, pos)
            if not solved:
                self.set_val(None, pos)
        return solved

    def get_row(self, pos):
        return self._rows[pos.get_row()]

    def get_col(self, pos):
        return self._cols[pos.get_col()]

    def get_box(self, pos):
        return self._boxes[pos.get_row() // 3][pos.get_col() // 3]

    def get_val(self, pos):
        return self._matrix[pos.get_row()][pos.get_col()].get_val()

    @staticmethod
    def entry_is_valid(val):
        return val is None or 1 <= val <= 9

    def entry_non_conflicting(self, val, pos):
        return (val not in self.get_row(pos)) and (val not in self.get_col(pos)) and (val not in self.get_box(pos))

    def __str__(self):
        s = ""
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                s += str(self._matrix[i][j]) + " "
                if j == 2 or j == 5:
                    s += "| "
            s += "\n"
            if i == 2 or i == 5:
                s += "-" * 21 + "\n"
        return s




