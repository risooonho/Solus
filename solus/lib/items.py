"""Docstring for classes."""
import pygame as pg
from tools import _Thing
import setup
import gui


class Item(_Thing):
    def __init__(self, name, *groups):
        super(Item, self).__init__(*groups)
        id_parent = self.id

        self.name = name
        self.picking_up = True

        id_parent = self.id
        self.id = 'item:' + id_parent

    def on_collide(self, player, world):
        if self.picking_up:
            self.picking_up = self.ask_pickup()
            if self.picking_up:
                self.pickup(player, world)

    def ask_pickup(self):
        return self.picking_up

    def pickup(self, *args):
        pass

    def place_in_inventory(self, player, world):
        player.inventory.append(self)
        msg = self.name + ' was added to your Inventory.'
        world.msgs.update_messages(msg)
        world.inventory.update(player.get_invtry_list())


class Equipment(Item):
    """This class handles all equipment, includes picking up."""

    def __init__(self, name, level, *groups):
        """init."""
        super(Equipment, self).__init__(name, *groups)
        self.level = level
        # groups include weapon, armor, useable, etc...
        self.modifier = {'attk': 0, 'dfnc': 0}
        self.is_equipped = False

        id_parent = self.id
        self.id = 'equipment:' + id_parent

    def equip(self, player, world):
        player.attk += self.modifier['attk']
        player.dfnc += self.modifier['dfnc']
        self.is_equipped = True
        world.inventory.update(player.get_invtry_list())
        world.stats.update(player.get_stat_list())


# Base class for weapon items, contains range and type
class Weapon(Equipment):
    """This class handles all weapons."""

    def __init__(self, name, level, attk_base, *groups):
        """init."""
        super(Weapon, self).__init__(name, level, *groups)
        self.modifier['attk'] = attk_base * level

        id_parent = self.id
        self.id = 'weapon:' + id_parent

# Class for knife items, contains attack attack bonus


class Knife(Weapon):
    """This class handles knife weapons."""

    def __init__(self, name, level, location, *groups):
        """init."""
        self.attk_base = 2
        super(Knife, self).__init__(name, level, self.attk_base, *groups)
        # sets attack bonus by multiplying by level attribute(Equipment class)

        self.image = setup.GFX['knife']
        self.attk_img = setup.GFX['swipe']
        self.attk_img.convert
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

        id_parent = self.id
        self.id = 'knife:' + id_parent

    def ask_pickup(self):
        return True

    def pickup(self, player, world):
        self.place_in_inventory(player, world)
        for item in player.inventory:
            if item.is_equipped:
                self.kill()
                return
        self.equip(player, world)
        self.kill()
