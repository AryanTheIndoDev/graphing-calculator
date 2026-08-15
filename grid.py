import pygame as pg
from pygame import Surface, Color, Font, Vector2

# Type Declaration
type Point = tuple[float, float]

# Grid
class Grid:
    def __init__(self, scale: float) -> None:
        # Scaling
        """scale is the pixels per unit
        displayScale is that times the unit
        unit = unitLength * 10 ^ unitLengthMult"""

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
        return self.unitLength * (10 ** self.unitLengthMultiplier)

    @property
    def displayScale(self) -> float:
        return self.scale * self.unit

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

    def zoom(self, scroll: int, intensity: int, mousePos: Vector2, screen: Surface):
        """ Scroll is like the direction
        while the self.scale is scaled by
        a percentage of itself."""

        self.scale += scroll * (self.scale * intensity / 100)

        # Increasing/Decreasing unit when displayScale gets uncomfortable
        if self.displayScale <= 80:
            self.cycleUnitLength(1)

        if self.displayScale >= 160:
            self.cycleUnitLength(-1)

        """Unfinished, Postponed to tomorrow"""
        # Panning screen towards mouse
        # origin = Vector2((screen.width // 2) + self.panning.x,
        #                  (screen.height // 2) + self.panning.y)

        # self.panning += -scroll * (mousePos - origin) * intensity / 100

    def pan(self, movement: Vector2):
        """ Panning the grid by the mouse
        movement vector."""

        self.panning += movement

    # Helper Functions
    
    def drawMajorLines(self, screen: Surface):
        centerx = screen.width // 2 + self.panning.x
        centery = screen.height // 2 + self.panning.y

        # vertical
        for line in range(1, int(max(centery, screen.height - centery) / self.displayScale) + 1):
            y = line * self.displayScale

            # positive
            pg.draw.line(screen, self.majorColor, (0, centery - y), (screen.width, centery - y))
            # number
            self.drawNum(line * self.unit, (centerx - 10, centery - y), screen)

            # negative
            pg.draw.line(screen, self.majorColor, (0, centery + y), (screen.width, centery + y))
            # number
            self.drawNum(-line * self.unit, (centerx - 10, centery + y), screen)

        # horizontal
        for line in range(1, int(max(centerx, screen.width - centerx) / self.displayScale) + 1):
            x = line * self.displayScale

            # positive
            pg.draw.line(screen, self.majorColor, (centerx + x, 0), (centerx + x, screen.height))
            # number
            self.drawNum(line * self.unit, (centerx + x, centery + 10), screen)

            # negative
            pg.draw.line(screen, self.majorColor, (centerx - x, 0), (centerx - x, screen.height))
            # number
            self.drawNum(-line * self.unit, (centerx - x, centery + 10), screen)

    def drawMinorLines(self, screen: Surface):
        centerx = screen.width // 2 + self.panning.x
        centery = screen.height // 2 + self.panning.y

        # vertical
        for line in range(1, int(max(centery, screen.height - centery) / (self.displayScale / 5)) + 1):
            y = line * self.displayScale / 5

            pg.draw.line(screen, self.minorColor, (0, centery + y), (screen.width, centery + y))
            pg.draw.line(screen, self.minorColor, (0, centery - y), (screen.width, centery - y))

        # horizontal
        for line in range(1, int(max(centerx, screen.width - centerx) / (self.displayScale / 5)) + 1):
            x = line * self.displayScale / 5

            pg.draw.line(screen, self.minorColor, (centerx + x, 0), (centerx + x, screen.height))
            pg.draw.line(screen, self.minorColor, (centerx - x, 0), (centerx - x, screen.height))

    def cycleUnitLength(self, direction: int):
        lengths: list = [1, 2, 5]

        current: int =  lengths.index(self.unitLength)
        new: int = current + direction

        # looping
        if new > len(lengths) - 1:
            new = 0
            self.unitLengthMultiplier += 1
        elif new < 0:
            new = len(lengths) - 1
            self.unitLengthMultiplier -= 1

        self.unitLength = lengths[new]

    def drawNum(self, num: float, pos: Point, screen: Surface):
        number = round(num, len(str(self.unit)))
        surf = self.font.render(f"{number}", True, self.axisColor)
        screen.blit(surf, surf.get_rect(center = pos))