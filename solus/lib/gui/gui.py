import pygame as pg


class Widget(pg.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Widget, self).__init__(*groups)
        self.location = location
        self.image = pg.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.location[0]
        self.rect.y = self.location[1]
