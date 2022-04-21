import pygame

pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
BOARD_WIDTH = 500
BOARD_HEIGHT = 500
VALUE_TAG = "value"
BOARD_TAG = "board"
POINTER_TAG = "pointer"
FONT = pygame.font.SysFont("Arial", 40)

SOLVE_BUTTON_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
GENERATE_BUTTON_POS = (SCREEN_WIDTH // 2, (2 * SCREEN_HEIGHT) // 3)