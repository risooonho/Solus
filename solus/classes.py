import dicts

class Game(object):
    def __init__(self):
        self.is_running = True
        self.turns = 0

#Most basic object (atm), contains location attribute
class Thing(object):

    location = [0,0,0]
    id = 'thing'

#Base for any living thing contains health and name
class Living(Thing):

    def __init__(self, name, hp):
        self.hp = hp
        self.name = name

        id_parent = self.id
        self.id = 'living:' + id_parent

#Base for any character, contains attack and defense stats, is_alive bool
# inventory and equipped lists
class Character(Living):

    def __init__(self, name, level, type):

        #this sets the stats based on CHR_LEVEL dict in dicts.py
        lvl = dicts.CHR_LEVEL[level]
        hp = lvl[0]
        attk = lvl[1]
        dfnc = lvl[2]

        super(Character, self).__init__(name, hp)
        self.type = type
        self.is_alive = True
        self.attk = attk
        self.dfnc = dfnc
        #holds character inventory, possible to add multiples of items?
        self.inventory = []

        id_parent = self.id
        self.id = 'character:' + id_parent

#Base class for player creation holds ...
class Player(Character):

    def __init__(self, name, level):

        super(Player, self).__init__(name, level, 'player')

        id_parent = self.id
        self.id = 'player:' + id_parent

#Base class for player creation holds ... can just
#use character object with attributes of hostile?
class Alien(Character):

    def __init__(self, name, level):

        super(Alien, self).__init__(name, level, 'alien')

        id_parent = self.id
        self.id = 'alien:' + id_parent

#Base class for equipment items, contains level, group, name attributes
class Equipment(Thing):

    def __init__(self, group, name, level):
        #level of equipment, modifies main bonuses
        self.level = level
        #groups include weapon, armor, useable, etc...
        self.group = group
        self.name = name
        self.is_equipped = False

        id_parent = self.id
        self.id = 'equipment:' + id_parent

#Base class for weapon items, contains range and type
class Weapon(Equipment):

    def __init__(self, type, name, wep_range, level):
        super(Weapon, self).__init__('weapon', name, level)
        #controlls how far away you can attack from
        self.wep_range = wep_range
        #hold info about type, melee, ranged, etc...
        self.type = type

        id_parent = self.id
        self.id = 'weapon:' + id_parent

#Class for knife items, contains attack attack bonus
class Knife(Weapon):

    def __init__(self, name, level):
        super(Knife, self).__init__('melee', name, 1, level)
        #sets attack bonus by multiplying by level attribute(Equipment class)
        self.attk_bonus = 2 * self.level

        id_parent = self.id
        self.id = 'knife:' + id_parent
