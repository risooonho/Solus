"""Run the game."""
import sys
import pygame as pg
from lib import setup
from lib.main import main

if __name__ == '__main__':
    setup.GAME
    main()
    pg.quit()
    sys.exit
