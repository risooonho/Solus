"""
This is the base class for all level states.

(i.e. states where the player can move around the screen).
Levels are differentiated by self.name and self.tmx_map.
This class inherits from the generic state class
found in the tools.py module.
"""

import pygame as pg
import random as rd
from .. import constants as c
from .. import living as liv
from .. import items as itm
from .. import tools, setup
from resources.tmx import tmx
from lib.gui import TextList, SlideGroup
from .. import collision


class World(tools._State):
    """World state is the mmain game state."""

    def __init__(self):
        """Init World by setting name and map path."""
        super(World, self).__init__()
        self.next = c.MAIN_MENU
        self.name = c.WORLD
        self.tmx_map = setup.TMX[self.name]

    def startup(self, current_time, game_data):
        """Call when the State object is flipped to."""
        self.game_data = game_data
        self.current_time = current_time
        self.state = "transition_in"
        self.tilemap = tmx.load(self.tmx_map, c.SCREEN_SIZE)

        self.make_sprite_groups()
        self.player = self.make_player()
        self.make_enemies()
        self.make_items()
        self.make_GUI()

        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.enemy_s,
                                                            self.item_s,
                                                            self)

        self.state_dict = self.make_state_dict()
        self.transition_rect = setup.SCREEN.get_rect()
        self.transition_alpha = 255

    def update(self, surface, keys, current_time):
        self.surface = surface
        state_function = self.state_dict[self.state]
        state_function(surface, keys, current_time)

    def running_normally(self, surface, keys, current_time):

        self.tilemap.update(30, self)
        view = self.player.rect.center
        self.tilemap.set_focus(view[0], view[1])
        self.collision_handler.update(self, keys)
        self.draw_world(surface, current_time)

    def draw_world(self, surface, current_time):
        surface.fill(c.WHITE)
        self.tilemap.draw(surface)
        self.gui_s.draw(surface)

    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                pass
            if event.key == pg.K_SPACE:
                print 'space'
                self.player.attack(self.surface)
            if event.key == pg.K_ESCAPE:
                self.done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if event.button == 4:
                if self.inventory.rect.collidepoint(pos):
                    print 'scrollingup'
            if event.button == 5:
                if self.inventory.rect.collidepoint(pos):
                    print 'scrollingdn'
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if event.button == 1:
                if self.inventory.rect.collidepoint(pos):
                    print 'clicked'

    def make_sprite_groups(self):

        self.enemy_s = tmx.SpriteLayer()
        self.item_s = tmx.SpriteLayer()
        self.player_s = tmx.SpriteLayer()

        self.tilemap.layers.append(self.enemy_s)
        self.tilemap.layers.append(self.item_s)
        self.tilemap.layers.append(self.player_s)

    def make_player(self):
        loc = self.tilemap.layers['triggers'].find('player')[0]
        player = liv.Player('Andre', 3, (loc.px, loc.py), self.player_s)
        return player

    def make_enemies(self):
        num = rd.randint(3, 8)
        for i in range(num):
            x = rd.randint(32, 1350)
            y = rd.randint(32, 1350)
            level = rd.randint(1, 2)
            enemy = liv.Enemy('Enemy ' + str(i + 1), level, (x, y),
                              self.enemy_s)

    def make_items(self):

        self.knife = itm.Knife('Knife', 1, (50, 1300), self.item_s)
        # self.knife = itm.Knife('Knife2', 1, (70, 1300), self.item_s)
        # self.knife = itm.Knife('Knife3', 1, (90, 1300), self.item_s)
        # self.knife = itm.Knife('Knife4', 1, (110, 1300), self.item_s)
        # self.knife = itm.Knife('Knife', 1, (50, 1340), self.item_s)
        # self.knife = itm.Knife('Knife2', 1, (70, 1340), self.item_s)
        # self.knife = itm.Knife('Knife3', 1, (90, 1340), self.item_s)
        # self.knife = itm.Knife('Knife4', 1, (110, 1340), self.item_s)

    def make_state_dict(self):
        """
        Make a dictionary of states the level can be in.
        """
        state_dict = {'normal': self.running_normally,
                      #'dialogue': self.handling_dialogue,
                      #'menu': self.goto_menu,
                      'transition_in': self.transition_in,
                      'transition_out': self.transition_out,
                      #'slow transition out': self.slow_fade_out
                      }
        return state_dict

    def transition_in(self, surface, *args):
        self.state = 'normal'

    def transition_out(self, surface, *args):
        self.done = True

    def make_GUI(self):
        self.gui_s = pg.sprite.Group()
        msgs = ['Welcome to Solus, WASD to move.', 'Find something to fight']
        self.msgs = TextList('Messages:', msgs,
                             20, c.BLACK, (32, 4), self.gui_s)
        self.stats = TextList('Stats:', self.player.stat_list,
                              20, c.BLACK, (495, 4), self.gui_s)
        inventory_list = TextList('Inventory:', self.player.get_invtry_list(),
                                  20, c.WHITE, (495, 4))
        self.inventory = SlideGroup((580, 200), inventory_list, self.gui_s)

    def get_mouse(self, pos):
        if self.inventory.rect.collidepoint(pos):
            self.inventory.slide_group(pos, 1)
        else:
            self.inventory.slide_group(pos, 0)
