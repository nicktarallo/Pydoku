import pygame
import constants
from game_state import GameState
from gui_button import GUIButton
from gui_board import GUIBoard
from board import Board

pygame.init()


def game_loop():
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    state = GameState.Menu
    board_to_display = None
    while running:
        screen.fill("white")
        events = pygame.event.get()
        if state == GameState.Menu:
            state, running = run_menu(state, screen, events)
        if state == GameState.Generate:
            state, board_to_display = generate_board()
        if state == GameState.DisplayBoard:
            state, running = display_board(screen, events, board_to_display)

        pygame.display.update()
        clock.tick(30)


def run_menu(state, screen, events):
    running = True
    solve_button = GUIButton("Solve", constants.SOLVE_BUTTON_POS)
    gen_button = GUIButton("Generate", constants.GENERATE_BUTTON_POS)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if solve_button.is_clicked(event):
            state = GameState.EnterBoard
        if gen_button.is_clicked(event):
            state = GameState.Generate
    solve_button.display(screen)
    gen_button.display(screen)
    return state, running


def display_board(screen, events, board):
    running = True
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    gui_board = GUIBoard(board, (0, 0))
    gui_board.display(screen)
    return GameState.DisplayBoard, running


def generate_board():
    return GameState.DisplayBoard, Board.generate_board()


game_loop()

pygame.quit()
