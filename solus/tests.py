import os
import pygame
from dicts import *

def msgs_update(msgs, msg):
    msgs[0] = msgs[1]
    msgs[1] = msg
    return msgs

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    font = pygame.font.SysFont(None, 30)
    print font.size('MESSAGE')
    font_color = CLR['wit']

    msgs = ['Welcome', 'Notification1']
    looping = True
    while looping:
        for event in pygame.event.get():
            #distinct key events
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                looping = False

        messages = []

        for index, msg in enumerate(msgs):
            txt =  font.render(msg, 1, font_color)
            width = txt.get_rect().width
            height = txt.get_rect().height
            print height

            posx = 20
            t_h = len(msgs)*height
            posy = 30 - (t_h/2) + (index * height)

            messages.append([msg, txt, (width, height), (posx,posy)])

        for txt, name, (width, height), (posx, posy) in messages:
            screen.blit(name, (posx,posy))

        pygame.display.flip()
        screen.fill(CLR['blk'])

        msgs_update(msgs, 'notification2')

'''
    self.screen = screen
    scr_width = self.screen.get_rect().width
    scr_height = self.screen.get_rect().height
    bg_color = CLR['blk']

    self.items = items
    self.lg_font = pygame.font.SysFont(None, 60)
    self.font = pygame.font.SysFont(None, 30)
    font_color = CLR['wit']

    self.items = []
    title = self.lg_font.render('SOLUS', 1, font_color)

    for index, item in enumerate(items):
        label = self.font.render(item, 1, font_color)
        width = label.get_rect().width
        height = label.get_rect().height

        posx = (scr_width/2) - (width/2)
        t_h = len(items)*height
        posy = (scr_height/2) - (t_h/2) + (index * height)

        self.items.append([item, label, (width, height), (posx,posy)])

    tsloop = True
    while tsloop:
        clock.tick(60)
        mcx, mcy = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tsloop = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                tsloop = False
            if event.type == pygame.MOUSEBUTTONUP:
                mcx, mcy = pygame.mouse.get_pos()

        self.screen.fill(bg_color)
        self.screen.blit(title, (10, 10))

        for name, label, (width, height), (posx, posy) in self.items:
            self.screen.blit(label, (posx,posy))
            if posx <= mcx <= posx + width and posy <= mcy <= posy + height:
                if name == 'Quit':
                    tsloop = False
                if name == 'Start':
                    self.main(self.screen)
        pygame.display.flip()
'''
