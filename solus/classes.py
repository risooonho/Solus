import functions as fn
from dicts import *
from map import tmx
import pygame
import random as rd

#pasted spritesheet class from pygame supporter somewhere...
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

    def title_screen(self, screen, items):
        self.clock = pygame.time.Clock()

        self.screen = screen
        self.s_size = self.screen.get_size()
        self.m_items = []

        title = FNT['lrg'].render('SOLUS', 1, CLR['wht'])

        for index, item in enumerate(items):
            label = FNT['med'].render(item, 1, CLR['wht'])
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.s_size[0] / 2) - (width / 2)
            t_h = len(items)*height
            posy = (self.s_size[1] / 2) - (t_h / 2) + (index * height)
            self.m_items.append([item, label, (width, height), (posx,posy)])

        tsloop = True
        self.hard_quit = False
        while tsloop:
            self.clock.tick(60)
            mcx, mcy = (0, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tsloop = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        tsloop = False
                    if event.key == pygame.K_RETURN:
                        self.main(self.screen)
                        if self.hard_quit:

                            return
                if event.type == pygame.MOUSEBUTTONUP:
                    mcx, mcy = pygame.mouse.get_pos()

            self.screen.fill(CLR['blk'])
            self.screen.blit(title, (10, 10))

            for name, label, (width, height), (posx, posy) in self.m_items:
                self.screen.blit(label, (posx,posy))
                if posx <= mcx <= posx + width and posy <= mcy <= posy + height:
                    if name == 'Quit':
                        tsloop = False
                    if name == 'Start':
                        self.main(self.screen)
                        if self.hard_quit:
                            return

            pygame.display.flip()

    def main(self, screen):
        self.tilemap = tmx.load('map/world.tmx', self.s_size)
        self.msgs = pygame.Surface((self.s_size[0]-40,
                                    int(2 * FNT['sml'].get_height())),
                                    pygame.SRCALPHA, 32)
        self.msgs.convert_alpha()

        self.messages = [None, None]
        welcome =  FNT['sml'].render('Welcome to Solus', 1, CLR['blk'])
        direction = FNT['sml'].render('Find something to fight!', 1, CLR['blk'])
        self.messages[0] = welcome
        self.messages[1] = direction


        self.player_s = tmx.SpriteLayer()
        self.enemy_s = tmx.SpriteLayer()
        self.item_s = tmx.SpriteLayer()

        plr_st = self.tilemap.layers['triggers'].find('player')[0]

        self.player = Player('Andre', 3, (plr_st.px, plr_st.py), self.player_s)
        self.player.update_stats()

        level = rd.randint(1,3)
        px = rd.randint(50, self.tilemap.px_width-50)
        py = rd.randint(50, self.tilemap.px_height-50)
        self.knife = Knife('Knife 1', level, (px,py), self.item_s)

        for i in range(rd.randint(1,5)):
            enemy_list = []
            enemy_name = 'enemy ' + str(i)
            level = rd.randint(1,3)
            px = rd.randint(50, self.tilemap.px_width-50)
            py = rd.randint(50, self.tilemap.px_height-50)
            enemy_list.append(Enemy(enemy_name, level, (px,py), self.enemy_s))

        #self.enemy = Enemy('Gloob', 1, (enemy_strt.px, enemy_strt.py), self.enemy_s)

        self.tilemap.layers.append(self.player_s)
        self.tilemap.layers.append(self.enemy_s)
        self.tilemap.layers.append(self.item_s)

        while self.player.is_alive:
            #restrain to 30fps
            dt = self.clock.tick(30)
            #event handling
            for event in pygame.event.get():
                #distinct key events
                if event.type == pygame.QUIT:
                    self.hard_quit = True
                    return
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        return

            #continuous key events

            #drawing
            self.tilemap.update(dt / 1000., self)
            screen.fill((CLR['blk']))
            self.tilemap.draw(screen)
            self.blit_game_info(screen)

            #after drawing everything, flip()
            pygame.display.flip()

    def blit_game_info(self, screen):
        screen.blit(self.messages[0], (20,18))
        screen.blit(self.messages[1], (20, 29))
        screen.blit(self.player.hp_t, (345, 18))
        screen.blit(self.player.attk_t, (345, 29))
        screen.blit(self.player.dfnc_t, (345, 40))

    def update_msgs(self, msg):
        self.messages[0] = self.messages[1]
        message =  FNT['sml'].render(msg, 1, CLR['blk'])
        self.messages[1] = message

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
        lvl = CHR_LEVEL[level]
        hp = lvl[0]

        super(Character, self).__init__(name, hp, *groups)
        self.type = type
        self.is_alive = True

        self.attk = lvl[1]
        self.dfnc = lvl[2]

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

    def update_stats(self):
        self.hp_t = FNT['sml'].render('    HP: '+str(self.hp), 1, CLR['blk'])
        self.attk_t = FNT['sml'].render('ATTK: '+str(self.attk), 1, CLR['blk'])
        self.dfnc_t = FNT['sml'].render('DFNC: '+str(self.dfnc), 1, CLR['blk'])

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

        game.tilemap.set_focus(new.x, new.y)

#Base class for player creation holds ... can just
#use character object with attributes of hostile?
class Enemy(Character):

    def __init__(self, name, level, location, *groups):

        super(Enemy, self).__init__(name, level, 'enemy', *groups)

        self.image = pygame.image.load('imgs/enemy.png')
        self.image.convert()
        self.rect = pygame.Rect(location, self.image.get_size())
        self.font = pygame.font.SysFont(None, 10)
        self.level_txt = self.font.render(str(level), 1, (255,255,255))

        self.image.blit(self.level_txt, (5, 5))

        id_parent = self.id
        self.id = 'enemy:' + id_parent
        self.i = 0

        font = pygame.font.Font(None, 24)
        font_color = (255,255,255)
        font_background = (0,0,0)
        t = font.render('Enemy!', True, font_color, font_background)
        t_rect = t.get_rect()
        t_rect.centerx, t_rect.centery = 100,100

    def update(self, dt, game):
        if self.rect.colliderect(game.player.rect):
            if self.is_alive and game.player.is_alive:
                fn.encounter(game.player, self)
                if not self.is_alive:
                    game.update_msgs('You killed ' + self.name)
                    game.player.update_stats()

#Base class for equipment items, contains level, group, name attributes
class Equipment(Thing):

    def __init__(self, group, name, level, *groups):
        super(Equipment, self).__init__(*groups)
        #level of equipment, modifies main bonuses
        self.level = level
        #groups include weapon, armor, useable, etc...
        self.group = group
        self.name = name
        self.is_equipped = False
        self.picking_up = True

        id_parent = self.id
        self.id = 'equipment:' + id_parent

    def update(self, dt, game):

        if self.rect.colliderect(game.player.rect) and self.picking_up:
            self.ask_pickup(dt, game)
        if not self.rect.colliderect(game.player.rect) and not self.picking_up:
            self.picking_up = True

    def ask_pickup(self, dt, game):
        choice = True
        pickup = FNT['med'].render('Pick up ' + self.name + '?', 1, CLR['blk'])
        game.screen.fill((CLR['blk']))
        game.tilemap.draw(game.screen)
        game.screen.blit(pickup, (152, 170))
        game.screen.blit(TXT['YES'], (152, 192))
        game.screen.blit(TXT['no'], (152, 203))
        game.blit_game_info(game.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                #distinct key events
                if event.type == pygame.QUIT:
                    game.hard_quit = True
                    return
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        if choice:
                            fn.pickup_equipment(game.player, self)
                            game.update_msgs('You picked up ' + self.name)
                            game.player.update_stats()
                            return
                        else:
                            return
                    if event.key == pygame.K_DOWN:
                        choice = False
                        self.picking_up = False
                        game.screen.fill((CLR['blk']))
                        game.tilemap.draw(game.screen)
                        game.screen.blit(pickup, (152, 170))
                        game.screen.blit(TXT['yes'], (152, 192))
                        game.screen.blit(TXT['NO'], (152, 203))
                        game.blit_game_info(game.screen)
                        pygame.display.flip()
                    if event.key == pygame.K_UP:
                        choice = True
                        game.screen.fill((CLR['blk']))
                        game.tilemap.draw(game.screen)
                        game.screen.blit(pickup, (152, 170))
                        game.screen.blit(TXT['YES'], (152, 192))
                        game.screen.blit(TXT['no'], (152, 203))
                        game.blit_game_info(game.screen)
                        pygame.display.flip()



#Base class for weapon items, contains range and type
class Weapon(Equipment):

    def __init__(self, type, name, wep_range, level, *groups):
        super(Weapon, self).__init__('weapon', name, level, *groups)
        #controlls how far away you can attack from
        self.wep_range = wep_range
        #hold info about type, melee, ranged, etc...
        self.type = type

        id_parent = self.id
        self.id = 'weapon:' + id_parent

#Class for knife items, contains attack attack bonus
class Knife(Weapon):

    def __init__(self, name, level, location, *groups):
        super(Knife, self).__init__('melee', name, 1, level, *groups)
        #sets attack bonus by multiplying by level attribute(Equipment class)
        self.attk_bonus = 2 * self.level

        self.image = pygame.image.load('imgs/knife.png')
        self.image.convert()
        self.rect = pygame.Rect(location, self.image.get_size())

        id_parent = self.id
        self.id = 'knife:' + id_parent
