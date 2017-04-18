"""Docstring for dicts."""
import pygame
import sys
import os

SCREEN_SIZE = (600, 480)

BLACK = (0, 0, 0)
NEAR_BLACK = (1, 0, 0)
WHITE = (255, 255, 255)
BLACK_BLUE = (19, 15, 48)
NEAR_BLACK_BLUE = (20, 15, 48)
LIGHT_BLUE = (0, 153, 204)
DARK_RED = (118, 27, 12)
REALLY_DARK_RED = (15, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (208, 32, 144)
TRANSITION_COLOR = BLACK_BLUE

MAIN_MENU = 'main menu'

#
# pygame.init()
#
#
# def res_path(relative):
#     """Return required path if run from .exe made with pyinstaller."""
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative)
#     return os.path.join(relative)
#
#
# font = 'resources\\s_font.ttf'
# font = res_path(font)
#
# # Dictionary used in character creation Level:(hp, attack, defence)
# CHR_LEVEL = {3: (100, 10, 10), 2: (50, 5, 5), 1: (10, 1, 1)}
#
# PROMPTS = {'create player': 'Enter your name: ',
#            'choose difficulty': 'Choose a difficulty.\n3 - Easy\n2 - '
#            'Medium\n1 - Hard\n>>>'}
#
# CLR = {'wht': (255, 255, 255),
#        'blk': (0, 0, 0)}
#
# FNT = {'lrg': pygame.font.Font(res_path(font), 40),
#        'med': pygame.font.Font(font, 20),
#        'sml': pygame.font.Font(font, 10),
#        'smlx': pygame.font.Font(font, 12)}
#
# TXT = {'YES': FNT['smlx'].render('YES', 1, CLR['wht']),
#        'NO': FNT['smlx'].render('NO', 1, CLR['wht']),
#        'yes': FNT['sml'].render('yes', 1, CLR['blk']),
#        'no': FNT['sml'].render('no', 1, CLR['blk'])}
