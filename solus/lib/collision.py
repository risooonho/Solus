import pygame as pg


class CollisionHandler(object):
    def __init__(self, player, enemies, items, world):
        self.player = player
        self.enemies = enemies
        self.items = items
        self.world = world
        self.last = None

    def update(self, world, keys):
        self.player.rect = self.check_for_blocker(world)
        self.check_for_fight(world)
        self.check_for_pickup(world)

    def check_for_blocker(self, world):
        new = self.player.rect.copy()

        for cell in world.tilemap.layers['triggers'].collide(new, 'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and new.bottom > cell.top:
                new.bottom = cell.top
            if 'b' in blockers and new.top < cell.bottom:
                new.top = cell.bottom
        return new

    def check_for_fight(self, world):
        enemy = pg.sprite.spritecollideany(self.player, self.enemies)
        if enemy is not None:
            enemy.encounter(self.player, world)

    def check_for_pickup(self, world):
        item = pg.sprite.spritecollideany(self.player, self.items)

        if item is not None:
            self.last = item
            if item.picking_up:
                item.on_collide(self.player, world)
        else:
            try:  # Need to fix this logic...
                self.last.picking_up = True
                self.last = None
            except:
                pass
