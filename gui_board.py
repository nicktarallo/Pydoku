import tkinter as tk
from position import Position
import constants
from board import Board


class GUIBoard(tk.Canvas):
    """Represents a tkinter canvas with specialized methods to draw a board"""

    def __init__(self, master, board, pointer, **kwargs):
        """
        Initialize a GUIBoard object
        :param master: Tk: The window to put the Canvas on
        :param board: Board: A board object to represent the current board to be drawn
        :param pointer: Position or None: Point on the board to be highlighted yellow to enter numbers
        :param kwargs: Additional tk.Canvas arguments
        """
        super().__init__(master, **kwargs)  # Call the tk.Canvas constructor with its necessary arguments
        self._board = board  # Set the board
        self._pointer = pointer  # Set the pointer

    def render_empty_board(self):
        """
        Render an empty board on the Canvas
        :return: None
        """
        self.delete('all')  # Clear the canvas
        # Create borders around sudoku board:
        self.create_line(0, 0, 0, constants.BOARD_HEIGHT, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(0, constants.BOARD_HEIGHT, constants.BOARD_WIDTH,
                         constants.BOARD_HEIGHT, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(constants.BOARD_HEIGHT, constants.BOARD_WIDTH,
                         constants.BOARD_WIDTH, 0, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(constants.BOARD_WIDTH, 0,
                         0, 0, width=7, fill="black", tag=constants.BOARD_TAG)
        pos = constants.BOARD_HEIGHT // 9  # Position to put lines
        # Create the vertical and horizontal gridlines that go on the sudoku board:
        for i in range(8):
            width = 7 if i == 2 or i == 5 else 2  # Determine if line should be thick or thin
            # Horizontal lines:
            self.create_line(0, pos, constants.BOARD_WIDTH, pos, width=width, fill="black", tag=constants.BOARD_TAG)
            # Vertical lines:
            self.create_line(pos, 0, pos, constants.BOARD_HEIGHT, width=width, fill="black", tag=constants.BOARD_TAG)
            pos += constants.BOARD_HEIGHT // 9  # Move to next position

    def render_pointer(self):
        """
        Render a yellow box where the pointer is located if it is not None
        :return: None
        """
        # Remove current pointer from canvas
        self.delete(constants.POINTER_TAG)
        # If there is a pointer:
        if self._pointer:
            # Calculate position to place rectangle
            x = self._pointer.get_col() * constants.BOARD_WIDTH // 9 - self._pointer.get_col() // 2
            y = self._pointer.get_row() * constants.BOARD_HEIGHT // 9 - self._pointer.get_row() // 2
            # Place rectangle at correct position:
            self.create_rectangle(x, y, x + constants.BOARD_WIDTH // 9, y + constants.BOARD_HEIGHT // 9,
                                  fill='yellow', tag=constants.POINTER_TAG)

    def render_values(self):
        """
        Render the board's values on the Canvas in the proper positions
        :return: None
        """
        self.delete(constants.VALUE_TAG)  # Clear all values from the Canvas
        # Iterate through each position on the board and calculate the position it corresponds to on the Canvas:
        y = constants.BOARD_HEIGHT // 18
        for i in range(9):
            x = constants.BOARD_WIDTH // 18
            for j in range(9):
                val = self._board.get_val(Position(i, j))  # Get the value for that position
                # If the value is not None, render it on the Canvas
                if val:
                    self.create_text(x, y, text=str(val), fill="black", font="Arial 35", tag=constants.VALUE_TAG)
                x += constants.BOARD_WIDTH // 9
            y += constants.BOARD_HEIGHT // 9

    def generate_random_board(self, max_remove=81):
        """
        Set the board attribute to be a randomly generated board
        :param max_remove: Integer: The maximum amount of numbers to remove from the board
        :return: None
        """
        self._board = Board.generate_board(max_remove=max_remove)  # Set the board attribute to the generated board

    def solve_board(self):
        """
        Attempt to solve the board associated with the board attribute
        :return: None
        """
        # Solve the board stored in the board attribute and revert if it can't be solved:
        self._board.solve(revert_if_unsolvable=True)

    def reset_board(self):
        """
        Reset the board associated with the board attribute to have no values
        :return: None
        """
        self._board = Board()  # Set board to new Board object

    def set_pointer_val(self, val):
        """
        Set the value at the position of the pointer to val
        :param val: Integer or None: The value to set the entry to
        :return: None
        """
        self._board.set_val(val, self._pointer)  # Set the value of the board at pointer

    def move_pointer(self, key):
        """
        Move the pointer based on the key that was pressed
        :param key: String: The key that was pressed by the user
        :return: None
        """
        # Cases for each arrow key that call the Position method to determine the new location of the pointer:
        if key == 'Up':
            self._pointer = self._pointer.up()
        if key == 'Down':
            self._pointer = self._pointer.down()
        if key == 'Left':
            self._pointer = self._pointer.left()
        if key == 'Right':
            self._pointer = self._pointer.right()

    def remove_pointer(self):
        """
        Set the pointer to none and re-render the pointer
        :return: None
        """
        self._pointer = None  # Set pointer to none
        self.render_pointer()  # Rerender pointer to remove it

    def add_pointer(self):
        """
        Add a pointer to the board at position (0, 0)
        :return: None
        """
        self._pointer = Position(0, 0)  # Set the pointer to Position(0, 0), the top-left corner
