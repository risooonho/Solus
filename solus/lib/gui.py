import pygame as pg
from lib import constants as c
from lib import setup


class Widget(pg.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Widget, self).__init__(*groups)
        self.location = location
        self.image = pg.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.location


class Button(Widget):
    def __init__(self, location, label, function=False, *groups):
        super(Button, self).__init__(location, *groups)
        self.name = label
        self.state = 0
        self.draw_button(self.name)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.clicked = function

    def draw_button(self, label):
        txt = setup.FNT[50].render(label, 1, c.WHITE)
        t_w, t_h = txt.get_size()
        b_w = t_w * 1.5
        b_h = t_h * 1.25
        t_x = (b_w // 2) - (t_w // 2)
        t_y = (b_h // 2) - (t_h // 2)

        self.image = pg.Surface((b_w, b_h))
        self.image.fill((100, 100, 100))
        self.image.blit(txt, (t_x, t_y))

    def click(self):
        txt = setup.FNT[50].render(self.name, 1, c.BLACK)
        t_w, t_h = txt.get_size()
        b_w = t_w * 1.5
        b_h = t_h * 1.25
        t_x = (b_w // 2) - (t_w // 2)
        t_y = (b_h // 2) - (t_h // 2)
        self.image = pg.Surface((b_w, b_h))
        self.image.fill((200, 200, 200))
        self.image.blit(txt, (t_x, t_y))


class SlideGroup(pg.sprite.Sprite):
    def __init__(self, location, widget, *groups):
        super(SlideGroup, self).__init__(*groups)
        self.image = pg.Surface((100, 100))
        self.image.fill(c.GREY)
        self.widget = widget
        self.image.blit(self.widget.image, (20, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.clock = pg.time.Clock()
        self.name = 'slide group'

    def slide_group(self, pos, state):
        if state:
            if self.rect.right > 600:
                self.rect.move_ip(-10, 0)
        else:
            if self.rect.left < 580:
                self.rect.move_ip(10, 0)

    def get_clicked(self, pos):
        convert = (self.rect.x, self.rect.y)
        c_pos = (pos[0] - convert[0], pos[1] - convert[1])
        return c_pos

    def update(self, update):
        self.widget.update(update)
        self.image.fill(c.GREY)
        self.image.blit(self.widget.image, (20, 0))


class Text(Widget):
    def __init__(self, txt, location, font_size, color, *groups):
        super(Text, self).__init__(location, *groups)
        self.image = setup.FNT[font_size].render(txt, 1, color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location


class TextList(Widget):
    def __init__(self, title, txt_list, font_size, color, location, *groups):
        super(TextList, self).__init__(location, *groups)
        self.rect.x, self.rect.y = location
        self.fs = font_size
        self.col = color
        self.title = setup.FNT[font_size].render(title, 1, self.col)
        self.update(txt_list)

    def update(self, txt_list):
        self.str_list = txt_list
        self.text_list = []
        num = 0
        for index, txt in enumerate(self.str_list):
            self.text_list.append(setup.FNT[self.fs].render(txt, 1, self.col))
            num += 1
        self.txt_h = self.title.get_height()
        self.list_h = (1.5 * self.txt_h) + (num * self.txt_h)
        self.image = pg.Surface((600, self.list_h), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.blit(self.title, (0, 0))
        for index, txt in enumerate(self.text_list):
            txt_y = (1.5 * self.txt_h) + (index * self.txt_h)
            self.image.blit(txt, (10, (txt_y)))

    def update_messages(self, new_message):
        self.image.fill(0)
        self.str_list[0] = self.str_list[1]
        self.str_list[1] = new_message
        self.image.blit(self.title, (0, 0))
        for index, msg in enumerate(self.str_list):
            self.text_list[index] = setup.FNT[self.fs].render(msg, 1, self.col)
            msg_y = (1.5 * self.txt_h) + (index * self.txt_h)
            self.image.blit(self.text_list[index], (10, (msg_y)))
