#!/usr/bin/env python
import pygame as pg
import os


SCREENRECT = pg.Rect(0, 0, 640, 800)
ALL_SPRITES = pg.sprite.RenderUpdates()


def _get_asset(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    return os.path.join(assets_dir, filename)


def load_image(filename):
    """ loads an image, prepares it for play
    """
    print("loading image %s from %s" % (filename, _get_asset(filename)))
    surface = pg.image.load(_get_asset(filename))
    return surface.convert_alpha()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(ALL_SPRITES)
        self.image = pg.transform.flip(load_image("black-circle.png"), 1, 0)
        self.speed = 5
        self.rect = self.image.get_rect(midbottom=SCREENRECT.center)

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

        # see if the player is pressing WASD
        player.handle_keystate(pg.key.get_pressed())

        # draw the scene
        ALL_SPRITES.clear(screen, background)
        dirty = ALL_SPRITES.draw(screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps
        clock.tick(40)


if __name__ == "__main__":
    main()
