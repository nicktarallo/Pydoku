import tkinter as tk
from position import Position
import constants
from board import Board


class TkinterBoard(tk.Canvas):
    def __init__(self, master, board, pointer, **kwargs):
        super().__init__(master, **kwargs)
        self.board = board
        self.pointer = pointer

    def render_empty_board(self):
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
        self.delete(constants.POINTER_TAG)
        if self.pointer:
            x = self.pointer.get_col() * constants.BOARD_WIDTH // 9 - self.pointer.get_col() // 2
            y = self.pointer.get_row() * constants.BOARD_HEIGHT // 9 - self.pointer.get_row() // 2
            self.create_rectangle(x, y, x + constants.BOARD_WIDTH // 9, y + constants.BOARD_HEIGHT // 9,
                                  fill='yellow', tag=constants.POINTER_TAG)

    def render_values(self):
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
        self.board = Board.generate_board()

    def solve_board(self):
        self.board.solve()

    def reset_board(self):
        self.board = Board()

    def set_pointer_val(self, val):
        self.board.set_val(val, self.pointer)

    def move_pointer(self, key):
        if key == 'Up':
            self.pointer = self.pointer.up()
        if key == 'Down':
            self.pointer = self.pointer.down()
        if key == 'Left':
            self.pointer = self.pointer.left()
        if key == 'Right':
            self.pointer = self.pointer.right()

