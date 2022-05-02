import random


class Position:
    """Represents the position of a cell on a sudoku board"""

    def __init__(self, row, col):
        """
        Initialize a position object for position (row, col)
        :param row: Integer: The row of the position (indexed from 0)
        :param col: Integer: The column of the position (indexed from 0)
        """
        # Initialize row and column values:
        self._row = row
        self._col = col

    def get_row(self):
        """
        Get the row from the position
        :return: Integer: The row index
        """
        return self._row  # Return the row value

    def get_col(self):
        """
        Get the column from the position
        :return: Integer: The column index
        """
        return self._col  # Return the column value

    def set_row(self, val):
        """
        Set the value of the row index
        :param val: Integer: The index to set the row to
        :return: None
        """
        self._row = val  # Set the row value

    def set_col(self, val):
        """
        Set the value of the column index
        :param val: Integer: The index to set the column to
        :return: None
        """
        self._col = val  # Set the column value

    def next(self):
        """
        Get a Position object at the next position (row-wise)
        :return: Position: The next position
        """
        # If on the last position in the row, move to the first position in the next row
        if self._col == 8:
            new_col = 0
            new_row = self._row + 1
        # Otherwise, just move to the next position in the row:
        else:
            new_col = self._col + 1
            new_row = self._row
        return Position(new_row, new_col)  # Return new Position object

    def up(self):
        """
        Get the Position above self if possible
        :return: Position: Position one above the current position or at the same position if it can't go up further
        """
        new_row = self._row
        # If not already on top row, move up one row:
        if self._row > 0:
            new_row = self._row - 1
        return Position(new_row, self._col)  # Return new Position object

    def down(self):
        """
        Get the Position below self if possible
        :return: Position: Position one below the current position or at the same position if it can't go down further
        """
        new_row = self._row
        # If not already on bottom row, move down one row
        if self._row < 8:
            new_row = self._row + 1
        return Position(new_row, self._col)  # Return new Position object

    def left(self):
        """
        Get the Position left of self if possible
        :return: Position left of the current position or at the same position if it can't go left further
        """
        new_col = self._col
        # If not already on leftmost column, move left one column
        if self._col > 0:
            new_col = self._col - 1
        return Position(self._row, new_col)  # Return new Position object

    def right(self):
        """
        Get the Position right of self if possible
        :return: Position right of the current position or at the same position if it can't go right further
        """
        new_col = self._col
        # If not already on rightmost column, move right one column
        if self._col < 8:
            new_col = self._col + 1
        return Position(self._row, new_col)  # Return new Position object

    def __eq__(self, other):
        """
        Check if two positions, self and other, are equal to each other
        :param other: Position or None: The position being compared to self
        :return: Boolean: Do the two positions have the same row and col value? (if other is None return False)
        """
        # If being compared to None, they cannot be equal
        if other is None:
            return False
        # If Position being compared to something that isn't a Position (other than None), raise error
        if not isinstance(other, Position):
            raise TypeError("Position can only compared to another Position")
        # Check and return if row and col values are both equal to each other
        return self._row == other._row and self._col == other._col

    def __str__(self):
        """
        Convert the position to a string
        :return: String: The position in the form "(row, col)"
        """
        # Convert to form "(row, col)" and return
        return "(" + str(self.get_row()) + ", " + str(self.get_col()) + ")"

    @staticmethod
    def get_all_positions():
        """
        Get a shuffled list of all possible positions on a 9x9 sudoku board
        :return: List of Positions: List of all possible positions on the board in random order
        """
        posns = []  # Create empty list to hold Position objects
        # Add each possible position on a Sudoku board to the list:
        for i in range(9):
            for j in range(9):
                posns.append(Position(i, j))
        # Shuffle to randomize and return list:
        random.shuffle(posns)
        return posns
