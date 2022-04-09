class Position:
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def set_row(self):
        return self._row

    def set_col(self):
        return self._col

    def next(self):
        if self._col == 9:
            new_col = 1
            new_row = self._row + 1
        else:
            new_col = self._col + 1
            new_row = self._row
        return Position(new_row, new_col)