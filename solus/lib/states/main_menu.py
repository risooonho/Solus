import pygame as pg
from .. import constants as c
from .. import tools, setup
from lib.gui.button import Button


class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()
        self.next = 'world'
        self.name = c.MAIN_MENU
        self.startup(0, 0)

    def startup(self, *args):
        self.title = setup.FNT[40].render('Solus', 0, c.WHITE)
        self.button_s = pg.sprite.Group()
        start_button = Button((100, 100), 'Start', self.button_s)
        self.button_s.add(start_button)

    def update(self, surface, keys, *args):
        self.draw_menu(surface)

    def draw_menu(self, surface):
        surface.blit(self.title, (10, 10))
        self.button_s.draw(surface)

    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                pass
