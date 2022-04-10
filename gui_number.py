import constants


class GUINumber:
    def __init__(self, val, pos):
        self.val = val
        self.x, self.y = pos
        self.text_color = "black"
        self.rendered = None
        self.size = None
        self.render_text()

    def render_text(self):
        self.rendered = constants.FONT.render(self.val, True, self.text_color)
        self.size = constants.FONT.size(self.val)

    def display(self, screen):
        x = self.x - (self.size[0] // 2)
        y = self.y - (self.size[1] // 2)
        screen.blit(self.rendered, (x, y))
