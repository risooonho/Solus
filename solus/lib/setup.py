"""Docstring for living classes."""
import os
import pygame as pg
from . import tools
from . import constants as c

GAME = 'BEGIN GAME'
ORIGINAL_CAPTION = 'Solus'
pg.init()
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)

SCREEN_RECT = SCREEN.get_rect
GFX = tools.load_all_gfx(os.path.join('resources', 'graphics'))
TMX = tools.load_all_tmx(os.path.join('resources', 'tmx'))
FONTS = tools.load_all_fonts(os.path.join('resources', 'fonts'))

FNT = {40: pg.font.Font(FONTS['s_font'], 40),
       20: pg.font.Font(FONTS['s_font'], 20),
       10: pg.font.Font(FONTS['s_font'], 10),
       12: pg.font.Font(FONTS['s_font'], 12)}
