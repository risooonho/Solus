"""Docstring for living classes."""
import constants as c
import setup
import pygame as pg
from tools import _Thing
from items import Knife


class Living(_Thing):
    """This class is the foundation for living things."""

    def __init__(self, name, hp, *groups):
        """init."""
        super(Living, self).__init__(*groups)
        self.hp = hp
        self.name = name
        self.spd = 10

        id_parent = self.id
        self.id = 'living:' + id_parent

    def on_collide(self):
        pass


class Character(Living):
    """This class is the foundation for all characters."""

    def __init__(self, name, level, type, *groups):
        """init."""
        # this sets the stats based on CHR_LEVEL dict in dicts.py
        lvl = (100, 10, 10)
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

    def load_img_vectors(self, img):
        img_vectors = {}
        keys = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']

        for index, key in enumerate(keys):
            img_v = pg.transform.rotate(img, 45 * index)
            img_vectors[key] = img_v
        return img_vectors


class Player(Character):
    """This class handles the player object."""

    def __init__(self, name, level, location, *groups):
        """init."""
        super(Player, self).__init__(name, level, 'player', *groups)
        self.base_img = setup.GFX['player']
        self.imgs = self.load_img_vectors(self.base_img)
        self.image = self.imgs['N']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.direction = 0

        self.stat_list = self.get_stat_list()
        self.inventory_list = []

        id_parent = self.id
        self.id = 'player:' + id_parent

    def get_stat_list(self):
        stat_list = ['HP: ' + str(self.hp),
                     'ATTK: ' + str(self.attk),
                     'DFNC: ' + str(self.dfnc)]
        return stat_list

    def get_invtry_list(self):
        self.inventory_list = []
        for index, item in enumerate(self.inventory):
            name = item.name
            if item.is_equipped:
                name += ' - E'
            self.inventory_list.append(name)
        return self.inventory_list

    def update(self, dt, game):
        """Update player object, handle movement, blockers, and viewport."""
        new = self.rect.copy()
        diag = False
        key = pg.key.get_pressed()
        if key[pg.K_d] and key[pg.K_w]:
            if not self.direction == 7:
                self.image = self.imgs['NE']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 7
            self.rect.x += self.spd * .707
            self.rect.y -= self.spd * .707
            diag = True
        if key[pg.K_a] and key[pg.K_w]:
            if not self.direction == 1:
                self.image = self.imgs['NW']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 1
            self.rect.x -= self.spd * .707
            self.rect.y -= self.spd * .707
            diag = True
        if key[pg.K_d] and key[pg.K_s]:
            if not self.direction == 5:
                self.image = self.imgs['SE']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 5
            self.rect.x += self.spd * .707
            self.rect.y += self.spd * .707
            diag = True
        if key[pg.K_a] and key[pg.K_s]:
            if not self.direction == 3:
                self.image = self.imgs['SW']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 3
            self.rect.x -= self.spd * .707
            self.rect.y += self.spd * .707
            diag = True
        if key[pg.K_d] and not diag:
            if not self.direction == 6:
                self.image = self.imgs['E']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 6
            self.rect.x += self.spd
        if key[pg.K_a] and not diag:
            if not self.direction == 2:
                self.image = self.imgs['W']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 2
            self.rect.x -= self.spd
        if key[pg.K_w] and not diag:
            if not self.direction == 0:
                self.image = self.imgs['N']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 0
            self.rect.y -= self.spd
        if key[pg.K_s] and not diag:
            if not self.direction == 4:
                self.image = self.imgs['S']
                self.rect = self.image.get_rect()
                self.rect.center = new.center
                self.direction = 4
            self.rect.y += self.spd

        game.tilemap.set_focus(new.x, new.y)

    def attack(self, surface):
        for item in self.inventory:
            if 'weapon' in item.id:
                if item.is_equipped:
                    self.image = item.attk_img
                    self.direction = 8


class Enemy(Character):
    """This class hancles enemy objects."""

    def __init__(self, name, level, location, *groups):
        """init."""
        super(Enemy, self).__init__(name, level, 'enemy', *groups)
        if level == 1:
            self.image = setup.GFX['pincher']
        elif level == 2:
            self.image = setup.GFX['grabber']
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.spd = self.spd / 4

        id_parent = self.id
        self.id = 'enemy:' + id_parent
        self.i = 0

    def encounter(self, player, world):
        print self.name
        print player.name
        player.hp -= self.attk
        self.kill()
        msg = 'You killed ' + self.name + '.'
        world.msgs.update_messages(msg)
        world.stats.update(player.get_stat_list())

    def update(self, dt, game):
        pass
