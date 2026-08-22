import pygame as pg
from pygame import Rect, Surface, Color, Font
from typing import Callable

import colors
import constants as c

from parser import parseEquation

# Type Declaration
type Point = tuple[int, int]

# InputBox
class InputBox:
    def __init__(self, dimensions: Point, font: Font) -> None:
        # text
        self.text: str = ""
        self.font: Font = font
        self.color: Color = Color(200, 200, 200)

        # structure
        self.surf: Surface = Surface(dimensions, pg.SRCALPHA)

        self.rect: Rect = self.surf.get_rect()

        # mechanics
        self.backspaceMode: bool = False
        self.backspaceTime: float = 0

        self.cursor: int = 0

        # functions
        self._lastparsedtext = None
        self._cachedFunc = lambda: None

    def draw(self, screen: Surface, pos: Point) -> None:

        # resetting self surface
        self.surf.fill(colors.Green1)

        # position
        self.rect.topleft = pos

        # text
        textSurf = self.font.render(self.text, True, self.color)
        textRect = textSurf.get_rect()

        textRect.left, textRect.centery = (10, self.rect.height // 2)

        self.surf.blit(textSurf, textRect)

        screen.blit(self.surf, self.rect)

    def handleEvent(self, keyPresses: pg.key.ScancodeWrapper, events: list[pg.Event], dt: float) -> None:

        # Text Input
        for event in events:
            if event.type == pg.TEXTINPUT:
                self.text += event.text

        # Backspace
        self.handleBackspace(keyPresses, dt)

    def getEquation(self) -> Callable:
        if self.text != self._lastparsedtext:
            self._lastparsedtext = self.text
            self._cachedFunc = parseEquation(self.text.replace(" ", ""), "x", "y")

        return self._cachedFunc

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
            