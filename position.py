import random


class Position:
    """Represents the position of a cell on a sudoku board"""

    def __init__(self, row, col):
        """
        Initialize a position object for position (row, col)
        :param row: Integer: The row of the position (indexed from 0)
        :param col: Integer: The column of the position (indexed from 0)
        """
        self._row = row
        self._col = col

    def get_row(self):
        """
        Get the row from the position
        :return: Integer: The row index
        """
        return self._row

    def get_col(self):
        """
        Get the column from the position
        :return: Integer: The column index
        """
        return self._col

    def set_row(self, val):
        """
        Set the value of the row index
        :param val: Integer: The index to set the row to
        :return: None
        """
        self._row = val

    def set_col(self, val):
        """
        Set the value of the column index
        :param val: Integer: The index to set the column to
        :return: None
        """
        self._col = val

    def next(self):
        """
        Get a Position object at the next position (row-wise)
        :return: Position: The next position
        """
        if self._col == 8:
            new_col = 0
            new_row = self._row + 1
        else:
            new_col = self._col + 1
            new_row = self._row
        return Position(new_row, new_col)

    def up(self):
        """
        Get the Position above self if possible
        :return: Position: Position one above the current position or at the same position if it can't go up further
        """
        new_row = self._row
        if self._row > 0:
            new_row = self._row - 1
        return Position(new_row, self._col)

    def down(self):
        """
        Get the Position below self if possible
        :return: Position: Position one below the current position or at the same position if it can't go down further
        """
        new_row = self._row
        if self._row < 8:
            new_row = self._row + 1
        return Position(new_row, self._col)

    def left(self):
        """
        Get the Position left of self if possible
        :return: Position left of the current position or at the same position if it can't go left further
        """
        new_col = self._col
        if self._col > 0:
            new_col = self._col - 1
        return Position(self._row, new_col)

    def right(self):
        """
        Get the Position right of self if possible
        :return: Position right of the current position or at the same position if it can't go right further
        """
        new_col = self._col
        if self._col < 8:
            new_col = self._col + 1
        return Position(self._row, new_col)

    def __eq__(self, other):
        """
        Check if two positions, self and other, are equal to each other
        :param other: Position or None: The position being compared to self
        :return: Boolean: Do the two positions have the same row and col value? (if other is None return False)
        """
        if other is None:
            return False
        if not isinstance(other, Position):
            raise TypeError("Position can only compared to another Position")
        return self._row == other._row and self._col == other._col

    def __str__(self):
        """
        Convert the position to a string
        :return: String: The position in the form "(row, col)"
        """
        return "(" + str(self.get_row()) + ", " + str(self.get_col()) + ")"

    @staticmethod
    def get_all_positions():
        """
        Get a shuffled list of all possible positions on a 9x9 sudoku board
        :return: List of Positions: List of all possible positions on the board in random order
        """
        posns = []
        for i in range(9):
            for j in range(9):
                posns.append(Position(i, j))

        random.shuffle(posns)
        return posns

