#!/usr/bin/env python
import random

import pygame as pg
import os
import math
from pygame.sprite import Sprite


SCREENRECT = pg.Rect(0, 0, 640, 800)
ALL_SPRITES = pg.sprite.RenderUpdates()


def _get_asset(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    return os.path.join(assets_dir, filename)


IMAGE_CACHE = {}


def load_image(filename):
    surface = IMAGE_CACHE.get(filename)
    if surface is not None:
        return surface

    surface = pg.image.load(_get_asset(filename))
    IMAGE_CACHE[filename] = surface

    return surface.convert_alpha()


BULLETS = []


class Bullet(Sprite):
    def __init__(self, start_pos, target, speed):
        # note https://github.com/mgold/Python-snippets/blob/master/pygame_angles.py
        super().__init__(ALL_SPRITES)
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect(center=start_pos)

        xchange = target[0] - start_pos[0]
        ychange = target[1] - start_pos[1]
        rads = math.atan2(ychange, xchange)
        rads %= 2 * math.pi
        angle = math.degrees(rads)

        offset = pg.math.Vector2(32, 0).rotate(angle)  # start from the edge of the circle
        self.pos = pg.math.Vector2(start_pos) + offset
        self.velocity = pg.math.Vector2(speed, 0)
        self.velocity.rotate_ip(angle)
        BULLETS.append(self)

    def update(self, *args, **kwargs) -> None:
        self.pos += self.velocity
        self.rect.center = self.pos

        if not SCREENRECT.contains(self.rect):
            self.remove()

    def remove(self):
        # remove from sprite updates, it'll get GC'd
        for group in self.groups():
            group.remove(self)
        BULLETS.remove(self)


class BadGuy(Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = load_image("red-circle.png")
        start_positions = {
            "midbottom": SCREENRECT.midbottom,
            "bottomleft": SCREENRECT.bottomleft,
            "bottomright": SCREENRECT.bottomright,
            "topleft": SCREENRECT.topleft,
            "topright": SCREENRECT.topright,
        }
        self.speed = 3
        # ick:
        _key = random.choice(list(start_positions.keys()))
        start_pos = {_key: start_positions[_key]}
        self.rect = self.image.get_rect(**start_pos)
        # set initial random target
        self.set_random_target()

    def set_random_target(self):
        # TODO: create a rectangle 32px smaller than screen rect so that
        # this sprite's centre (it's a 64x64 image) can reach all targets
        self.target = (
            random.randint(SCREENRECT.left + 32, SCREENRECT.right - 32),  # x target
            random.randint(SCREENRECT.top + 32, SCREENRECT.bottom - 32),  # y target
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

    def see_if_got_hit(self):
        for bullet in BULLETS:
            if self.rect.collidepoint(bullet.rect.center):
                # remove the bullet
                bullet.remove()
                # no more updates
                for group in self.groups():
                    group.remove(self)

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.clamp(SCREENRECT)

        self.see_if_got_hit()

        if self.target_reached():
            self.set_random_target()

        self.adjust_velocity()


class Player(Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = load_image("black-circle.png")
        self.speed = 5
        self.rect = self.image.get_rect(center=SCREENRECT.center)
        self.bullets = 10

    def shoot(self, target, speed):
        if self.bullets == 0:
            return
        # no need to keep a reference, we won't do anything
        Bullet(self.rect.center, target, speed)
        self.bullets -= 1

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.clamp(SCREENRECT)
        self.handle_keystate(pg.key.get_pressed())

    def handle_keystate(self, keystate):
        xchange, ychange = 0, 0
        if keystate[pg.K_w]:
            # W -> up
            ychange -= 1
        if keystate[pg.K_a]:
            # A -> left
            xchange -= 1
        if keystate[pg.K_s]:
            # S -> down
            ychange += 1
        if keystate[pg.K_d]:
            # D -> right
            xchange += 1

        self.rect.move_ip(self.speed * xchange, self.speed * ychange)


def main():
    pg.init()
    pg.display.set_caption("PyRats")

    screen = pg.display.set_mode(SCREENRECT.size)
    background = pg.Surface(SCREENRECT.size)
    background.fill((255, 255, 255))

    screen.blit(background, (0, 0))
    pg.display.flip()

    # create the player
    player = Player()
    # make bad guys
    [BadGuy() for _ in range(5)]

    clock = pg.time.Clock()

    # main loop
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    player.shoot(pg.mouse.get_pos(), event.button * 4)

            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # draw the scene
        ALL_SPRITES.clear(screen, background)
        ALL_SPRITES.update()
        dirty = ALL_SPRITES.draw(screen)
        pg.display.update(dirty)

        # fix the framerate
        clock.tick(100)

    pg.quit()


if __name__ == "__main__":
    main()
