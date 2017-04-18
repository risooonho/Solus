"""Docstring for main."""
import os
import sys
import random
import pygame as pg
from resources.graphics import spritesheet


class Control(object):
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 30
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)

    def event_loop(self):
        self.events = pg.event.get()

        for event in self.events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.state.get_event(event)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_event(event)

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.state.update(self.screen, self.keys, self.current_time)


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
            img = img.convert()
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
