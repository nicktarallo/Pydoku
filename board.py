from entry import Entry
from position import Position
import random
import copy


class Board:
    """Represents a sudoku board"""

    def __init__(self):
        """Creates a Board object with a matrix to hold each entry and also arrays to store the rows, cols, and boxes"""
        self._matrix = [[Entry() for x in range(9)] for _ in range(9)]
        self._rows = [set() for _ in range(9)]
        self._cols = [set() for _ in range(9)]
        self._boxes = [[set() for x in range(3)] for _ in range(3)]

    def set_val(self, val, pos):
        """
        Set the value on the board at the given position or raise error if it is not possible
        :param val: None or Integer: The value to set the given cell to
        :param pos: Position: The position on the board to set
        :return: None
        """
        if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
            if val is None:
                self.remove_val(self.get_val(pos), pos)
            elif 1 <= val <= 9:
                if self.get_val(pos):
                    self.remove_val(self.get_val(pos), pos)
                self.add_val(val, pos)
        else:
            raise ValueError("Not a valid value (None or 1-9) or Value already exists in column, row, or box")
        self._matrix[pos.get_row()][pos.get_col()].set_val(val)

    def remove_val(self, val, pos):
        """
        Remove the value from the the corresponding row, column, and box set
        :param val: Integer or None: The value to remove
        :param pos: Position: The position of the cell where the value is being removed
        :return: None
        """
        if val in self.get_row(pos):
            self.get_row(pos).remove(val)
        if val in self.get_col(pos):
            self.get_col(pos).remove(val)
        if val in self.get_box(pos):
            self.get_box(pos).remove(val)

    def add_val(self, val, pos):
        """
        Add a value to the corresponding row, column, and box
        :param val: Integer: The value to be added to the row, col, and box sets
        :param pos: Position: The position on the board where the value is being added
        :return: None
        """
        self.get_row(pos).add(val)
        self.get_col(pos).add(val)
        self.get_box(pos).add(val)

    def solve(self, rand=False, restrict_val=None, restrict_pos=None):
        """
        Attempt to solve the board from the current state
        :param rand: Boolean: Should the values be shuffled for each iteration before placing them to add randomness?
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: None
        """
        if not rand:
            self.solve_simple(restrict_val, restrict_pos)
        solved = self._solve(Position(0, 0), rand, restrict_val, restrict_pos)
        if not solved:
            raise ValueError("Given board is not solvable")

    def solve_simple(self, restrict_val=None, restrict_pos=None):
        """
        Find and fill in clearly solvable values on the board before moving to recursive solution that is slower
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: None
        """
        made_change = True
        while made_change:
            made_change = False
            made_change = self.check_ind_cells(restrict_val, restrict_pos) or made_change
            made_change = self.check_rows(restrict_val, restrict_pos) or made_change
            made_change = self.check_cols(restrict_val, restrict_pos) or made_change
            made_change = self.check_boxes(restrict_val, restrict_pos) or made_change

    def _solve(self, pos, rand=False, restrict_val=None, restrict_pos=None):
        """
        Attempt to solve the board from the given state using the recursive backtracking algorithm
        :param pos: Position: The current position to test different values with
        :param rand: Boolean: Should the values be shuffled for each iteration before placing them to add randomness?
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Is the board solved?
        """
        if pos.get_row() == 9:
            solved = True
        elif self.get_val(pos) is not None:
            solved = self._solve(pos.next(), rand, restrict_val, restrict_pos)
        else:
            vals = list(range(1, 10))
            solved = False
            if rand:
                random.shuffle(vals)
            if pos == restrict_pos:
                vals.remove(restrict_val)
            for val in vals:
                if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
                    self.set_val(val, pos)
                    solved = self._solve(pos.next(), rand, restrict_val, restrict_pos)
                    if solved:
                        break
                    self.remove_val(val, pos)
            if not solved:
                self.set_val(None, pos)
        return solved

    def check_ind_cells(self, restrict_val=None, restrict_pos=None):
        """
        Check each cell to see if there is only one possible value that could fit in that cell based on what is
        already in its row, col, and box
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        for i in range(9):
            for j in range(9):
                pos = Position(i, j)
                if self.get_val(pos) is not None:
                    continue
                union = self.get_box(pos) | self.get_col(pos) | self.get_row(pos)
                if len(union) == 8:
                    val = ({1, 2, 3, 4, 5, 6, 7, 8, 9} - union).pop()
                    if pos == restrict_pos:
                        if restrict_val == val:
                            continue
                    made_change = True
                    self.set_val(val, pos)
        return made_change

    def check_rows(self, restrict_val=None, restrict_pos=None):
        """
        Check each row to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        for i in range(len(self._rows)):
            missing_vals = set(range(1, 10)) - self._rows[i]
            for val in missing_vals:
                possible_positions = []
                for j in range(9):
                    pos = Position(i, j)
                    if restrict_pos == pos:
                        if restrict_val == val:
                            continue
                    if self.get_val(pos) is None:
                        if self.entry_non_conflicting(val, pos):
                            possible_positions.append(pos)
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change

    def check_cols(self, restrict_val=None, restrict_pos=None):
        """
        Check each column to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        for i in range(len(self._cols)):
            missing_vals = set(range(1, 10)) - self._cols[i]
            for val in missing_vals:
                possible_positions = []
                for j in range(9):
                    pos = Position(j, i)
                    if restrict_pos == pos:
                        if restrict_val == val:
                            continue
                    if self.get_val(pos) is None:
                        if self.entry_non_conflicting(val, pos):
                            possible_positions.append(pos)
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change

    def check_boxes(self, restrict_val=None, restrict_pos=None):
        """
        Check each box to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        for i in range(3):
            for j in range(3):
                missing_vals = set(range(1, 10)) - self._boxes[i][j]
                for val in missing_vals:
                    possible_positions = []
                    for r in range(i * 3, (i + 1) * 3):
                        for c in range(j * 3, (j + 1) * 3):
                            pos = Position(r, c)
                            if restrict_pos == pos:
                                if restrict_val == val:
                                    continue
                            if self.get_val(pos) is None:
                                if self.entry_non_conflicting(val, pos):
                                    possible_positions.append(pos)
                    if len(possible_positions) == 1:
                        self.set_val(val, possible_positions.pop())
                        made_change = True
        return made_change

    def get_row(self, pos):
        """
        Get the row set corresponding to the given position
        :param pos: Position: The position of the cell that the row is being found for
        :return: Set of Integer: The set of values for the respective row of the position
        """
        return self._rows[pos.get_row()]

    def get_col(self, pos):
        """
        Get the column set corresponding to the given position
        :param pos: Position: The position of the cell that the column is being found for
        :return: Set of Integer: The set of values for the respective column of the position
        """
        return self._cols[pos.get_col()]

    def get_box(self, pos):
        """
        Get the box set corresponding to the given position
        :param pos: Position: The position of the cell that the box is being found for
        :return: Set of Integer: The set of values for the respective box of the position
        """
        return self._boxes[pos.get_row() // 3][pos.get_col() // 3]

    def get_val(self, pos):
        """
        Get the value of the entry at the given position on the board
        :param pos: Position: The position to get the value from
        :return: None or Integer: The value of the entry at the given position
        """
        return self._matrix[pos.get_row()][pos.get_col()].get_val()

    def entry_non_conflicting(self, val, pos):
        """
        Check if the given value is already in the respective box, row, or column of that position
        :param val: Integer: The value that is being checked
        :param pos: Position: The position to get the row, column, and box from
        :return: Boolean: Does the given value NOT conflict with any other values in the row, col, or box?
        """
        return (val not in self.get_row(pos)) and (val not in self.get_col(pos)) and (val not in self.get_box(pos))

    @staticmethod
    def generate_board(max_remove=81):
        """
        Generate an unsolved sudoku board with one unique solution
        :return: Board: An unsolved sudoku board with one unique solution
        """
        b = Board.get_solved_board()
        posns = Position.get_all_positions()
        removed = 0
        while posns and removed < max_remove:
            pos = posns.pop()
            valid = True
            val = b.get_val(pos)
            b_copy = copy.deepcopy(b)
            b_copy.set_val(None, pos)
            try:
                b_copy.solve(restrict_val=val, restrict_pos=pos)
                valid = False
            except ValueError:
                pass
            if valid:
                b.set_val(None, pos)
                removed += 1
        return b

    @staticmethod
    def get_solved_board():
        """
        Generate a random, fully solved sudoku board
        :return: Board: A solved sudoku board
        """
        b = Board()
        b.solve(True)
        return b

    def __str__(self):
        """
        Convert the board to a string
        :return: String: The board in string form
        """
        s = ""
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                if self._matrix[i][j].get_val() is None:
                    val = 0
                else:
                    val = str(self._matrix[i][j])
                s += str(val) + " "
                if j == 2 or j == 5:
                    s += "| "
            s += "\n"
            if i == 2 or i == 5:
                s += "-" * 21 + "\n"
        return s
