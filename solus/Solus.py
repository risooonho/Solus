"""Run the game."""
import pygame
from classes import Game

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    menu_items = ['Start', 'Quit']
    Game().title_screen(screen, menu_items)
