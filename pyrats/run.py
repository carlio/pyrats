#!/usr/bin/env python
import pygame as pg
import os
import math


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


class Bullet(pg.sprite.Sprite):
    def __init__(self, start_pos, target):
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
        self.velocity = pg.math.Vector2(5, 0)
        self.velocity.rotate_ip(angle)

    def update(self, *args, **kwargs) -> None:
        self.pos += self.velocity
        self.rect.center = self.pos


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = load_image("black-circle.png")
        self.speed = 5
        self.rect = self.image.get_rect(midbottom=SCREENRECT.center)

    def shoot(self, target):
        Bullet(self.rect.center, target)

    def update(self, *args, **kwargs) -> None:
        self.handle_keystate(pg.key.get_pressed())

    def handle_keystate(self, keystate):
        self.rect = self.rect.clamp(SCREENRECT)

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
    clock = pg.time.Clock()

    # main loop
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    player.shoot(pg.mouse.get_pos())
                # if event.button == 3: # right click

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
