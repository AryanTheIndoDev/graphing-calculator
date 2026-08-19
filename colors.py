import pygame as pg
from pygame import Color, Surface

import constants as c

"""Helper Functions"""

def createGradient(orientation: tuple[int, int], dimensions: tuple[int, int], *colors: Color) -> Surface:
    surf = Surface(orientation, pg.SRCALPHA)
    if orientation[0] * orientation[1] != len(colors):
        raise ValueError("Colors must be provided for each pixel")
    index = 0
    for x in range(surf.width):
        for y in range(surf.height):
            surf.set_at((x, y), colors[index])
            index += 1

    return pg.transform.smoothscale(surf, dimensions)

"""Primary Colors"""

White = Color(255, 255, 255, 255)
Black = Color(0, 0, 0, 255)
Grey1 = Color(10, 10, 10, 255)
Grey2 = Color(30, 30, 30, 255)
Grey3 = Color(50, 50, 50, 255)
Grey4 = Color(70, 70, 70, 255)
Green1 = Color(40, 96, 77)

"""Exclusive Colors"""

# Grid
MajorAxisColor = Color(200, 200, 200, 150)
MinorAxisColor = Color(100, 100, 100, 50)

"""Gradients"""

InputHeaderGradient = createGradient((2, 2), (c.INPUTWINDOWWIDTH, c.HEADERHEIGHT), Grey2, Grey1, Grey1, Black)