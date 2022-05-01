import enum


class GameState(enum.Enum):
    """Represents the possible states that the application could be in (Menu, DisplayBoard, EnterBoard)"""
    Menu = 1
    DisplayBoard = 2
    EnterBoard = 3
