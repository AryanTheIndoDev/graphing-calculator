import pygame as pg
from pygame import Rect, Surface, Color, Font, Vector2
from typing import Callable
from string import ascii_lowercase

import colors
import constants as c

from parser import parseEquation

# Type Declaration
type Point = tuple[int, int]

# InputBox
class InputBox:
    def __init__(self, font: Font) -> None:
        # text
        self.text: str = "y = x"
        self.font: Font = font
        self.color: Color = Color(200, 200, 200)

        # structure
        self.rect: Rect = Rect()

        self.border: int = 6

        # mechanics
        self.focused: bool = False
        self.backspaceMode: bool = False
        self.backspaceTime: float = 0

        self.cursor: int = 0

        # functions
        self._lastparsedtext = None
        self._cachedFunc: tuple[tuple, Callable] = ((), lambda: None)

    def draw(self, screen: Surface, pos: Point, dimensions: Point) -> None:
        # setting up bounding rect and main surf
        self.rect.size = dimensions
        surf = Surface((dimensions[0] - 2 * self.border, dimensions[1] - self.border), pg.SRCALPHA)

        # position
        self.rect.topleft = pos

        # inner rectangle
        innerRect = surf.get_rect()
        if self.focused:
            pg.draw.rect(surf, colors.Grey3, innerRect, 0, 5)
        else:
            pg.draw.rect(surf, colors.Grey1, innerRect, 0, 5)

        # text
        textSurf = self.font.render(self.text, True, self.color)
        textRect = textSurf.get_rect()

        textRect.left, textRect.centery = (2 * self.border, innerRect.height // 2)

        surf.blit(textSurf, textRect)

        screen.blit(surf, (pos[0] + self.border, pos[1] + self.border))

    def handleEvent(self, keyPresses: pg.key.ScancodeWrapper, events: list[pg.Event], dt: float) -> None:

        # Text Input
        for event in events:
            if event.type == pg.TEXTINPUT:
                self.text += event.text

        # Backspace
        self.handleBackspace(keyPresses, dt)

    def getEquation(self) -> tuple[tuple, Callable]:
        if self.text != self._lastparsedtext:
            self._lastparsedtext = self.text

            self._cachedFunc = parseEquation(self.text.replace(" ", ""), "x", "y")

        return self._cachedFunc

    def focusOn(self) -> None:
        self.focused = True

    def focusOff(self) -> None:
        self.focused = False

    def isColliding(self, point: Vector2) -> bool:
        return self.rect.collidepoint(point)

    # Helper Functions
    def handleBackspace(self, keyPresses: pg.key.ScancodeWrapper, dt: float):
        if keyPresses[pg.K_BACKSPACE]:
            # initial back
            if not self.backspaceMode and self.backspaceTime == 0:
                self.text = self.text[0:-1]
            # in between timer
            elif not self.backspaceMode and self.backspaceTime >= c.BACKSPACESTARTTIMER:
                self.text = self.text[0:-1]
                self.backspaceMode = True
                self.backspaceTime -= c.BACKSPACESTARTTIMER
            # backspace mode go brrrr
            elif self.backspaceMode and self.backspaceTime >= c.BACKSPACEBETWEENTIMER:
                self.text = self.text[0:-1]
                self.backspaceTime -= c.BACKSPACEBETWEENTIMER
            # timer increment
            self.backspaceTime += dt

        else:
            # resetting backspace
            self.backspaceTime = 0
            self.backspaceMode = False
            