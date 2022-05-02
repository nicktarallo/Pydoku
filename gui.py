import tkinter as tk
from tkinter import messagebox
import constants
from gui_board import GUIBoard
from board import Board
from game_state import GameState


class GUI:
    """Represents an instance of the GUI application"""

    def __init__(self):
        """Initialize a GUI object with Tkinter attributes"""
        self.gs = None
        self.gui_board = None
        self.solve_button = None
        self.generate_button = None
        self.generate_solution_button = None
        self.main_menu_button = None

    def generate_command(self):
        """
        Command that runs when the generate button is pressed
        :return: None
        """
        self.gs = GameState.DisplayBoard
        self.solve_button.pack_forget()
        self.generate_button.pack_forget()
        self.gui_board.generate_random_board()
        self.gui_board.render_values()
        self.gui_board.pack()
        self.generate_solution_button.pack()
        self.main_menu_button.pack()

    def solve_command(self):
        """
        Command that runs when the solve button is pressed
        :return: None
        """
        self.gs = GameState.EnterBoard
        self.solve_button.pack_forget()
        self.generate_button.pack_forget()
        self.gui_board.reset_board()
        self.gui_board.add_pointer()
        self.gui_board.render_pointer()
        self.gui_board.render_values()
        self.gui_board.pack()
        self.generate_solution_button.pack()
        self.main_menu_button.pack()

    def generate_solution_command(self):
        """
        Command that runs when the generate solution button is pressed
        :return: None
        """
        try:
            self.gui_board.solve_board()
            self.gs = GameState.DisplayBoard
            self.generate_solution_button.pack_forget()
            self.gui_board.remove_pointer()
            self.gui_board.render_pointer()
            self.gui_board.render_values()
        except ValueError:
            messagebox.showerror("ERROR", "Given board is not solvable.\nCheck board and try again.")

    def main_menu_command(self):
        """
        Command that runs when the main menu button is pressed
        :return: None
        """
        self.gs = GameState.Menu
        self.gui_board.pack_forget()
        self.main_menu_button.pack_forget()
        self.generate_solution_button.pack_forget()
        self.gui_board.remove_pointer()
        self.solve_button.pack()
        self.generate_button.pack()

    def key_handler(self, event):
        """
        Command that runs when a key is pressed
        :param event: Event: The key event triggered by the user pressing a key
        :return: None
        """
        if self.gs == GameState.EnterBoard:
            if event.char in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                try:
                    self.gui_board.set_pointer_val(int(event.char))
                except ValueError:
                    print("Not a valid number for this space")
            elif event.keysym == 'BackSpace':
                try:
                    self.gui_board.set_pointer_val(None)
                except ValueError:
                    print("Cannot remove this value")
            elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
                self.gui_board.move_pointer(event.keysym)
            self.gui_board.render_pointer()
            self.gui_board.render_values()
            self.gui_board.pack()

    def run(self):
        """
        Run the GUI application
        :return: None
        """
        top = tk.Tk()
        top.wm_title("Pydoku!")
        self.gs = GameState.Menu

        self.solve_button = tk.Button(top, text="SOLVE", command=self.solve_command)
        self.generate_button = tk.Button(top, text="GENERATE", command=self.generate_command)
        self.generate_solution_button = tk.Button(top, text="GENERATE SOLUTION", command=self.generate_solution_command)
        self.main_menu_button = tk.Button(top, text="MAIN MENU", command=self.main_menu_command)
        self.gui_board = GUIBoard(top, Board(), None, bg="white",
                                  height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
        top.bind('<Key>', self.key_handler)
        self.gui_board.render_empty_board()

        self.solve_button.pack()
        self.generate_button.pack()

        top.mainloop()
