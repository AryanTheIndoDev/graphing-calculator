import pygame as pg
from pygame import Rect, Surface, Color, Font

# Type Declaration
type Point = tuple[int, int]

# InputBox
class InputBox:
    def __init__(self, dimensions: Point, font: Font) -> None:
        # text
        self.text: str = "y = x"
        self.font: Font = font
        self.color: Color = Color(200, 200, 200)

        # structure
        self.surf: Surface = Surface(dimensions, pg.SRCALPHA)

        self.rect: Rect = self.surf.get_rect()

    def draw(self, screen: Surface, pos: Point) -> None:
        # position
        self.rect.topleft = pos

        # text
        textSurf = self.font.render(self.text, True, self.color)
        textRect = textSurf.get_rect()

        textRect.left, textRect.centery = (10, self.rect.height // 2)

        self.surf.blit(textSurf, textRect)

        screen.blit(self.surf, self.rect)

        
    def getText(self, text: str) -> None:
        self.text += text