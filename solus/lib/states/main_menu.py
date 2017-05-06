import pygame as pg
from .. import constants as c
from .. import tools, setup
from lib.gui import Button, Text


def start_game(state):
    state.done = True


def quit_game(state):
    state.quit = True


class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()
        self.next = c.WORLD
        self.name = c.MAIN_MENU
        self.startup(0, 0)

    def startup(self, *args):
        # self.title = setup.FNT[100].render('Solus', 1, c.WHITE)
        self.make_GUI()

    def update(self, surface, *args):
        self.draw_menu(surface)

    def draw_menu(self, surface):
        surface.fill((0, 0, 0))
        # surface.blit(self.title, (10, 10))
        self.gui_s.draw(surface)

    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                start_game(self)
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in self.button_s:
                if button.rect.collidepoint(pos):
                    button.click()
        if event.type == pg.MOUSEBUTTONUP:
            pos = event.pos
            for button in self.button_s:
                if button.rect.collidepoint(pos):
                    button.clicked(self)
                else:
                    button.draw_button(button.name)

    def make_GUI(self):
        self.gui_s = pg.sprite.Group()
        self.text_s = pg.sprite.Group()
        self.button_s = pg.sprite.Group()
        title = Text('Solus', (10, 10), 100, c.WHITE,
                     self.text_s, self.gui_s)
        start_button = Button((100, 100), 'Start', start_game,
                              self.button_s, self.gui_s)
        quit_button = Button((100, 200), 'Quit', quit_game,
                             self.button_s, self.gui_s)

    def get_mouse(self, pos):
        pass
