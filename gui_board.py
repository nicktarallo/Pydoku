import constants
import pygame
from position import Position
from gui_number import GUINumber


class GUIBoard:
    def __init__(self, board, pos):
        self.board = board
        self.x, self.y = pos
        self.surf = pygame.Surface((constants.SCREEN_HEIGHT, constants.SCREEN_HEIGHT))
        self.render_empty_board()
        self.add_values()

    def render_empty_board(self):
        self.surf.fill("white")
        pygame.draw.line(self.surf, "black", (0, 0), (0, constants.SCREEN_HEIGHT), 7)
        pygame.draw.line(self.surf, "black",
                         (0, constants.SCREEN_HEIGHT), (constants.SCREEN_HEIGHT, constants.SCREEN_HEIGHT), 7)
        pygame.draw.line(self.surf, "black",
                         (constants.SCREEN_HEIGHT, constants.SCREEN_HEIGHT), (constants.SCREEN_HEIGHT, 0), 7)
        pygame.draw.line(self.surf, "black", (constants.SCREEN_HEIGHT, 0), (0, 0), 7)
        pos = constants.SCREEN_HEIGHT // 9
        for i in range(8):
            width = 7 if i == 2 or i == 5 else 2
            pygame.draw.line(self.surf, "black", (0, pos), (constants.SCREEN_HEIGHT, pos), width)
            pygame.draw.line(self.surf, "black", (pos, 0), (pos, constants.SCREEN_HEIGHT), width)
            pos += constants.SCREEN_HEIGHT // 9

    def add_values(self):
        y = constants.SCREEN_HEIGHT // 18
        for i in range(9):
            x = constants.SCREEN_HEIGHT // 18
            for j in range(9):
                val = self.board.get_val(Position(i, j))
                if val:
                    gui_num = GUINumber(str(val), (x, y))
                    gui_num.display(self.surf)
                x += constants.SCREEN_HEIGHT // 9
            y += constants.SCREEN_HEIGHT // 9

    def display(self, screen):
        screen.blit(self.surf, (self.x, self.y))


