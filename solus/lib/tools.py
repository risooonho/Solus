"""This module houses the main engine."""

import os
import sys
import pygame as pg
from resources.graphics import spritesheet


class Control(object):
    """
    Control class for entire project.

    Contains the game loop, and contains the event_loop
    which passes events to States as needed.
    Logic for flipping states is also found here.
    """

    def __init__(self, caption):
        """Create Control object with game caption."""
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 30
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        """Load state dict when called from main.py."""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def main(self):
        """Main loop for entire program."""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

    def event_loop(self):
        """Pass events to current state."""
        self.events = pg.event.get()

        for event in self.events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEMOTION:
                break
            elif event.type == pg.ACTIVEEVENT:
                break
            self.state.get_event(event)
        self.state.get_mouse(pg.mouse.get_pos())

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(self.current_time, persist)


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game_data = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.game_data

    def update(self, surface, keys, current_time):
        pass


def load_all_gfx(directory, accept=('.png')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            if hasattr(sys, '_MEIPASS'):
                directory = os.path.join(sys._MEIPASS, directory)
            img = pg.image.load(os.path.join(directory, pic))
            img = img.convert_alpha()
            if '_SS' in name:
                ss = spritesheet.spritesheet(os.path.join(directory, pic))
                sstrip = ss.load_strip((0, 0, 16, 16), 8, (255, 255, 255))
                img = sstrip
            graphics[name] = img
    return graphics


def load_all_tmx(directory, accept=('.tmx')):
    tmx = {}
    for item in os.listdir(directory):
        name, ext = os.path.splitext(item)
        if ext.lower() in accept:
            if hasattr(sys, '_MEIPASS'):
                directory = os.path.join(sys._MEIPASS, directory)
            tmx[name] = os.path.join(directory, item)
    return tmx


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_tmx(directory, accept)


class _Thing(pg.sprite.Sprite):
    """This class is the most basic object in the game."""

    def __init__(self, *groups):
        """init."""
        super(_Thing, self).__init__(*groups)
        self.id = 'thing'
