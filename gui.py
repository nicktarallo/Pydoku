import pygame
import constants
from game_state import GameState
from gui_button import GUIButton

pygame.init()


def game_loop():
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    state = GameState.Menu
    while running:
        screen.fill("white")
        events = pygame.event.get()
        if state == GameState.Menu:
            state = run_menu(state, screen, events)
        pygame.display.update()
        clock.tick(30)


def run_menu(state, screen, events):
    solve_button = GUIButton("Solve", constants.SOLVE_BUTTON_POS)
    gen_button = GUIButton("Generate", constants.GENERATE_BUTTON_POS)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if solve_button.is_clicked(event):
            state = GameState.EnterBoard
        if gen_button.is_clicked(event):
            state = GameState.DisplayBoard
    solve_button.display(screen)
    gen_button.display(screen)
    return state


game_loop()

pygame.quit()
