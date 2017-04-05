
import os
import pygame
from functions import *
from classes import *
from dicts import *

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    menu_items = ['Start', 'Quit']
    Game().title_screen(screen, menu_items)
