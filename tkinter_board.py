import tkinter as tk
from position import Position
import constants
from board import Board
from copy import deepcopy


class TkinterBoard(tk.Canvas):
    """Represents a tkinter canvas with specialized methods to draw a board"""

    def __init__(self, master, board, pointer, **kwargs):
        """
        Initialize a TkinterBoard object
        :param master: Tk: The window to put the Canvas on
        :param board: Board: A board object to represent the current board to be drawn
        :param pointer: Position or None: Point on the board to be highlighted yellow to enter numbers
        :param kwargs: Additional tk.Canvas arguments
        """
        super().__init__(master, **kwargs)
        self.board = board
        self.pointer = pointer

    def render_empty_board(self):
        """
        Render an empty board on the Canvas
        :return: None
        """
        self.delete('all')
        self.create_line(0, 0, 0, constants.BOARD_HEIGHT, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(0, constants.BOARD_HEIGHT, constants.BOARD_HEIGHT,
                         constants.BOARD_HEIGHT, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(constants.BOARD_HEIGHT, constants.BOARD_HEIGHT,
                         constants.BOARD_HEIGHT, 0, width=7, fill="black", tag=constants.BOARD_TAG)
        self.create_line(constants.BOARD_HEIGHT, 0,
                         0, 0, width=7, fill="black", tag=constants.BOARD_TAG)
        pos = constants.BOARD_HEIGHT // 9
        for i in range(8):
            width = 7 if i == 2 or i == 5 else 2
            self.create_line(0, pos, constants.BOARD_HEIGHT, pos, width=width, fill="black", tag=constants.BOARD_TAG)
            self.create_line(pos, 0, pos, constants.BOARD_HEIGHT, width=width, fill="black", tag=constants.BOARD_TAG)
            pos += constants.BOARD_HEIGHT // 9

    def render_pointer(self):
        """
        Render a yellow box where the pointer is located if it is not None
        :return: None
        """
        self.delete(constants.POINTER_TAG)
        if self.pointer:
            x = self.pointer.get_col() * constants.BOARD_WIDTH // 9 - self.pointer.get_col() // 2
            y = self.pointer.get_row() * constants.BOARD_HEIGHT // 9 - self.pointer.get_row() // 2
            self.create_rectangle(x, y, x + constants.BOARD_WIDTH // 9, y + constants.BOARD_HEIGHT // 9,
                                  fill='yellow', tag=constants.POINTER_TAG)

    def render_values(self):
        """
        Render the board's values on the Canvas in the proper positions
        :return: None
        """
        self.delete(constants.VALUE_TAG)
        y = constants.BOARD_HEIGHT // 18
        for i in range(9):
            x = constants.BOARD_WIDTH // 18
            for j in range(9):
                val = self.board.get_val(Position(i, j))
                if val:
                    self.create_text(x, y, text=str(val), fill="black", font="Arial 35", tag=constants.VALUE_TAG)
                x += constants.BOARD_WIDTH // 9
            y += constants.BOARD_HEIGHT // 9

    def generate_random_board(self):
        """
        Set the board attribute to be a randomly generated board
        :return: None
        """
        self.board = Board.generate_board()

    def solve_board(self):
        """
        Attempt to solve the board associated with the board attribute
        :return: None
        """
        self.board.solve()

    def reset_board(self):
        """
        Reset the board associated with the board attribute to have no values
        :return: None
        """
        self.board = Board()

    def set_pointer_val(self, val):
        """
        Set the value at the position of the pointer to val
        :param val: Integer or None: The value to set the entry to
        :return: None
        """
        self.board.set_val(val, self.pointer)

    def move_pointer(self, key):
        """
        Move the pointer based on the key that was pressed
        :param key: String: The key that was pressed by the user
        :return: None
        """
        if key == 'Up':
            self.pointer = self.pointer.up()
        if key == 'Down':
            self.pointer = self.pointer.down()
        if key == 'Left':
            self.pointer = self.pointer.left()
        if key == 'Right':
            self.pointer = self.pointer.right()

    def remove_pointer(self):
        """
        Set the pointer to none and re-render the pointer
        :return: None
        """
        self.pointer = None
        self.render_pointer()

    def add_pointer(self):
        """
        Add a pointer to the board at position (0, 0)
        :return: None
        """
        self.pointer = Position(0, 0)


