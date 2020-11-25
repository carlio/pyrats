from .base import BaseSprite
from .weapons import Bullet, Sword

import pygame as pg


class Player(BaseSprite):

    sprite_filepath = "black-circle.png"

    def __init__(self, game):
        super().__init__(game)
        self.speed = 5
        self.bullet_count = 10

        self.sword = Sword(game, self)

    def slash(self):
        self.sword.slash()

    def shoot(self, target):
        if self.bullet_count <= 0:
            # TODO: make empty gun click noise
            return

        Bullet(self.game, self.rect.center, target)
        self.bullet_count -= 1

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.clamp(self.game.get_screen_rect())
        # use update to handle continuous events like movement
        self.handle_keystate(pg.key.get_pressed())
        # use handle event to handle single situations like clicks

    def handle_keystate(self, keystate):
        # movement
        xchange, ychange = 0, 0
        if keystate[pg.K_w]:  # W -> up
            ychange -= 1
        if keystate[pg.K_a]:  # A -> left
            xchange -= 1
        if keystate[pg.K_s]:  # S -> down
            ychange += 1
        if keystate[pg.K_d]:  # D -> right
            xchange += 1

        self.rect.move_ip(self.speed * xchange, self.speed * ychange)

    def handle_event(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # left click!
                self.slash()
            if event.button == 3:
                # right click!
                self.shoot(pg.mouse.get_pos())
