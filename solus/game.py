from classes import *
from functions import encounter
from dicts import *
from map import tmx
import pygame
import random as rd
import sys

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


clock = pygame.time.Clock()

def title_screen(screen, items):
    s_size = screen.get_size()
    print s_size
    bg_color = CLR['blk']
    font_color = CLR['wit']
    menu_items = []

    title = FNT['lg'].render('SOLUS', 1, font_color)

    for index, item in enumerate(items):
        label = FNT['med'].render(item, 1, font_color)
        width = label.get_rect().width
        height = label.get_rect().height

        posx = (s_size[0] / 2) - (width / 2)
        t_h = len(items) * height
        posy = (s_size[1] / 2) - (t_h / 2) + (index * height)

        menu_items.append([item, label, (width, height), (posx,posy)])

    tsloop = True
    while tsloop:
        clock.tick(100)
        mcx, mcy = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tsloop = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    tsloop = False
                if event.key == pygame.K_RETURN:
                    main(screen)
            if event.type == pygame.MOUSEBUTTONUP:
                mcx, mcy = pygame.mouse.get_pos()

    screen.fill(bg_color)
    screen.blit(title, (10, 10))

    for name, label, (width, height), (posx, posy) in menu_items:
        screen.blit(label, (posx,posy))
        if posx <= mcx <= posx + width and posy <= mcy <= posy + height:
            if name == 'Quit':
                tsloop = False
            if name == 'Start':
                main(screen)

    pygame.display.flip()

def main(screen):
    s_size = screen.get_size()
    tilemap = tmx.load('map/world.tmx', s_size)
    msg_block = pygame.Surface((s_size[0] - 40, FNT['sm'].get_height()),
                                pygame.SRCALPHA, 32)
    msg_block.convert_alpha()

    txt =  FNT['sm'].render('Welcome to Solus', 1, CLR['blk'])
    msg_block.blit(txt, (0,0))


    player_s = tmx.SpriteLayer()
    enemy_s = tmx.SpriteLayer()
    item_s = tmx.SpriteLayer()

    plyr_strt = tilemap.layers['triggers'].find('player')[0]

    player = Player('Andre', 3, (plyr_strt.px, plyr_strt.py), player_s)

    for i in range(rd.randint(1,5)):
        enemy_list = []
        enemy_name = 'enemy' + str(i)
        level = rd.randint(1,3)
        px = rd.randint(50, tilemap.px_width-50)
        py = rd.randint(50, tilemap.px_height-50)
        enemy_list.append(Enemy(enemy_name, level, (px,py), enemy_s))
        print i

    tilemap.layers.append(player_s)
    tilemap.layers.append(enemy_s)

    while player.is_alive:
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
        c_m = sys.modules[__name__]
        #drawing LIKELY TO HAVE ISSUES HERE WITH UPDATE, NEEDS SELF?
        tilemap.update(dt / 1000., c)
        screen.fill((CLR['blk']))
        tilemap.draw(screen)
        screen.blit(msg_block, (20,18))
        #after drawing everything, flip()
        pygame.display.flip()
