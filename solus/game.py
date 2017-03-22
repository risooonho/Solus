
import os
import pygame
from functions import *
from classes import *
from dicts import *
print('pygamed branch?')
player = create_player()
print("%s, %d, %d, %d") %(player.name, player.hp, player.attk, player.dfnc)
alien = Alien("Gloob", 2)
print("%s, %d, %d, %d") %(alien.name, alien.hp, alien.attk, alien.dfnc)
os.system('cls')

game = Game()

while game.is_running:
    while player.is_alive:
        encounter(player, alien)
        game.turns += 1
        quit_querry(game)
        if not game.is_running:
            break
