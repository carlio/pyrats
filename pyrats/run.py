#!/usr/bin/env python
import pygame as pg
import os


SCREENRECT = pg.Rect(0, 0, 640, 800)


DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 4
DIRECTION_RIGHT = 8


def _get_asset(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    return os.path.join(assets_dir, filename)


def load_image(filename):
    """ loads an image, prepares it for play
    """
    print("loading image %s from %s" % (filename, _get_asset(filename)))
    surface = pg.image.load(_get_asset(filename))
    return surface.convert()


ALL_SPRITES = pg.sprite.RenderUpdates()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = pg.transform.flip(load_image("black-circle.png"), 1, 0)

        self.rect = self.image.get_rect(midbottom=SCREENRECT.center)

    def move(self, direction):
        self.rect = self.rect.clamp(SCREENRECT)

        print(direction)

        xchange, ychange = 0, 0
        if direction == DIRECTION_DOWN:
            ychange = 1
        elif direction == DIRECTION_UP:
            ychange = -1
        if direction == DIRECTION_LEFT:
            xchange = -1
        elif direction == DIRECTION_RIGHT:
            xchange = 1

        self.rect.move_ip(xchange, ychange)


def main():
    pg.init()
    pg.display.set_caption("Pyrats")

    screen = pg.display.set_mode(SCREENRECT.size)

    # create the background, tile the bgd image
    bgdtile = load_image("cat.jpg")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
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
            if event.type == pg.TEXTINPUT:
                key = event.text.lower()
                direction = {"w": DIRECTION_UP, "a": DIRECTION_LEFT, "s": DIRECTION_DOWN, "d": DIRECTION_RIGHT}[key]
                player.move(direction)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click
                    print("meow")
                if event.button == 3:
                    # right click
                    print("purr")
                print(event.pos)

            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # draw the scene
        dirty = ALL_SPRITES.draw(screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps
        clock.tick(40)


if __name__ == "__main__":
    main()
