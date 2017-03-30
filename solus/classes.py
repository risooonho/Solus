import dicts
import pygame
from functions import encounter
from map import tmx

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        self.tilemap = tmx.load('map/world.tmx', screen.get_size())

        self.player_s = tmx.SpriteLayer()
        self.enemy_s = tmx.SpriteLayer()
        self.item_s = tmx.SpriteLayer()

        plyr_strt = self.tilemap.layers['triggers'].find('player')[0]
        enemy_strt = self.tilemap.layers['triggers'].find('enemy')[0]

        self.player = Player('Andre', 3, (plyr_strt.px, plyr_strt.py), self.player_s)
        self.enemy = Enemy('Gloob', 1, (enemy_strt.px, enemy_strt.py), self.enemy_s)

        self.tilemap.layers.append(self.player_s)
        self.tilemap.layers.append(self.enemy_s)

        while 1:
            #restrain to 30fps
            dt = clock.tick(30)
            #event handling
            for event in pygame.event.get():
                #distinct key events
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            #continuous key events

            #drawing
            self.tilemap.update(dt / 1000., self)
            screen.fill((200, 200, 200))
            self.tilemap.draw(screen)
            #after drawing everything, flip()
            pygame.display.flip()

#Most basic object (atm), contains location attribute
class Thing(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Thing, self).__init__(*groups)
        self.id = 'thing'

#Base for any living thing contains health and name
class Living(Thing):

    def __init__(self, name, hp, *groups):
        super(Living, self).__init__(*groups)
        self.hp = hp
        self.name = name

        id_parent = self.id
        self.id = 'living:' + id_parent

#Base for any character, contains attack and defense stats, is_alive bool
# inventory and equipped lists
class Character(Living):

    def __init__(self, name, level, type, *groups):

        #this sets the stats based on CHR_LEVEL dict in dicts.py
        lvl = dicts.CHR_LEVEL[level]
        hp = lvl[0]
        attk = lvl[1]
        dfnc = lvl[2]

        super(Character, self).__init__(name, hp, *groups)
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

    def __init__(self, name, level, location, *groups):

        super(Player, self).__init__(name, level, 'player', *groups)

        self.ss = spritesheet('imgs/playerSS.png')
        self.sstrip = self.ss.load_strip((0,0,16,16), 8, (255,255,255))

        self.img_N, self.img_S, self.img_E, self.img_W = self.sstrip[:4]
        self.img_NE, self.img_SE, self.img_NW, self.img_SW = self.sstrip[4:]

        self.image = self.img_N
        self.rect = pygame.Rect(location, self.image.get_size())

        id_parent = self.id
        self.id = 'player:' + id_parent

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.img_E
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.img_W
        if key[pygame.K_UP]:
            self.rect.y -= 300 * dt
            self.image = self.img_N
            if key[pygame.K_RIGHT]:
                self.image = self.img_NE
            if key[pygame.K_LEFT]:
                self.image = self.img_NW
        if key[pygame.K_DOWN]:
            self.rect.y += 300 * dt
            self.image = self.img_S
            if key[pygame.K_RIGHT]:
                self.image = self.img_SE
            if key[pygame.K_LEFT]:
                self.image = self.img_SW

        new = self.rect
        for cell in game.tilemap.layers['triggers'].collide(new, 'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                new.bottom = cell.top
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom

        B = pygame.sprite.spritecollideany(self, game.enemy_s)
        if B and B.is_alive:
            encounter(self, B)

        game.tilemap.set_focus(new.x, new.y)

#Base class for player creation holds ... can just
#use character object with attributes of hostile?
class Enemy(Character):

    def __init__(self, name, level, location, *groups):

        super(Enemy, self).__init__(name, level, 'enemy', *groups)

        self.image = pygame.image.load('imgs/enemy.png')
        self.image.convert()
        self.rect = pygame.Rect(location, self.image.get_size())

        id_parent = self.id
        self.id = 'enemy:' + id_parent
        self.i = 0

    def update(self, dt, game):

        if self.rect.colliderect(game.player.rect):
            encounter(game.player, self)


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
