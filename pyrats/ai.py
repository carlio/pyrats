from .base import BaseSprite
import random
import math
import pygame as pg


class EnemyPirate(BaseSprite):

    sprite_filepath = "red-circle.png"

    def __init__(self, game, spawn_pos):
        super().__init__(game)
        self.pos = spawn_pos
        self.set_random_target()
        self.speed = 3

    def set_random_target(self):
        # TODO: create a rectangle 32px smaller than screen rect so that
        # this sprite's centre (it's a 64x64 image) can reach all targets
        scrct = self.game.get_screen_rect()
        self.target = (
            random.randint(scrct.left + 32, scrct.right - 32),  # x target
            random.randint(scrct.top + 32, scrct.bottom - 32),  # y target
        )

    def adjust_velocity(self):
        start_pos = self.rect.center
        xchange = self.target[0] - start_pos[0]
        ychange = self.target[1] - start_pos[1]
        rads = math.atan2(ychange, xchange)
        rads %= 2 * math.pi
        angle = math.degrees(rads)

        self.pos = pg.math.Vector2(start_pos)
        self.velocity = pg.math.Vector2(self.speed, 0)
        self.velocity.rotate_ip(angle)
        self.rect.center += self.velocity

    def target_reached(self):
        return self.rect.collidepoint(self.target)

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.clamp(self.game.get_screen_rect())

        # self.see_if_got_hit()

        if self.target_reached():
            self.set_random_target()

        self.adjust_velocity()
