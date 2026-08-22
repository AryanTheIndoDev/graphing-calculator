import pygame as pg
from pygame import Surface, Color, Font, Vector2
from typing import Callable

import colors

from graph import Graph

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

        # Screen
        self.width: int = 0
        self.height: int = 0

        # Panning
        self.panning: Vector2 = Vector2()

        # Graphs
        self.graphs: dict[Callable, Graph] = {}

        # Colors
        self.axisColor: Color = colors.White
        self.majorColor: Color = colors.MajorAxisColor
        self.minorColor: Color = colors.MinorAxisColor

        # Font
        self.font: Font = pg.font.SysFont("Cambria Math", 15)

    @property
    def unit(self) -> float:
        return self.unitLength * (10 ** self.unitLengthMultiplier)

    @property
    def displayScale(self) -> float:
        return self.scale * self.unit

    def draw(self, screen: Surface) -> None:
        # Dimensions
        self.width = screen.width
        self.height = screen.height

        self.origin = Vector2((screen.width // 2) + self.panning.x, (screen.height // 2) + self.panning.y)

        # Minor lines:-
        self.drawMinorLines(screen)

        # Major lines:-
        self.drawMajorLines(screen)

        # Axes:-
        # x-axis
        pg.draw.line(screen, self.axisColor, (0, self.origin.y), (self.width, self.origin.y), 2)
        # y-axis
        pg.draw.line(screen, self.axisColor, (self.origin.x, 0), (self.origin.x, self.height), 2)

        # Graphs:-
        for function in self.graphs:
            graph = self.graphs[function]
            sortedPoints = sorted(graph.points.items())
            xpoints = list(p[0] for p in sortedPoints)
            ypoints = list(p[1] for p in sortedPoints)
            for i in range(0, len(graph.points) - 2):
                x1 = xpoints[i]
                y1 = ypoints[i]
                x2 = xpoints[i + 1]
                y2 = ypoints[i + 1]

                pos1 = (self.origin.x + x1 * self.scale, self.origin.y - y1 * self.scale)
                pos2 = (self.origin.x + x2 * self.scale, self.origin.y - y2 * self.scale)

                pg.draw.line(screen, colors.Green3, pos1, pos2, 3)


    def zoom(self, scroll: int, intensity: int, mousePos: Vector2, screen: Surface) -> None:
        """Calcalute the old mathematical coords of mouse,
        calculate the new mathematical coords of the mouse,
        add their difference to panning"""

        self.origin = Vector2(screen.width // 2 + self.panning.x,
                         screen.height // 2 + self.panning.y)

        oldMathCoords = Vector2((mousePos.x - self.origin.x) / self.scale,
                                (self.origin.y - mousePos.y) / self.scale)

        """ Scroll is like the direction
        while the self.scale is scaled by
        a percentage of itself."""

        self.scale += scroll * (self.scale * intensity / 100)

        newMathCoords = Vector2((mousePos.x - self.origin.x) / self.scale,
                                (self.origin.y - mousePos.y) / self.scale)

        # Increasing/Decreasing unit when displayScale gets uncomfortable
        if self.displayScale <= 80:
            self.cycleUnitLength(1)

        if self.displayScale >= 160:
            self.cycleUnitLength(-1)

        # Panning screen towards mouse
        self.panning.x -= (oldMathCoords.x - newMathCoords.x) * self.scale
        self.panning.y += (oldMathCoords.y - newMathCoords.y) * self.scale

    def pan(self, movement: Vector2) -> None:
        """ Panning the grid by the mouse
        movement vector."""

        self.panning += movement

        self.origin = Vector2(self.width // 2 + self.panning.x,
                         self.height // 2 + self.panning.y)

        startx = -self.origin.x / self.scale
        endx = (self.width - self.origin.x) / self.scale

        for function in self.graphs:
            self.graphs[function].update(startx, endx, 10 ** (self.unitLengthMultiplier - 2))

    def addFunction(self, function: Callable):
        if function not in self.graphs:

            startx = -self.origin.x / self.scale
            endx = (self.width - self.origin.x) / self.scale
            graph = Graph(function)
            graph.generate(startx, endx, 10 ** (self.unitLengthMultiplier - 2))

            self.graphs[function] = graph

    # Helper Functions
    
    def drawMajorLines(self, screen: Surface) -> None:
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

    def drawMinorLines(self, screen: Surface) -> None:
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

    def cycleUnitLength(self, direction: int) -> None:
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

    def drawNum(self, num: float, pos: Point, screen: Surface) -> None:
        number = round(num, len(str(self.unit)))
        surf = self.font.render(f"{number}", True, self.axisColor)
        screen.blit(surf, surf.get_rect(center = pos))