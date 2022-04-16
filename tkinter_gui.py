import tkinter as tk
import constants
from tkinter_board import TkinterBoard
from board import Board


def generate_command():
    solve_button.pack_forget()
    generate_button.pack_forget()
    gui_board.generate_random_board()
    gui_board.render_values()
    gui_board.pack()

top = tk.Tk()

solve_button = tk.Button(top, text="SOLVE")
generate_button = tk.Button(top, text="GENERATE", command=generate_command)
# canvas = tk.Canvas(top, bg="white", height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
gui_board = TkinterBoard(top, Board(), None, bg="white",
                         height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
gui_board.render_empty_board()

# canvas.pack()
solve_button.pack()
generate_button.pack()

top.mainloop()

