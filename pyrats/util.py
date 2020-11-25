import os
import pygame as pg


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
