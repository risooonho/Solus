"""Docstring for dicts."""
import pygame
import sys
import os
pygame.init()


def res_path(relative):
    """Return required path if run from .exe made with pyinstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


font = 'data\\s_font.ttf'
font = res_path(font)

# Dictionary used in character creation Level:(hp, attack, defence)
CHR_LEVEL = {3: (100, 10, 10), 2: (50, 5, 5), 1: (10, 1, 1)}

PROMPTS = {'create player': 'Enter your name: ',
           'choose difficulty': 'Choose a difficulty.\n3 - Easy\n2 - '
           'Medium\n1 - Hard\n>>>'}

CLR = {'wht': (255, 255, 255),
       'blk': (0, 0, 0)}

FNT = {'lrg': pygame.font.Font(res_path(font), 40),
       'med': pygame.font.Font(font, 20),
       'sml': pygame.font.Font(font, 10),
       'smlx': pygame.font.Font(font, 12)}

TXT = {'YES': FNT['smlx'].render('YES', 1, CLR['wht']),
       'NO': FNT['smlx'].render('NO', 1, CLR['wht']),
       'yes': FNT['sml'].render('yes', 1, CLR['blk']),
       'no': FNT['sml'].render('no', 1, CLR['blk'])}
