import pygame as pg
from pygame import Surface, Color, Font, Vector2

# Grid
class Grid:
    def __init__(self, scale: float) -> None:
        # Scaling
        self.scale: float = scale
        self.unitLength: float = 2
        self.unitLengthMultiplier: int = 0

        # Panning
        self.panning: Vector2 = Vector2()

        # Colors
        self.axisColor: Color = Color(255, 255, 255, 255)
        self.majorColor: Color = Color(200, 200, 200, 150)
        self.minorColor: Color = Color(100, 100, 100, 50)

        # Font
        self.font: Font = pg.font.SysFont("Cambria Math", 15)

    @property
    def unit(self) -> float:
        return self.unitLength * self.unitLengthMultiplier

    def draw(self, screen: Surface):
        # Dimensions
        width = screen.width
        height = screen.height

        centerWidth = (screen.width // 2) + self.panning.x
        centerHeight = (screen.height // 2) + self.panning.y

        # Minor lines:-
        self.drawMinorLines(screen)

        # Major lines:-
        self.drawMajorLines(screen)

        # Axes:-
        # x-axis
        pg.draw.line(screen, self.axisColor, (0, centerHeight), (width, centerHeight), 2)
        # y-axis
        pg.draw.line(screen, self.axisColor, (centerWidth, 0), (centerWidth, height), 2)
    
    def drawMajorLines(self, screen: Surface):
        centerx = screen.width // 2 + self.panning.x
        centery = screen.height // 2 + self.panning.y

        # horizontal
        for line in range(1, int(max(centery, screen.height - centery) / self.scale) + 1):
            y = line * self.scale

            # positive
            pg.draw.line(screen, self.majorColor, (0, centery - y), (screen.width, centery - y))
            # number
            num = self.font.render(f"{line * self.unitLength}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - 10, centery - y)))

            # negative
            pg.draw.line(screen, self.majorColor, (0, centery + y), (screen.width, centery + y))
            # number
            num = self.font.render(f"{-line * self.unitLength}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - 10, centery + y)))

        # vertical
        for line in range(1, int(max(centerx, screen.width - centerx) / self.scale) + 1):
            x = line * self.scale

            # positive
            pg.draw.line(screen, self.majorColor, (centerx + x, 0), (centerx + x, screen.height))
            # number
            num = self.font.render(f"{line * self.unitLength}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx + x, centery + 10)))

            # negative
            pg.draw.line(screen, self.majorColor, (centerx - x, 0), (centerx - x, screen.height))
            # number
            num = self.font.render(f"{-line * self.unitLength}", True, self.axisColor)
            screen.blit(num, num.get_rect(center = (centerx - x, centery + 10)))

    def drawMinorLines(self, screen: Surface):
        centerx = screen.width // 2 + self.panning.x
        centery = screen.height // 2 + self.panning.y

        # horizontal
        for line in range(1, int(max(centery, screen.height - centery) / (self.scale / 5)) + 1):
            y = line * self.scale / 5

            pg.draw.line(screen, self.minorColor, (0, centery + y), (screen.width, centery + y))
            pg.draw.line(screen, self.minorColor, (0, centery - y), (screen.width, centery - y))

        # vertical
        for line in range(1, int(max(centerx, screen.width - centerx) / (self.scale / 5)) + 1):
            x = line * self.scale / 5

            pg.draw.line(screen, self.minorColor, (centerx + x, 0), (centerx + x, screen.height))
            pg.draw.line(screen, self.minorColor, (centerx - x, 0), (centerx - x, screen.height))

    def zoom(self, scroll: int, intensity: int):
        """ Scroll is like the direction
        while the self.scale is scaled by
        a percentage of itself."""

        self.scale += scroll * (self.scale * intensity / 100)

    def pan(self, movement: Vector2):
        """ Panning the grid by the mouse
        movement vector."""

        self.panning += movement

    def cycleUnitLength(self, direction: int):
        lengths: list = [1, 2, 5]

        current: int =  lengths.index(self.unitLength)
        new: int = current + direction

        # looping
        if new > len(lengths) - 1:
            new = 0
        elif new < 0:
            new = len(lengths) - 1

        self.unitLength = lengths[new]