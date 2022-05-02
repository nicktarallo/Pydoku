from entry import Entry
from position import Position
import random
import copy


class Board:
    """Represents a sudoku board"""

    def __init__(self):
        """Creates a Board object with a matrix to hold each entry and also arrays to store the rows, cols, and boxes"""
        self._matrix = [[Entry() for x in range(9)] for _ in range(9)]  # Matrix of entries (9 x 9 like sudoku board)
        self._rows = [set() for _ in range(9)]  # List of sets, 1 for each row showing the values in that row
        self._cols = [set() for _ in range(9)]  # List of sets, 1 for each column showing the values in that col
        # Matrix of sets, 1 for each box, showing values in that box:
        self._boxes = [[set() for x in range(3)] for _ in range(3)]

    def set_val(self, val, pos):
        """
        Set the value on the board at the given position or raise error if it is not possible
        :param val: None or Integer: The value to set the given cell to
        :param pos: Position: The position on the board to set
        :return: None
        """
        # Make sure the value be placed in that position:
        if Entry.value_is_valid(val) and self.entry_non_conflicting(val, pos):
            # If the value is None, then remove the value at that position from the row, col, and box sets
            if val is None:
                self.remove_val(self.get_val(pos), pos)
            # If the value is an integer, then remove the current value if there is one and add the new one to the
            # row, col and box sets that correspond to that position
            elif 1 <= val <= 9:
                if self.get_val(pos):
                    self.remove_val(self.get_val(pos), pos)
                self.add_val(val, pos)
        else:
            # If not possible, raise an error
            raise ValueError("Not a valid value (None or 1-9) or Value already exists in column, row, or box")
        # Set the value in the matrix at that position to the given value:
        self._matrix[pos.get_row()][pos.get_col()].set_val(val)

    def remove_val(self, val, pos):
        """
        Remove the value from the the corresponding row, column, and box set
        :param val: Integer or None: The value to remove
        :param pos: Position: The position of the cell where the value is being removed
        :return: None
        """
        # Remove the given value from the proper row, column, and box set if it is in any of them:
        if val in self.get_row(pos):  # Remove from row
            self.get_row(pos).remove(val)
        if val in self.get_col(pos):  # Remove from col
            self.get_col(pos).remove(val)
        if val in self.get_box(pos):  # Remove from box
            self.get_box(pos).remove(val)

    def add_val(self, val, pos):
        """
        Add a value to the corresponding row, column, and box
        :param val: Integer: The value to be added to the row, col, and box sets
        :param pos: Position: The position on the board where the value is being added
        :return: None
        """
        self.get_row(pos).add(val)  # Add to row set
        self.get_col(pos).add(val)  # Add to column set
        self.get_box(pos).add(val)  # Add to box set

    def solve(self, rand=False, restrict_val=None, restrict_pos=None):
        """
        Attempt to solve the board from the current state
        :param rand: Boolean: Should the values be shuffled for each iteration before placing them to add randomness?
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: None
        """
        if not rand:
            # Try to solve obvious values without backtracking first (if shuffling is not required):
            self._solve_simple(restrict_val, restrict_pos)
        # Attempt to finish solving using the backtracking algorithm:
        solved = self._solve_backtracking(Position(0, 0), rand, restrict_val, restrict_pos)
        if not solved:
            # Raise error if board is unsolvable
            raise ValueError("Given board is not solvable")

    def _solve_simple(self, restrict_val=None, restrict_pos=None):
        """
        Find and fill in clearly solvable values on the board before moving to recursive solution that is slower
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: None
        """
        made_change = True  # Boolean to keep track of whether the board is still being changed
        # Loop until this algorithm can no longer solve any items:
        while made_change:
            made_change = False
            # Check individual cells to see if they can only hold one value:
            made_change = self._check_ind_cells(restrict_val, restrict_pos) or made_change
            # Check rows, cols, and boxes respectively to see if there are places where only one value could fit:
            made_change = self._check_rows(restrict_val, restrict_pos) or made_change
            made_change = self._check_cols(restrict_val, restrict_pos) or made_change
            made_change = self._check_boxes(restrict_val, restrict_pos) or made_change

    def _solve_backtracking(self, pos, rand=False, restrict_val=None, restrict_pos=None):
        """
        Attempt to solve the board from the given state using the recursive backtracking algorithm
        :param pos: Position: The current position to test different values with
        :param rand: Boolean: Should the values be shuffled for each iteration before placing them to add randomness?
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Is the board solved?
        """
        # If the position gets past the ninth and final row, the board is solved:
        if pos.get_row() == 9:
            solved = True
        # If the given position already has a value, move to the next one:
        elif self.get_val(pos) is not None:
            solved = self._solve_backtracking(pos.next(), rand, restrict_val, restrict_pos)
        # Otherwise:
        else:
            vals = list(range(1, 10))  # Create list of possible values to use
            solved = False
            if rand:
                random.shuffle(vals)  # Shuffle the list of values if necessary to randomize solution
            # If this is the restricted position, remove the restricted value from the list so it cannot be tested
            # as a possible solution:
            if pos == restrict_pos:
                vals.remove(restrict_val)
            # Check each value
            for val in vals:
                # If the value can be put in this position:
                if self.entry_non_conflicting(val, pos):
                    # Set the entry at the current position to that value:
                    self.set_val(val, pos)
                    # Attempt to solve the board with this value starting from the next position:
                    solved = self._solve_backtracking(pos.next(), rand, restrict_val, restrict_pos)
                    # If the solving worked, then break out of the loop, but if not, remove the value that was tried
                    # from the board
                    if solved:
                        break
                    self.remove_val(val, pos)
            # If no value could solve the board, reset the value at that position to None and backtrack
            if not solved:
                self.set_val(None, pos)
        return solved  # Return whether the board is solved or not

    def _check_ind_cells(self, restrict_val=None, restrict_pos=None):
        """
        Check each cell to see if there is only one possible value that could fit in that cell based on what is
        already in its row, col, and box
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        # Iterate through each possible position:
        for i in range(9):
            for j in range(9):
                pos = Position(i, j)
                # If there is already a value at this position, move to the next one
                if self.get_val(pos) is not None:
                    continue
                # Get a set of all of the values in the row, col, and box of that position:
                union = self.get_box(pos) | self.get_col(pos) | self.get_row(pos)
                # If 8 values are already there, there can only be 1 left:
                if len(union) == 8:
                    # Find the value that is not already in the row/col/box:
                    val = ({1, 2, 3, 4, 5, 6, 7, 8, 9} - union).pop()
                    # If this is the restrict_pos and restrict_val, do not put the value in:
                    if pos == restrict_pos and restrict_val == val:
                        continue
                    # Otherwise, set the value at that position to the only possible one
                    made_change = True
                    self.set_val(val, pos)
        return made_change  # Return whether a change was made to the board

    def _check_rows(self, restrict_val=None, restrict_pos=None):
        """
        Check each row to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        # Iterate through each row:
        for i in range(len(self._rows)):
            # Find what values are not already in this row:
            missing_vals = set(range(1, 10)) - self._rows[i]
            # Iterate through each value not already in the row:
            for val in missing_vals:
                possible_positions = []  # List to store the positions that value could go in
                # Go through each position in that row:
                for j in range(9):
                    pos = Position(i, j)
                    # If this is the restricted position and value, then skip
                    if restrict_pos == pos and restrict_val == val:
                        continue
                    # If there is no value at this position and the value is valid for this position, add it to the list
                    # of possible positions for the value
                    if self.get_val(pos) is None and self.entry_non_conflicting(val, pos):
                        possible_positions.append(pos)
                # If there is only one possible position for the missing value, then set the entry at that position
                # to that value:
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change  # Return whether a change was made

    def _check_cols(self, restrict_val=None, restrict_pos=None):
        """
        Check each column to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        # Iterate through each column:
        for i in range(len(self._cols)):
            # Find what values are not already in this column:
            missing_vals = set(range(1, 10)) - self._cols[i]
            # Iterate through each value not already in the column:
            for val in missing_vals:
                possible_positions = []  # List to store the positions that value could go in
                # Go through each position in that column:
                for j in range(9):
                    pos = Position(j, i)
                    # If this is the restricted position and value, then skip
                    if restrict_pos == pos and restrict_val == val:
                        continue
                    # If there is no value at this position and the value is valid for this position, add it to the list
                    # of possible positions for the value
                    if self.get_val(pos) is None and self.entry_non_conflicting(val, pos):
                        possible_positions.append(pos)
                # If there is only one possible position for the missing value, then set the entry at that position
                # to that value:
                if len(possible_positions) == 1:
                    self.set_val(val, possible_positions.pop())
                    made_change = True
        return made_change  # Return whether a change was made

    def _check_boxes(self, restrict_val=None, restrict_pos=None):
        """
        Check each box to see if there are any cells where only 1 value could fit and add them if so
        :param restrict_val: None or Integer: If there is a value that should be restricted, what is it?
        :param restrict_pos: None or Position: If there is a position that should be restricted, what is it?
        :return: Boolean: Were any changes made to the board?
        """
        made_change = False
        # Iterate through each box:
        for i in range(3):
            for j in range(3):
                # Find what values are not already in this box:
                missing_vals = set(range(1, 10)) - self._boxes[i][j]
                # Iterate through each value not already in the box:
                for val in missing_vals:
                    possible_positions = []  # List to store the positions that value could go in
                    # Go through each position in that box:
                    for r in range(i * 3, (i + 1) * 3):
                        for c in range(j * 3, (j + 1) * 3):
                            pos = Position(r, c)
                            # If this is the restricted position and value, then skip
                            if restrict_pos == pos and restrict_val == val:
                                continue
                            # If there is no value at this position and the value is valid for this position,
                            # add it to the list of possible positions for the value
                            if self.get_val(pos) is None and self.entry_non_conflicting(val, pos):
                                possible_positions.append(pos)
                    # If there is only one possible position for the missing value, then set the entry at that position
                    # to that value:
                    if len(possible_positions) == 1:
                        self.set_val(val, possible_positions.pop())
                        made_change = True
        return made_change  # Return whether a change was made

    def get_row(self, pos):
        """
        Get the row set corresponding to the given position
        :param pos: Position: The position of the cell that the row is being found for
        :return: Set of Integer: The set of values for the respective row of the position
        """
        return self._rows[pos.get_row()]  # Return row set from row index

    def get_col(self, pos):
        """
        Get the column set corresponding to the given position
        :param pos: Position: The position of the cell that the column is being found for
        :return: Set of Integer: The set of values for the respective column of the position
        """
        return self._cols[pos.get_col()]  # Return col set from col index

    def get_box(self, pos):
        """
        Get the box set corresponding to the given position
        :param pos: Position: The position of the cell that the box is being found for
        :return: Set of Integer: The set of values for the respective box of the position
        """
        # Return box set from row and col index and int division by 3:
        return self._boxes[pos.get_row() // 3][pos.get_col() // 3]

    def get_val(self, pos):
        """
        Get the value of the entry at the given position on the board
        :param pos: Position: The position to get the value from
        :return: None or Integer: The value of the entry at the given position
        """
        return self._matrix[pos.get_row()][pos.get_col()].get_val()  # Return value of entry at given position

    def entry_non_conflicting(self, val, pos):
        """
        Check if the given value is already in the respective box, row, or column of that position
        :param val: Integer: The value that is being checked
        :param pos: Position: The position to get the row, column, and box from
        :return: Boolean: Does the given value NOT conflict with any other values in the row, col, or box?
        """
        # Return True if the val is not in the row, col, or box at that position, False if otherwise
        return (val not in self.get_row(pos)) and (val not in self.get_col(pos)) and (val not in self.get_box(pos))

    @staticmethod
    def generate_board(max_remove=81):
        """
        Generate an unsolved sudoku board with one unique solution
        :param max_remove: Integer: The maximum amount of numbers to remove from the board
        :return: Board: An unsolved sudoku board with one unique solution
        """
        b = Board.get_solved_board()  # Get a random, fully solved board
        posns = Position.get_all_positions()  # Get a list of all positions on the board
        removed = 0  # Counter of how many were removed
        # Iterate while there are still positions to try to remove and the maximum amount given has not been reached:
        while posns and removed < max_remove:
            pos = posns.pop()  # Remove a position
            valid = True
            val = b.get_val(pos)  # Get the value at that position
            b_copy = copy.deepcopy(b)
            b_copy.set_val(None, pos)  # Make a copy of the board and set the value at that position to None
            # Attempt to solve the board while not using the previous value at that position
            try:
                b_copy.solve(restrict_val=val, restrict_pos=pos)
                # If the board solves without error with these restrictions, there is more than one unique solution
                # if this value is removed, so this board is not valid
                valid = False
            except ValueError:
                pass
            # If the board is valid, set the value to None and increase the counter
            if valid:
                b.set_val(None, pos)
                removed += 1
        return b  # Return the generated board

    @staticmethod
    def get_solved_board():
        """
        Generate a random, fully solved sudoku board
        :return: Board: A solved sudoku board
        """
        b = Board()  # Make an empty board
        b.solve(rand=True)  # Solve the board with rand=True so it is different each time
        return b  # Return the solved board

    def __str__(self):
        """
        Convert the board to a string
        :return: String: The board in string form
        """
        s = ""  # Initial empty string
        # Iterate through each value on the matrix:
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                if self._matrix[i][j].get_val() is None:
                    val = 0
                else:
                    val = str(self._matrix[i][j])
                s += str(val) + " "
                if j == 2 or j == 5:
                    s += "| "  # Add vertical borders
            s += "\n"
            if i == 2 or i == 5:
                s += "-" * 21 + "\n"  # Add horizontal borders
        return s  # Return the string
