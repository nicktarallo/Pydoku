import pygame
import constants


class GUIButton:
    def __init__(self, text, pos, text_color="black", bg="white", outline="black"):
        self.text = text
        self.x, self.y = pos[0], pos[1]
        self.bg = bg
        self.outline = outline
        self.text_color = text_color
        self.rendered = None
        self.rect = None
        self.size = None
        self.render_text()

    def render_text(self):
        self.rendered = constants.FONT.render(self.text, True, self.text_color)
        self.rect = self.rendered.get_rect(center=(self.x, self.y))
        self.size = constants.FONT.size(self.text)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True

    def display(self, screen):
        x = self.x - (self.size[0] // 2)
        y = self.y - (self.size[1] // 2)
        screen.blit(self.rendered, (x, y))



