#!/usr/bin/env python
import pygame as pg
import os


SCREENRECT = pg.Rect(0, 0, 640, 800)


def _get_asset(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    return os.path.join(assets_dir, filename)


def load_image(filename):
    """ loads an image, prepares it for play
    """
    surface = pg.image.load(_get_asset(filename))
    return surface.convert()


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

    # main loop
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.MOUSEBUTTONDOWN:
                print("meow")
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
