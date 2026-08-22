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
        self.points: dict[float, float] = {}

        self.startx: float = 0
        self.endx: float = 0

    def generate(self, startx: float, endx: float, step: float) -> None:
        x = startx

        # generating points for each x
        while x < endx:
            y = self.function(x)[0]
            self.points[x] = y
            x += step

        # setting the values
        self.startx = startx
        self.endx = endx

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
                y = self.function(x)[0]
                self.points[x] = y
                x -= step

        # end side
        if eIncrement > 0:
            x = e1 + step
            while x < e2:
                y = self.function(x)[0]
                self.points[x] = y
                x += step

        # setting the values
        self.startx = s2
        self.endx = e2
