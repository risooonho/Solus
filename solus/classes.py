"""Docstring for classes."""
import functions as fn
from dicts import CHR_LEVEL, CLR, FNT, TXT
from data import tmx
import sys
import os
import pygame as pg
import random as rd


def res_path(relative):
    """Return required path if run from .exe made with pyinstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class spritesheet(object):
    """This class handles sprite sheets.

    This was taken from www.scriptefun.com/transcript-2-using
    sprite-sheets-and-drawing-the-background
    I've added some code to fail if the file wasn't found..
    Note: When calling images_at the rect is the format:
    (x, y, x + offset, y + offset)
    """

    def __init__(self, filename):
        """init."""
        try:
            self.sheet = pg.image.load(filename).convert()
        except pg.error:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey=None):
        """Load image from x,y,x+offset,y+offset."""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        rect
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects, colorkey=None):
        """Load multiple images, supply a list of coordinates."""
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a strip of images and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Game(object):
    """This class handles the majority of the game functionality."""

    def title_screen(self, screen, items):
        """Create the title screen with 'Play' and 'Quit' buttons."""
        self.clock = pg.time.Clock()
        self.screen = screen
        self.s_size = self.screen.get_size()
        self.m_items = []
        title = FNT['lrg'].render('SOLUS', 1, CLR['wht'])
        for index, item in enumerate(items):
            label = FNT['med'].render(item, 1, CLR['wht'])
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.s_size[0] / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.s_size[1] / 2) - (t_h / 2) + (index * height)
            self.m_items.append([item, label, (width, height), (posx, posy)])
        tsloop = True
        self.hard_quit = False

        while tsloop:
            self.clock.tick(60)
            mcx, mcy = (0, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    tsloop = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        tsloop = False
                    if event.key == pg.K_RETURN:
                        self.main(self.screen)
                        if self.hard_quit:
                            return

                if event.type == pg.MOUSEBUTTONUP:
                    mcx, mcy = pg.mouse.get_pos()

            self.screen.fill(CLR['blk'])
            self.screen.blit(title, (10, 10))

            for name, label, (width, height), (posx, posy) in self.m_items:
                self.screen.blit(label, (posx, posy))
                if posx <= mcx <= posx + width and \
                        posy <= mcy <= posy + height:
                    if name == 'Quit':
                        tsloop = False
                    if name == 'Start':
                        self.main(self.screen)
                        if self.hard_quit:
                            return

            pg.display.flip()

    def main(self, screen):
        """Handle game init and main while loop."""
        tmap = 'data\\world.tmx'
        tmap = res_path(tmap)
        self.tilemap = tmx.load(tmap, self.s_size)
        self.msgs = pg.Surface((self.s_size[0] - 40,
                                int(2 * FNT['sml'].get_height())),
                               pg.SRCALPHA, 32)
        self.msgs.convert_alpha()
        self.messages = [None, None]
        welcome = FNT['sml'].render('Welcome to Solus', 1, CLR['blk'])
        direction = FNT['sml'].render('Find something to fight!',
                                      1, CLR['blk'])
        self.messages[0] = welcome
        self.messages[1] = direction
        self.player_s = tmx.SpriteLayer()
        self.enemy_s = tmx.SpriteLayer()
        self.item_s = tmx.SpriteLayer()
        plr_st = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player('Andre', 3, (plr_st.px, plr_st.py), self.player_s)
        self.player.update_stats()
        level = rd.randint(1, 3)
        px = rd.randint(50, self.tilemap.px_width - 50)
        py = rd.randint(50, self.tilemap.px_height - 50)
        self.knife = Knife('Knife 1', level, (px, py), self.item_s)

        for i in range(rd.randint(1, 5)):
            enemy_list = []
            enemy_name = 'enemy ' + str(i)
            level = rd.randint(1, 3)
            px = rd.randint(50, self.tilemap.px_width - 50)
            py = rd.randint(50, self.tilemap.px_height - 50)
            enemy_list.append(Enemy(enemy_name, level, (px, py), self.enemy_s))

        self.tilemap.layers.append(self.player_s)
        self.tilemap.layers.append(self.enemy_s)
        self.tilemap.layers.append(self.item_s)
        while self.player.is_alive:
            # restrain to 30fps
            dt = self.clock.tick(30)
            # event handling
            for event in pg.event.get():
                # distinct key events
                if event.type == pg.QUIT:
                    self.hard_quit = True
                    return
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        return

            # continuous key events

            # drawing
            self.tilemap.update(dt / 1000., self)
            screen.fill((CLR['blk']))
            self.tilemap.draw(screen)
            self.blit_game_info(screen)

            # after drawing everything, flip()
            pg.display.flip()

    def blit_game_info(self, screen):
        """Blit default running text to screen."""
        screen.blit(self.messages[0], (20, 18))
        screen.blit(self.messages[1], (20, 29))
        screen.blit(self.player.hp_t, (345, 18))
        screen.blit(self.player.attk_t, (345, 29))
        screen.blit(self.player.dfnc_t, (345, 40))

    def update_msgs(self, msg):
        """Update messaes with most recent event message."""
        self.messages[0] = self.messages[1]
        message = FNT['sml'].render(msg, 1, CLR['blk'])
        self.messages[1] = message


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
        ssheet = 'data\\playerSS.png'
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
        img = 'data\\enemy.png'
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

# Base class for equipment items, contains level, group, name attributes


class Equipment(Thing):
    """This class handles all equipment, includes picking up."""

    def __init__(self, group, name, level, *groups):
        """init."""
        super(Equipment, self).__init__(*groups)
        # level of equipment, modifies main bonuses
        self.level = level
        # groups include weapon, armor, useable, etc...
        self.group = group
        self.name = name
        self.is_equipped = False
        self.picking_up = True

        id_parent = self.id
        self.id = 'equipment:' + id_parent

    def update(self, dt, game):
        """Update equipment, check for collides."""
        if self.rect.colliderect(game.player.rect) and self.picking_up:
            self.ask_pickup(dt, game)
        if not self.rect.colliderect(game.player.rect) and not self.picking_up:
            self.picking_up = True

    def ask_pickup(self, dt, game):
        """Ask player to pick up equipment, pickup equipment."""
        choice = True
        pickup = FNT['med'].render('Pick up ' + self.name + '?', 1, CLR['blk'])
        game.screen.fill((CLR['blk']))
        game.tilemap.draw(game.screen)
        game.screen.blit(pickup, (152, 170))
        game.screen.blit(TXT['YES'], (152, 192))
        game.screen.blit(TXT['no'], (152, 203))
        game.blit_game_info(game.screen)
        pg.display.flip()
        while True:
            for event in pg.event.get():
                # distinct key events
                if event.type == pg.QUIT:
                    game.hard_quit = True
                    return
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        return
                    if event.key == pg.K_RETURN:
                        if choice:
                            fn.pickup_equipment(game.player, self)
                            game.update_msgs('You picked up ' + self.name)
                            game.player.update_stats()
                            return
                        else:
                            return
                    if event.key == pg.K_DOWN:
                        choice = False
                        self.picking_up = False
                        game.screen.fill((CLR['blk']))
                        game.tilemap.draw(game.screen)
                        game.screen.blit(pickup, (152, 170))
                        game.screen.blit(TXT['yes'], (152, 192))
                        game.screen.blit(TXT['NO'], (152, 203))
                        game.blit_game_info(game.screen)
                        pg.display.flip()
                    if event.key == pg.K_UP:
                        choice = True
                        game.screen.fill((CLR['blk']))
                        game.tilemap.draw(game.screen)
                        game.screen.blit(pickup, (152, 170))
                        game.screen.blit(TXT['YES'], (152, 192))
                        game.screen.blit(TXT['no'], (152, 203))
                        game.blit_game_info(game.screen)
                        pg.display.flip()


# Base class for weapon items, contains range and type
class Weapon(Equipment):
    """This class handles all weapons."""

    def __init__(self, type, name, wep_range, level, *groups):
        """init."""
        super(Weapon, self).__init__('weapon', name, level, *groups)
        # controlls how far away you can attack from
        self.wep_range = wep_range
        # hold info about type, melee, ranged, etc...
        self.type = type

        id_parent = self.id
        self.id = 'weapon:' + id_parent

# Class for knife items, contains attack attack bonus


class Knife(Weapon):
    """This class handles knife weapons."""

    def __init__(self, name, level, location, *groups):
        """init."""
        super(Knife, self).__init__('melee', name, 1, level, *groups)
        # sets attack bonus by multiplying by level attribute(Equipment class)
        self.attk_bonus = 2 * self.level

        img = 'data\\knife.png'
        img = res_path(img)
        self.image = pg.image.load(img)
        self.image.convert()
        self.rect = pg.Rect(location, self.image.get_size())

        id_parent = self.id
        self.id = 'knife:' + id_parent
