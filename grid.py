import pygame as pg
from pygame import Surface, Color, Font

# Grid
class Grid:
    def __init__(self, scale: float, zoom: float = 1) -> None:
        # Scaling
        self.scale: float = scale
        self.zoom: float = zoom

        # Colors
        self.axisColor: Color = Color(255, 255, 255, 255)
        self.majorColor: Color = Color(200, 200, 200, 150)
        self.minorColor: Color = Color(100, 100, 100, 50)

        # Font
        self.font: Font = pg.font.SysFont("Cambria Math", 15)

    def draw(self, screen: Surface):
        # Dimensions
        width: int = screen.width
        height: int = screen.height

        # Minor lines:-
        self.drawMinorLines(screen)

        # Major lines:-
        self.drawMajorLines(screen)

        # Axes:-
        # x-axis
        pg.draw.line(screen, self.axisColor, (0, height // 2), (width, height // 2), 2)
        # y-axis
        pg.draw.line(screen, self.axisColor, (width // 2, 0), (width // 2, height), 2)
    
    def drawMajorLines(self, screen: Surface):
        centerx = screen.width // 2
        centery = screen.height // 2

        # horizontal
        for line in range(1, int((screen.height / 2) / self.scale) + 1):
            y = line * self.scale

            # positive
            pg.draw.line(screen, self.majorColor, (0, centery - y), (screen.width, centery - y))
            # number
            num = self.font.render(f"{line}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - 10, centery - y)))

            # negative
            pg.draw.line(screen, self.majorColor, (0, centery + y), (screen.width, centery + y))
            # number
            num = self.font.render(f"{-line}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - 10, centery + y)))

        # vertical
        for line in range(1, int((screen.width / 2) / self.scale) + 1):
            x = line * self.scale

            # positive
            pg.draw.line(screen, self.majorColor, (centerx + x, 0), (centerx + x, screen.height))
            # number
            num = self.font.render(f"{line}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx + x, centery + 10)))

            # negative
            pg.draw.line(screen, self.majorColor, (centerx - x, 0), (centerx - x, screen.height))
            # number
            num = self.font.render(f"{-line}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - x, centery + 10)))

    def drawMinorLines(self, screen: Surface):
        centerx = screen.width // 2
        centery = screen.height // 2

        # horizontal
        for line in range(1, int((screen.height / 2) / (self.scale / 5)) + 1):
            y = line * self.scale / 5

            pg.draw.line(screen, self.minorColor, (0, centery + y), (screen.width, centery + y))
            pg.draw.line(screen, self.minorColor, (0, centery - y), (screen.width, centery - y))

        # vertical
        for line in range(1, int((screen.width / 2) / (self.scale / 5)) + 1):
            x = line * self.scale / 5

            pg.draw.line(screen, self.minorColor, (centerx + x, 0), (centerx + x, screen.height))
            pg.draw.line(screen, self.minorColor, (centerx - x, 0), (centerx - x, screen.height))

