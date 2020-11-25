from pygame.sprite import Sprite
from .util import load_image


class BaseSprite(Sprite):
    """
    This class represents an object.

    It is a collection of common functions about movement,
    shooting etc, but it is just a base class.
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.game.register_sprite(self)
        self.image = load_image(self.sprite_filepath)
        self.rect = self.image.get_rect(center=game.get_screen_rect().center)

    def handle_event(self, event):
        pass
