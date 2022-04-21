import tkinter as tk
import constants
from tkinter_board import TkinterBoard
from board import Board
from position import Position
from game_state import GameState


def generate_command():
    global gs
    gs = GameState.Generate
    solve_button.pack_forget()
    generate_button.pack_forget()
    gui_board.generate_random_board()
    gui_board.render_values()
    gui_board.pack()


def solve_command():
    global gs
    gs = GameState.EnterBoard
    solve_button.pack_forget()
    generate_button.pack_forget()
    gui_board.reset_board()
    gui_board.pointer = Position(0, 0)
    gui_board.render_pointer()
    gui_board.render_values()
    gui_board.pack()
    generate_solution_button.pack()


def generate_solution_command():
    global gs
    try:
        gui_board.solve_board()
        gs = GameState.DisplayBoard
        generate_solution_button.pack_forget()
        gui_board.pointer = None
        gui_board.render_pointer()
        gui_board.render_values()
    except ValueError:
        print("Given board is not solvable")


def key_handler(event):
    if gs == GameState.EnterBoard:
        print(event.keysym)
        if event.char in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            try:
                gui_board.set_pointer_val(int(event.char))
            except ValueError:
                print("Not a valid number for this space")
        elif event.keysym == 'BackSpace':
            try:
                gui_board.set_pointer_val(None)
            except ValueError:
                print("Cannot remove this value")
        elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
            gui_board.move_pointer(event.keysym)
        gui_board.render_pointer()
        gui_board.render_values()
        gui_board.pack()


top = tk.Tk()
gs = GameState.Menu

solve_button = tk.Button(top, text="SOLVE", command=solve_command)
generate_button = tk.Button(top, text="GENERATE", command=generate_command)
generate_solution_button = tk.Button(top, text="GENERATE SOLUTION", command=generate_solution_command)
# canvas = tk.Canvas(top, bg="white", height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
gui_board = TkinterBoard(top, Board(), None, bg="white",
                         height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
top.bind('<Key>', key_handler)
gui_board.render_empty_board()

# canvas.pack()
solve_button.pack()
generate_button.pack()

top.mainloop()
