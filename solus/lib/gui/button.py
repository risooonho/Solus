import pygame as pg
from gui import Widget
from .. import setup
from lib import constants as c


class Button(Widget):
    def __init__(self, location, label, *groups):
        super(Button, self).__init__(location, *groups)
        self.name = label
        self.state = 0
        self.image = self.draw_button(self.name, self.state)

    def draw_button(self, label, state):
        txt = setup.FNT[20].render(label, 1, c.WHITE)
        t_w, t_h = txt.get_size()
        t_w_c = t_w // 2
        t_h_c = t_h // 2
        t_w_d = t_w * 2
        t_h_d = t_h * 2
        self.image = pg.Surface((t_w_d, t_h_d))
        self.image.fill((100, 100, 100))
        self.image.blit(txt, (t_w_c, t_h_c))

        return self.image
