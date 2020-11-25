from .base import BaseSprite
import pygame as pg
import math


class Sword(BaseSprite):

    sprite_filepath = "sword.png"

    def __init__(self, game, player):
        super().__init__(game)
        self.player = player

    def slash(self):
        pass
        # get each enemy, figure out if we hit them...

    def update(self, *args, **kwargs):
        self.point_at(pg.mouse.get_pos())

    def point_at(self, target):
        player_ctr = self.player.rect.center

        xchange = target[0] - player_ctr[0]
        ychange = target[1] - player_ctr[1]
        rads = math.atan2(ychange, xchange)
        rads %= 2 * math.pi
        angle = math.degrees(rads)

        offset = pg.math.Vector2(32 + 4, 0).rotate(angle)  # start from the edge of the player circle

        self.rect.center = pg.math.Vector2(player_ctr) + offset


class Bullet(BaseSprite):

    sprite_filepath = "bullet.png"

    def __init__(self, game, start_pos, target):
        # note https://github.com/mgold/Python-snippets/blob/master/pygame_angles.py
        super().__init__(game)

        xchange = target[0] - start_pos[0]
        ychange = target[1] - start_pos[1]
        rads = math.atan2(ychange, xchange)
        rads %= 2 * math.pi
        angle = math.degrees(rads)

        # offset = pg.math.Vector2(32, 0).rotate(angle)  # start from the edge of the circle
        self.pos = pg.math.Vector2(start_pos)  # + offset
        self.velocity = pg.math.Vector2(5, 0)
        self.velocity.rotate_ip(angle)

    def update(self, *args, **kwargs) -> None:
        self.pos += self.velocity
        self.rect.center = self.pos

        if not self.game.get_screen_rect().contains(self.rect):
            self.game.remove_sprite(self)
