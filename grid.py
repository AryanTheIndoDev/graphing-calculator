import math

import pygame as pg
from pygame import Surface, Color, Font, Vector2
from typing import Callable
import numpy as np

import colors
import constants as c

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
        self.maxScale: float = c.MAXSCALE
        self.unitLength: float = 2
        self.unitLengthMultiplier: int = 0

        # Screen
        self.width: int = 0
        self.height: int = 0

        # Panning
        self.panning: Vector2 = Vector2()

        # Graphs
        self.graphs: dict[tuple, Graph] = {}
        self.lineWidth: int = c.UNFOCUSEDLINEWIDTH

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
        if 0 <= self.origin.y <= self.height:
            pg.draw.line(screen, self.axisColor, (0, self.origin.y), (self.width, self.origin.y), 2)
        # y-axis
        if 0 <= self.origin.x <= self.width:
            pg.draw.line(screen, self.axisColor, (self.origin.x, 0), (self.origin.x, self.height), 2)

        # Graphs:-
        for function in self.graphs.keys():
            graph = self.graphs[function]
            if graph.plotable:
                sortedChains = graph.getSortedChains()
                for chain in sortedChains:
                    for chunk in chain:
                        if len(chunk) > 1:
                            # converting to np arrays 
                            xs, ys = map(np.array, zip(*chunk))

                            # converting to screen coords
                            xs = self.origin.x + xs * self.scale
                            ys = np.clip(self.origin.y - ys * self.scale, -self.lineWidth, self.height + self.lineWidth)
                            # print(ys)

                            # drawing the lines
                            pg.draw.lines(screen, colors.Green3, False, list(zip(xs.tolist(), ys.tolist())), self.lineWidth)

    def zoom(self, scroll: float, intensity: int, mousePos: Vector2, screen: Surface) -> None:
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
        deltaScale = scroll * (self.scale * intensity / 100)
        self.scale = pg.math.clamp(self.scale + deltaScale, self.scale + deltaScale, self.maxScale)

        newMathCoords = Vector2((mousePos.x - self.origin.x) / self.scale,
                                (self.origin.y - mousePos.y) / self.scale)

        # Increasing/Decreasing unit when displayScale gets uncomfortable
        self.changeResolution()

        # Panning screen towards mouse
        self.panning.x -= (oldMathCoords.x - newMathCoords.x) * self.scale
        self.panning.y += (oldMathCoords.y - newMathCoords.y) * self.scale

        # Updating graphs
        self.updateGraphs()

    def pan(self, movement: Vector2) -> None:
        """ Panning the grid by the mouse
        movement vector."""

        self.panning += movement
        self.updateGraphs()
    
    def addFunction(self, function: tuple[tuple, Callable]):
        if function[0] not in self.graphs.keys():

            startx = -self.origin.x / self.scale
            endx = (self.width - self.origin.x) / self.scale
            graph = Graph(function[1])

            if graph.plotable:
                graph.generate(startx, endx, (endx - startx) / self.width)

            self.graphs[function[0]] = graph

    def onResize(self, screen: Surface):
        self.width = screen.width
        self.height = screen.height

        # update graphs
        self.updateGraphs()

    def focusOn(self):
        self.focused: bool = True
        self.lineWidth: int = c.FOCUSEDLINEWIDTH

    def focusOff(self):
        self.focused: bool = False
        self.lineWidth: int = c.UNFOCUSEDLINEWIDTH

    # Helper Functions
    
    def drawMajorLines(self, screen: Surface) -> None:
        centerx = self.origin.x
        centery = self.origin.y

        # horizontal lines
        yrange = [math.floor(centery / self.displayScale), math.ceil((centery - screen.height) / self.displayScale)]

        for line in range(yrange[1], yrange[0] + 1):
            if line != 0:
                y = line * self.displayScale

                # lines
                pg.draw.line(screen, self.majorColor, (0, centery - y), (screen.width, centery - y))
                # number
                self.drawNum(line * self.unit, (centerx - 10, centery - y), screen, "y")

        # vertical lines
        xrange = [math.floor(-centerx / self.displayScale), math.ceil((screen.width - centerx) / self.displayScale)]
        for line in range(xrange[0], xrange[1] + 1):
            if line != 0:
                x = line * self.displayScale

                # lines
                pg.draw.line(screen, self.majorColor, (centerx + x, 0), (centerx + x, screen.height))
                # number
                self.drawNum(line * self.unit, (centerx + x, centery + 10), screen, "x")

    def drawMinorLines(self, screen: Surface) -> None:
        centerx = self.origin.x
        centery = self.origin.y

        minorScale = self.displayScale / 5

        # horizontal lines
        yrange = [math.floor(centery / minorScale), math.ceil((centery - screen.height) / minorScale)]
        for line in range(yrange[1], yrange[0] + 1):
            if line != 0:
                y = line * minorScale

                # lines
                pg.draw.line(screen, self.minorColor, (0, centery - y), (screen.width, centery - y))

        # vertical lines
        xrange = [math.floor(-centerx / minorScale), math.ceil((screen.width - centerx) / minorScale)]
        for line in range(xrange[0], xrange[1] + 1):
            if line != 0:
                x = line * minorScale

                # lines
                pg.draw.line(screen, self.minorColor, (centerx + x, 0), (centerx + x, screen.height))

    def drawNum(self, num: float, pos: Point, screen: Surface, axis: str) -> None:
        number = np.round(num, len(str(self.unit)))
        surf = self.font.render(f"{number}", True, self.axisColor)

        rect = surf.get_rect(center = pos)

        if axis == "x":
            rect.centery = pg.math.clamp(rect.centery, rect.height / 2, self.height - (rect.height / 2))
        elif axis == "y":
            rect.centerx = pg.math.clamp(rect.centerx, rect.width / 2, self.width - (rect.width / 2))
        
        screen.blit(surf, rect)

    def changeResolution(self) -> None:
        if self.displayScale <= c.MINIMUMDISPLAYSCALE:
            self.cycleUnitLength(1)
            self.regenerateGraphs()

        if self.displayScale >= c.MAXIMUMDISPLAYSCALE:
            self.cycleUnitLength(-1)
            self.regenerateGraphs()
        
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

    def updateGraphs(self):
        self.origin = Vector2(self.width // 2 + self.panning.x,
                         self.height // 2 + self.panning.y)

        startx = -self.origin.x / self.scale
        endx = (self.width - self.origin.x) / self.scale

        for function in self.graphs:
            if self.graphs[function].plotable:
                self.graphs[function].update(startx, endx, (endx - startx) / self.width)

    def regenerateGraphs(self):
        self.origin = Vector2(self.width // 2 + self.panning.x,
                         self.height // 2 + self.panning.y)

        startx = -self.origin.x / self.scale
        endx = (self.width - self.origin.x) / self.scale

        for function in self.graphs:
            if self.graphs[function].plotable:
                self.graphs[function].generate(startx, endx, (endx - startx) / self.width)
            