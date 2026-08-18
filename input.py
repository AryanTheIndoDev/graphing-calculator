import pygame as pg
from pygame import Surface, Color, Rect, Font

import colors

from inputBox import InputBox

# Input
class Input:
    BOXHEIGHT: int = 100
    HEADERHEIGHT: int = 80
    def __init__(self, screen: Surface) -> None:
        # Screen
        self.screen: Surface = screen

        # Boxes
        self.boxes: list[InputBox] = []
        self.font: Font = pg.font.SysFont("Cambria Math", 20)
        self.headerFont: Font = pg.font.SysFont("Corbel", 40, bold = True)

        # Screen Components
        self.headerWindow: Surface = Surface((self.screen.width, self.HEADERHEIGHT))
        self.boxWindow: Surface = Surface((self.screen.width, self.screen.height - self.HEADERHEIGHT))

        self.headerRect: Rect = self.headerWindow.get_rect()
        self.boxRect: Rect = self.boxWindow.get_rect(topleft = (0, self.HEADERHEIGHT))

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
            box.draw(self.boxWindow, (0, index * self.BOXHEIGHT))

        # divider
        pg.draw.line(self.screen, colors.Grey3, (0, self.HEADERHEIGHT), (self.screen.width, self.HEADERHEIGHT))

    def addBox(self) -> None:
        box = InputBox((self.screen.width, self.BOXHEIGHT), self.font)
        self.boxes.append(box)

    def onResize(self, screen: Surface):
        # update screen
        self.screen = screen

        # updating screen components
        self.headerWindow: Surface = Surface((self.screen.width, self.HEADERHEIGHT))
        self.boxWindow: Surface = Surface((self.screen.width, self.screen.height - self.HEADERHEIGHT))

        self.headerRect: Rect = self.headerWindow.get_rect()
        self.boxRect: Rect = self.boxWindow.get_rect(topleft = (0, self.HEADERHEIGHT))