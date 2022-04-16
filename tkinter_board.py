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

    def render_values(self):
        self.delete(constants.VALUE_TAG)
        y = constants.BOARD_HEIGHT // 18
        for i in range(9):
            x = constants.BOARD_HEIGHT // 18
            for j in range(9):
                val = self.board.get_val(Position(i, j))
                if val:
                    self.create_text(x, y, text=str(val), fill="black", font="Arial 35", tag=constants.VALUE_TAG)
                x += constants.SCREEN_HEIGHT // 9
            y += constants.SCREEN_HEIGHT // 9

    def generate_random_board(self):
        self.board = Board.generate_board()

