"""Docstring for living classes."""
import functions as fn
from dicts import CHR_LEVEL, CLR, FNT, TXT
import sys
import os
import pygame as pg
import random as rd


def res_path(relative):
    """Return required path if run from .exe made with pyinstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class Thing(pg.sprite.Sprite):
    """This class is the most basic object in the game."""

    def __init__(self, *groups):
        """init."""
        super(Thing, self).__init__(*groups)
        self.id = 'thing'


class Living(Thing):
    """This class is the foundation for living things."""

    def __init__(self, name, hp, *groups):
        """init."""
        super(Living, self).__init__(*groups)
        self.hp = hp
        self.name = name
        self.spd = 10

        id_parent = self.id
        self.id = 'living:' + id_parent


class Character(Living):
    """This class is the foundation for all characters."""

    def __init__(self, name, level, type, *groups):
        """init."""
        # this sets the stats based on CHR_LEVEL dict in dicts.py
        lvl = CHR_LEVEL[level]
        hp = lvl[0]

        super(Character, self).__init__(name, hp, *groups)
        self.type = type
        self.is_alive = True

        self.attk = lvl[1]
        self.dfnc = lvl[2]

        # holds character inventory, possible to add multiples of items?
        self.inventory = []

        id_parent = self.id
        self.id = 'character:' + id_parent


class Player(Character):
    """This class handles the player object."""

    def __init__(self, name, level, location, *groups):
        """init."""
        super(Player, self).__init__(name, level, 'player', *groups)
        ssheet = 'resources\\playerSS.png'
        ssheet = res_path(ssheet)
        self.ss = spritesheet(ssheet)
        self.sstrip = self.ss.load_strip((0, 0, 16, 16), 8, (255, 255, 255))

        self.img_N, self.img_S, self.img_E, self.img_W = self.sstrip[:4]
        self.img_NE, self.img_SE, self.img_NW, self.img_SW = self.sstrip[4:]

        self.image = self.img_N
        self.rect = pg.Rect(location, self.image.get_size())

        id_parent = self.id
        self.id = 'player:' + id_parent

    def update_stats(self):
        """Update player stat text attributes for blitting."""
        self.hp_t = FNT['sml'].render('    HP: ' + str(self.hp), 1, CLR['blk'])
        self.attk_t = FNT['sml'].render('ATTK: ' +
                                        str(self.attk), 1, CLR['blk'])
        self.dfnc_t = FNT['sml'].render('DFNC: ' +
                                        str(self.dfnc), 1, CLR['blk'])

    def blit_inventory(self, game):
        inventory = FNT['smlx'].render('Inventory:', 1, CLR['blk'])
        game.screen.blit(inventory, (320, 55))
        for index, item in enumerate(self.inventory):
            name = item.name
            if item.is_equipped:
                name += ' - E'
            name_t = FNT['sml'].render(name, 1, CLR['blk'])
            game.screen.blit(name_t, (320, 70 + (index * 11)))

    def update(self, dt, game):
        """Update player object, handle movement, blockers, and viewport."""
        last = self.rect.copy()
        diag = False
        key = pg.key.get_pressed()
        if key[pg.K_RIGHT] and key[pg.K_UP]:
            self.rect.x += self.spd * .707
            self.rect.y -= self.spd * .707
            self.image = self.img_NE
            diag = True
        if key[pg.K_LEFT] and key[pg.K_UP]:
            self.rect.x -= self.spd * .707
            self.rect.y -= self.spd * .707
            self.image = self.img_NW
            diag = True
        if key[pg.K_RIGHT] and key[pg.K_DOWN]:
            self.rect.x += self.spd * .707
            self.rect.y += self.spd * .707
            self.image = self.img_SE
            diag = True
        if key[pg.K_LEFT] and key[pg.K_DOWN]:
            self.rect.x -= self.spd * .707
            self.rect.y += self.spd * .707
            self.image = self.img_SW
            diag = True
        if key[pg.K_RIGHT] and not diag:
            self.rect.x += self.spd
            self.image = self.img_E
        if key[pg.K_LEFT] and not diag:
            self.rect.x -= self.spd
            self.image = self.img_W
        if key[pg.K_UP] and not diag:
            self.rect.y -= self.spd
            self.image = self.img_N
        if key[pg.K_DOWN] and not diag:
            self.rect.y += self.spd
            self.image = self.img_S

        new = self.rect
        for cell in game.tilemap.layers['triggers'].collide(new, 'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and last.right <= cell.left and \
                    new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and \
                    new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and \
                    new.bottom > cell.top:
                new.bottom = cell.top
            if 'b' in blockers and last.top >= cell.bottom and \
                    new.top < cell.bottom:
                new.top = cell.bottom

        game.tilemap.set_focus(new.x, new.y)


class Enemy(Character):
    """This class hancles enemy objects."""

    def __init__(self, name, level, location, *groups):
        """init."""
        super(Enemy, self).__init__(name, level, 'enemy', *groups)
        img = 'resources\\enemy.png'
        img = res_path(img)
        self.image = pg.image.load(img)
        self.image.convert()
        self.rect = pg.Rect(location, self.image.get_size())
        self.level_txt = FNT['sml'].render(str(level), 1, (255, 255, 255))
        self.spd = self.spd / 4
        self.image.blit(self.level_txt, (5, 5))

        id_parent = self.id
        self.id = 'enemy:' + id_parent
        self.i = 0

    def update(self, dt, game):
        """Update enemy object, move toward player, check for collides."""
        if self.rect.colliderect(game.player.rect):
            if self.is_alive and game.player.is_alive:
                fn.encounter(game.player, self)
                if not self.is_alive:
                    game.update_msgs('You killed ' + self.name)
                    game.player.update_stats()
