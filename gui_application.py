import tkinter as tk
from tkinter import messagebox
import constants
from gui_board import GUIBoard
from board import Board
from gui_state import GUIState


class GUIApplication:
    """Represents an instance of the GUI application"""

    def __init__(self):
        """Initialize a GUIApplication object with Tkinter attributes"""
        self.gs = None  # To store a GUIState
        self.gui_board = None  # To store a GUIBoard
        # To store tkinter Buttons:
        self.solve_button = None
        self.generate_easy_button = None
        self.generate_medium_button = None
        self.generate_hard_button = None
        self.generate_solution_button = None
        self.main_menu_button = None

    def generate_command(self, max_remove=81):
        """
        Command that runs when the generate button is pressed
        :param max_remove: Integer: The maximum amount of numbers to remove from the board
        :return: None
        """
        # Set gs to the display state:
        self.gs = GUIState.DisplayBoard
        # Hide unnecessary buttons:
        self.solve_button.pack_forget()
        self.pack_forget_generate_buttons()
        # Generate the random board and render:
        self.gui_board.generate_random_board(max_remove)
        self.gui_board.render_values()
        # Pack the board and buttons onto window:
        self.gui_board.pack()
        self.generate_solution_button.pack()
        self.main_menu_button.pack()

    def solve_command(self):
        """
        Command that runs when the solve button is pressed
        :return: None
        """
        # Set gs to the enter state:
        self.gs = GUIState.EnterBoard
        # Hide unnecessary buttons:
        self.solve_button.pack_forget()
        self.pack_forget_generate_buttons()
        # Reset the board to empty, add a pointer, and render the pointer and values:
        self.gui_board.reset_board()
        self.gui_board.add_pointer()
        self.gui_board.render_pointer()
        self.gui_board.render_values()
        # Pack the board and buttons onto window:
        self.gui_board.pack()
        self.generate_solution_button.pack()
        self.main_menu_button.pack()

    def generate_solution_command(self):
        """
        Command that runs when the generate solution button is pressed
        :return: None
        """
        # Try to solve the board:
        try:
            # Attempt to solve board:
            self.gui_board.solve_board()
            # Set gs to display state:
            self.gs = GUIState.DisplayBoard
            # Hide unnecessary button:
            self.generate_solution_button.pack_forget()
            # Remove the pointer and render the values:
            self.gui_board.remove_pointer()
            self.gui_board.render_values()
        # If the board is unsolvable:
        except ValueError:
            # Display message box showing the error and tell user to retry:
            messagebox.showerror("ERROR", "Given board is not solvable.\nCheck board and try again.")

    def main_menu_command(self):
        """
        Command that runs when the main menu button is pressed
        :return: None
        """
        # Set gs to the menu state:
        self.gs = GUIState.Menu
        # Hide unnecessary buttons:
        self.gui_board.pack_forget()
        self.main_menu_button.pack_forget()
        self.generate_solution_button.pack_forget()
        # Remove the pointer:
        self.gui_board.remove_pointer()
        # Pack necessary buttons to window:
        self.solve_button.pack()
        self.pack_generate_buttons()

    def key_handler(self, event):
        """
        Command that runs when a key is pressed
        :param event: Event: The key event triggered by the user pressing a key
        :return: None
        """
        # Only handle keys if the the state allows user to enter a board
        if self.gs == GUIState.EnterBoard:
            # If the user tries to set a number:
            if event.char in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                # Try to set the value at the position of the pointer to the value of the key pressed
                try:
                    self.gui_board.set_pointer_val(int(event.char))
                # If it can't be placed, just print to the console telling user and do not place it
                except ValueError:
                    print("Not a valid number for this space")
            # If the user tries to backspace
            elif event.keysym == 'BackSpace':
                # Try to remove the value at the position of the pointer
                try:
                    self.gui_board.set_pointer_val(None)
                # If it can't be removed, print to the console telling user
                except ValueError:
                    print("Cannot remove this value")
            # If the user hit an arrow key, move the pointer accordingly with move_pointer method:
            elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
                self.gui_board.move_pointer(event.keysym)
            # Render the pointer and values to the GUIBoard:
            self.gui_board.render_pointer()
            self.gui_board.render_values()
            # Pack the board to the window
            self.gui_board.pack()

    def pack_generate_buttons(self):
        """
        Easy way to pack all three generate buttons (1 for each difficulty)
        :return: None
        """
        # Pack all three generate buttons to the window:
        self.generate_easy_button.pack()
        self.generate_medium_button.pack()
        self.generate_hard_button.pack()

    def pack_forget_generate_buttons(self):
        """
        Easy way to hide all three generate buttons (1 for each difficulty)
        :return: None
        """
        # Pack forget (hide) all three generate buttons:
        self.generate_easy_button.pack_forget()
        self.generate_medium_button.pack_forget()
        self.generate_hard_button.pack_forget()

    def run(self):
        """
        Run the GUI application
        :return: None
        """
        # Create top window and title it:
        top = tk.Tk()
        top.wm_title("Pydoku!")

        self.gs = GUIState.Menu  # Set initial GUIState

        # BUTTON CREATION
        # Button to enter solve mode:
        self.solve_button = tk.Button(top, text="SOLVE", command=self.solve_command)
        # Button to generate an easy puzzle:
        self.generate_easy_button = tk.Button(top, text="GENERATE EASY",
                                              command=lambda: self.generate_command(constants.EASY_REMOVE))
        # Button to generate a medium puzzle:
        self.generate_medium_button = tk.Button(top, text="GENERATE MEDIUM",
                                                command=lambda: self.generate_command(constants.MEDIUM_REMOVE))
        # Button to generate a hard puzzle:
        self.generate_hard_button = tk.Button(top, text="GENERATE HARD",
                                              command=lambda: self.generate_command(constants.HARD_REMOVE))
        # Button to generate a solution of the board on screen:
        self.generate_solution_button = tk.Button(top, text="GENERATE SOLUTION", command=self.generate_solution_command)
        # Button to return to main menu
        self.main_menu_button = tk.Button(top, text="MAIN MENU", command=self.main_menu_command)

        # Bind any key to the key handler method:
        top.bind('<Key>', self.key_handler)

        # Initial GUIBoard creation:
        self.gui_board = GUIBoard(top, Board(), None, bg="white",
                                  height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
        self.gui_board.render_empty_board()

        # Pack initial necessary buttons to the window:
        self.solve_button.pack()
        self.pack_generate_buttons()

        # Start the Tkinter loop:
        top.mainloop()
