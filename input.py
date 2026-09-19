import pygame as pg
from pygame import Surface, Rect, Font, Vector2
from typing import Callable

import colors
import constants as c

from inputBox import InputBox

type Point = tuple[int, int]

# InputBox adder
class boxAdder:
    def __init__(self) -> None:
        self.rect: Rect = Rect()

        self.border: int = 6

        self.hovered: bool = False

        self.color = colors.Grey1
        self.hoveredColor = colors.Grey2
        self.iconColor = colors.Grey4
        self.hoveredIconColor = colors.Green2

    def draw(self, screen: Surface, pos: Point, dimensions: Point):
        # owning dimensions
        self.rect.size = dimensions
        self.rect.topleft = pos

        # creating the surf with border
        surf = Surface((dimensions[0] - 2 * self.border, dimensions[1] - self.border), pg.SRCALPHA)
        innerRect = surf.get_rect()

        # filling the surf with rounded rect
        if self.hovered:
            bgCol = self.hoveredColor
            iconCol = self.hoveredIconColor
        else:
            bgCol = self.color
            iconCol = self.iconColor

        pg.draw.rect(surf, bgCol, innerRect, 0, 5)
        
        # drawing the icon (order: Vertical, Horizontal)
        w = c.PLUSVERTICALRECTWIDTH
        h = c.PLUSVERTICALRECTHEIGHT
        b = c.PLUSBORDERWIDTH
        pg.draw.rect(surf, iconCol, ((surf.width // 2) - (w // 2), (surf.height // 2) - (h // 2), w, h), 0, b)
        pg.draw.rect(surf, iconCol, ((surf.width // 2) - (h // 2), (surf.height // 2) - (w // 2), h, w), 0, b)

        # blitting on screen
        screen.blit(surf, (pos[0] + self.border, pos[1] + self.border))

    def update(self, mousePos: Vector2, mouseClicked: bool) -> bool:
        # hovering
        if self.rect.collidepoint(mousePos):
            if mouseClicked:
                self.hovered = False
                return True
            self.hovered = True
        else:
            self.hovered = False

        return False
    
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

        self.boxAdder: boxAdder = boxAdder()

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

        self.boxAdder.draw(self.boxWindow, (0, len(self.boxes) * c.BOXHEIGHT), (self.screen.width, c.BOXHEIGHT))

        self.screen.blit(self.boxWindow, self.boxRect)

        # dividers
        # auxiliary
        pg.draw.line(self.screen, colors.Grey2, (0, c.HEADERHEIGHT), (self.screen.width, c.HEADERHEIGHT), 2)
        # main
        pg.draw.line(self.screen, colors.Grey5, (0, 0), (0, self.screen.height), 3)
        pg.draw.line(self.screen, colors.Grey5, (self.screen.width, 0), (self.screen.width, self.screen.height), 6)

    def update(self, keyPresses: pg.key.ScancodeWrapper, events: list[pg.Event], mousePos: Vector2, dt: float) -> None:
        functions: list = []
        LMBdown = False

        # handle focusing
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LMBdown = True

        if LMBdown:
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

        # boxAdder
        if self.boxAdder.update(mousePos - Vector2(0, c.HEADERHEIGHT), LMBdown):
            self.addBox()

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
