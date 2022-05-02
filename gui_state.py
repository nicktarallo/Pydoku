import enum


class GUIState(enum.Enum):
    """Represents the possible states that the application could be in (Menu, DisplayBoard, EnterBoard)"""
    Menu = 1  # GUI is on main menu
    DisplayBoard = 2  # GUI is displaying a board to the user
    EnterBoard = 3  # GUI is letting user enter a board
