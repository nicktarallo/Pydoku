import enum


class GUIState(enum.Enum):
    """Represents the possible states that the application could be in (MENU, DISPLAY_BOARD, ENTER_BOARD)"""
    MENU = 0  # GUI is on main menu
    DISPLAY_BOARD = 1  # GUI is displaying a board to the user
    ENTER_BOARD = 2  # GUI is letting user enter a board
