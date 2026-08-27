import pygame as pg
from pygame import Surface, Rect, Font, Vector2
from typing import Callable

import colors
import constants as c

from inputBox import InputBox

# Input
class Input:
    def __init__(self, screen: Surface) -> None:
        # Screen
        self.screen: Surface = screen

        # Boxes
        self.boxes: list[InputBox] = []
        self.focused: int | None = None
        self.font: Font = pg.font.SysFont("Cambria Math", 20)
        self.headerFont: Font = pg.font.SysFont("Corbel", 40, bold = True)

        self.functions: list[tuple[tuple, Callable]] = []

        # Screen Components
        self.headerWindow: Surface = Surface((self.screen.width, c.HEADERHEIGHT))
        self.boxWindow: Surface = Surface((self.screen.width, self.screen.height - c.HEADERHEIGHT))

        self.headerRect: Rect = self.headerWindow.get_rect()
        self.boxRect: Rect = self.boxWindow.get_rect(topleft = (0, c.HEADERHEIGHT))

        # Scroll
        self.scroll: int = 0

    def draw(self) -> None:
        # Resetting components
        self.headerWindow.blit(colors.InputHeaderGradient)
        self.boxWindow.fill(colors.Black)

        # header
        header = self.headerFont.render("graphity", True, colors.Green1)
        self.headerWindow.blit(header, header.get_rect(center = self.headerRect.center))

        self.screen.blit(self.headerWindow, self.headerRect)

        # boxes
        for index, box in enumerate(self.boxes):
            box.draw(self.boxWindow, (0, index * c.BOXHEIGHT), (self.screen.width, c.BOXHEIGHT))

        self.screen.blit(self.boxWindow, self.boxRect)

        # dividers
        # auxiliary
        pg.draw.line(self.screen, colors.Grey2, (0, c.HEADERHEIGHT), (self.screen.width, c.HEADERHEIGHT), 2)
        # main
        pg.draw.line(self.screen, colors.Grey5, (0, 0), (0, self.screen.height), 3)
        pg.draw.line(self.screen, colors.Grey5, (self.screen.width, 0), (self.screen.width, self.screen.height), 6)

    def update(self, keyPresses: pg.key.ScancodeWrapper, events: list[pg.Event], mousePos: Vector2, dt: float) -> None:
        functions: list = []

        # handle focusing
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in self.boxes:
                        if box.isColliding(mousePos - Vector2(0, c.HEADERHEIGHT)):
                            box.focusOn()
                        else:
                            box.focusOff()

        # handle inputs
        for box in self.boxes:
            if box.focused:
                box.handleEvent(keyPresses, events, dt)

            # handle outputs
            function = box.getEquation()
            functions.append(function)

        self.functions = functions.copy()

    def addBox(self) -> None:
        box = InputBox(self.font)
        self.boxes.append(box)

    def onResize(self, screen: Surface):
        # update screen
        self.screen = screen

        # updating screen components
        self.headerWindow: Surface = Surface((self.screen.width, c.HEADERHEIGHT))
        self.boxWindow: Surface = Surface((self.screen.width, self.screen.height - c.HEADERHEIGHT))

        self.headerRect: Rect = self.headerWindow.get_rect()
        self.boxRect: Rect = self.boxWindow.get_rect(topleft = (0, c.HEADERHEIGHT))

        # update gradients
        colors.InputBoxWindowGradient = colors.createGradient((1, 2), self.boxWindow.size, colors.Grey1, colors.Black)