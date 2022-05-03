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
        self._gs = None  # To store a GUIState
        self._gui_board = None  # To store a GUIBoard
        # To store tkinter Buttons:
        self._solve_button = None
        self._generate_easy_button = None
        self._generate_medium_button = None
        self._generate_hard_button = None
        self._generate_solution_button = None
        self._main_menu_button = None

    def run(self):
        """
        Run the GUI application
        :return: None
        """
        # Create top window and title it:
        top = tk.Tk()
        top.wm_title("Pydoku!")

        self._gs = GUIState.MENU  # Set initial GUIState

        # BUTTON CREATION
        # Button to enter solve mode:
        self._solve_button = tk.Button(top, text="SOLVE", command=self._solve_command)
        # Button to generate an easy puzzle:
        self._generate_easy_button = tk.Button(top, text="GENERATE EASY",
                                               command=lambda: self._generate_command(constants.EASY_REMOVE))
        # Button to generate a medium puzzle:
        self._generate_medium_button = tk.Button(top, text="GENERATE MEDIUM",
                                                 command=lambda: self._generate_command(constants.MEDIUM_REMOVE))
        # Button to generate a hard puzzle:
        self._generate_hard_button = tk.Button(top, text="GENERATE HARD",
                                               command=lambda: self._generate_command(constants.HARD_REMOVE))
        # Button to generate a solution of the board on screen:
        self._generate_solution_button = tk.Button(top, text="GENERATE SOLUTION",
                                                   command=self._generate_solution_command)
        # Button to return to main menu
        self._main_menu_button = tk.Button(top, text="MAIN MENU", command=self._main_menu_command)

        # Bind any key to the key handler method:
        top.bind('<Key>', self._key_handler)

        # Initial GUIBoard creation:
        self._gui_board = GUIBoard(top, Board(), None, bg="white",
                                   height=constants.BOARD_HEIGHT, width=constants.BOARD_WIDTH)
        self._gui_board.render_empty_board()

        # Pack initial necessary buttons to the window:
        self._solve_button.pack()
        self._pack_generate_buttons()

        # Start the Tkinter loop:
        top.mainloop()

    def _generate_command(self, max_remove=81):
        """
        Command that runs when the generate button is pressed
        :param max_remove: Integer: The maximum amount of numbers to remove from the board
        :return: None
        """
        # Set gs to the display state:
        self._gs = GUIState.DISPLAY_BOARD
        # Hide unnecessary buttons:
        self._solve_button.pack_forget()
        self._pack_forget_generate_buttons()
        # Generate the random board and render:
        self._gui_board.generate_random_board(max_remove)
        self._gui_board.render_values()
        # Pack the board and buttons onto window:
        self._gui_board.pack()
        self._generate_solution_button.pack()
        self._main_menu_button.pack()

    def _solve_command(self):
        """
        Command that runs when the solve button is pressed
        :return: None
        """
        # Set gs to the enter state:
        self._gs = GUIState.ENTER_BOARD
        # Hide unnecessary buttons:
        self._solve_button.pack_forget()
        self._pack_forget_generate_buttons()
        # Reset the board to empty, add a pointer, and render the pointer and values:
        self._gui_board.reset_board()
        self._gui_board.add_pointer()
        self._gui_board.render_pointer()
        self._gui_board.render_values()
        # Pack the board and buttons onto window:
        self._gui_board.pack()
        self._generate_solution_button.pack()
        self._main_menu_button.pack()

    def _generate_solution_command(self):
        """
        Command that runs when the generate solution button is pressed
        :return: None
        """
        # Try to solve the board:
        try:
            # Attempt to solve board:
            self._gui_board.solve_board()
            # Set gs to display state:
            self._gs = GUIState.DISPLAY_BOARD
            # Hide unnecessary button:
            self._generate_solution_button.pack_forget()
            # Remove the pointer and render the values:
            self._gui_board.remove_pointer()
            self._gui_board.render_values()
        # If the board is unsolvable:
        except ValueError:
            # Display message box showing the error and tell user to retry:
            messagebox.showerror("ERROR", "Given board is not solvable.\nCheck board and try again.")

    def _main_menu_command(self):
        """
        Command that runs when the main menu button is pressed
        :return: None
        """
        # Set gs to the menu state:
        self._gs = GUIState.MENU
        # Hide unnecessary buttons:
        self._gui_board.pack_forget()
        self._main_menu_button.pack_forget()
        self._generate_solution_button.pack_forget()
        # Remove the pointer:
        self._gui_board.remove_pointer()
        # Pack necessary buttons to window:
        self._solve_button.pack()
        self._pack_generate_buttons()

    def _key_handler(self, event):
        """
        Command that runs when a key is pressed
        :param event: Event: The key event triggered by the user pressing a key
        :return: None
        """
        # Only handle keys if the the state allows user to enter a board
        if self._gs == GUIState.ENTER_BOARD:
            # If the user tries to set a number:
            if event.char in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                # Try to set the value at the position of the pointer to the value of the key pressed
                try:
                    self._gui_board.set_pointer_val(int(event.char))
                # If it can't be placed, just print to the console telling user and do not place it
                except ValueError:
                    print("Not a valid number for this space")
            # If the user tries to backspace
            elif event.keysym == 'BackSpace':
                # Try to remove the value at the position of the pointer
                try:
                    self._gui_board.set_pointer_val(None)
                # If it can't be removed, print to the console telling user
                except ValueError:
                    print("Cannot remove this value")
            # If the user hit an arrow key, move the pointer accordingly with move_pointer method:
            elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
                self._gui_board.move_pointer(event.keysym)
            # Render the pointer and values to the GUIBoard:
            self._gui_board.render_pointer()
            self._gui_board.render_values()
            # Pack the board to the window
            self._gui_board.pack()

    def _pack_generate_buttons(self):
        """
        Easy way to pack all three generate buttons (1 for each difficulty)
        :return: None
        """
        # Pack all three generate buttons to the window:
        self._generate_easy_button.pack()
        self._generate_medium_button.pack()
        self._generate_hard_button.pack()

    def _pack_forget_generate_buttons(self):
        """
        Easy way to hide all three generate buttons (1 for each difficulty)
        :return: None
        """
        # Pack forget (hide) all three generate buttons:
        self._generate_easy_button.pack_forget()
        self._generate_medium_button.pack_forget()
        self._generate_hard_button.pack_forget()
