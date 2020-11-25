import pygame as pg
from .player import Player
from .ai import EnemyPirate

FPS = 100


class PyRatsGame:
    """
    This class is to represent the main game loop and
    keep sprite updates going
    """

    def __init__(self):
        self._screen_rect = pg.Rect(0, 0, 640, 800)
        self._all_sprites = pg.sprite.RenderUpdates()

    def get_screen_rect(self):
        return self._screen_rect

    def register_sprite(self, sprite):
        self._all_sprites.add(sprite)

    def remove_sprite(self, sprite):
        self._all_sprites.remove(sprite)

    def setup(self):
        # start up pygame
        pg.init()
        pg.display.set_caption("PyRats")

        # set up the screen
        self._screen = pg.display.set_mode(self._screen_rect.size)
        self._background = pg.Surface(self._screen_rect.size)
        self._background.fill((255, 255, 255))

        self._screen.blit(self._background, (0, 0))
        pg.display.flip()

        # make the player and some enemies
        self._player = Player(self)
        self._enemies = [
            EnemyPirate(self, (222, 333)),
            EnemyPirate(self, (222, 333)),
            EnemyPirate(self, (222, 333)),
        ]

    def run(self):
        self.setup()
        self.game_loop()

    def game_loop(self):
        clock = pg.time.Clock()

        running = True

        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                for sprite in self._all_sprites:
                    sprite.handle_event(event)

            # draw the scene
            self._all_sprites.clear(self._screen, self._background)
            self._all_sprites.update()
            dirty = self._all_sprites.draw(self._screen)
            pg.display.update(dirty)

            clock.tick(FPS)

        pg.quit()
