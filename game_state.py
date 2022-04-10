import enum


class GameState(enum.Enum):
    Menu = 1
    DisplayBoard = 2
    EnterBoard = 3
    Generate = 4
    Solve = 5
