import random


class Position:
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def set_row(self, val):
        self._row = val

    def set_col(self, val):
        self._col = val

    def next(self):
        if self._col == 8:
            new_col = 0
            new_row = self._row + 1
        else:
            new_col = self._col + 1
            new_row = self._row
        return Position(new_row, new_col)

    def up(self):
        new_row = self._row
        if self._row > 0:
            new_row = self._row - 1
        return Position(new_row, self._col)

    def down(self):
        new_row = self._row
        if self._row < 8:
            new_row = self._row + 1
        return Position(new_row, self._col)

    def left(self):
        new_col = self._col
        if self._col > 0:
            new_col = self._col - 1
        return Position(self._row, new_col)

    def right(self):
        new_col = self._col
        if self._col < 8:
            new_col = self._col + 1
        return Position(self._row, new_col)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Position):
            raise TypeError("Position can only compared to another Position")
        return self._row == other._row and self._col == other._col

    def __str__(self):
        return "(" + str(self.get_row()) + ", " + str(self.get_col()) + ")"

    @staticmethod
    def get_all_positions():
        posns = []
        for i in range(9):
            for j in range(9):
                posns.append(Position(i, j))

        random.shuffle(posns)
        return posns

