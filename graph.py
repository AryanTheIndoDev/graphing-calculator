import pygame as pg
from typing import Callable

# Initialization
pg.init()

# Type Declaration
type Point = tuple[int, int]

# Graph
class Graph:
    def __init__(self, function: Callable) -> None:
        self.function: Callable = function

        # points
        self.points: dict[float, float] = {}

        self._sortedCache: list = []
        self._dirty: bool = True

        self.startx: float = 0
        self.endx: float = 0

        if self.function(1) == None:
            self.plotable: bool = False
        else:
            self.plotable: bool = True

    def generate(self, startx: float, endx: float, step: float) -> None:
        # reset points
        self.points = {}

        x = startx

        # generating points for each x
        while x < endx:
            y = float(self.function(x)[0])
            self.points[x] = y
            x += step

        # setting the values
        self.startx = startx
        self.endx = endx

        # setting self to dirty
        self._dirty = True

    def update(self, startx: float, endx: float, step: float) -> None:
        # getting the values in place
        s1 = self.startx
        e1 = self.endx

        s2 = startx
        e2 = endx

        # calculating increments to both sides
        sIncrement = s1 - s2
        eIncrement = e2 - e1

        # start side
        if sIncrement > 0:
            x = s1 - step
            while x > s2:
                y = float(self.function(x)[0])
                self.points[x] = y
                x -= step

        # end side
        if eIncrement > 0:
            x = e1 + step
            while x < e2:
                y = float(self.function(x)[0])
                self.points[x] = y
                x += step

        self.points = {x: y for x, y in self.points.items() if s2 <= x <= e2}

        # setting the values
        self.startx = s2
        self.endx = e2

        # setting self to dirty
        self._dirty = True


    def getSortedPoints(self) -> list:
        if self._dirty:
            self._sortedCache = sorted(self.points.items())
            self._dirty = False

        return self._sortedCache
