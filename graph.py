import pygame as pg
import numpy as np
from decimal import Decimal

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
        self.points: list[dict[float, float]] = []

        self._sortedCache: list = []
        self._dirty: bool = True

        self.startx: float = 0
        self.endx: float = 0
        self.step: float = 0

        if self.function(np.array([1])) == None:
            self.plotable: bool = False
        else:
            self.plotable: bool = True

    def generate(self, startx: float, endx: float, step: float) -> None:
        # reset points
        self.points = []

        # solve for all
        xs = np.arange(startx, endx + step, step)
        xs = np.round(xs, self.getDecimalPlaces(step))
        chains = self.solve(xs)

        # assign points
        # self.points = dict(zip(xs.tolist(), ys.tolist()))
        for ys in chains:
            self.points.append(dict(zip(xs.tolist(), ys.tolist())))

        # setting the values
        self.startx = startx
        self.endx = endx
        self.step = step

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
            xs = np.arange(s2, s1 + step, step)
            xs = np.round(xs, self.getDecimalPlaces(step))
            chains = self.solve(xs)
            for index in range(len(self.points)):
                self.points[index].update(dict(zip(xs.tolist(), chains[index].tolist())))

        # end side
        if eIncrement > 0:
            xs = np.arange(e1, e2 + step, step)
            xs = np.round(xs, self.getDecimalPlaces(step))
            chains = self.solve(xs)
            for index in range(len(self.points)):
                self.points[index].update(dict(zip(xs.tolist(), chains[index].tolist())))

        for index in range(len(self.points)):
            self.points[index] = {x: y for x, y in self.points[index].items() if s2 <= x <= e2}
            print(len(self.points[index]))

        # setting the values
        self.startx = s2
        self.endx = e2
        self.step = step

        # setting self to dirty
        self._dirty = True

    def getSortedChains(self) -> list[list[list[tuple[float, float]]]]:
        if self._dirty:
            self._sortedCache = []
            for chain in self.points:
                sortedPoints = sorted(chain.items())

                # splitting the dict
                indices = []
                for i in range(1, len(sortedPoints) - 1):
                    curPoint = sortedPoints[i]
                    previousPoint = sortedPoints[i - 1]

                    if self.checkAsymptote(curPoint[1], previousPoint[1]):
                        indices += [i]

                indices = [0] + indices + [len(sortedPoints) - 1]
                chunks = [sortedPoints[indices[i]: indices[i+1]] for i in range(len(indices) - 1)]

                # removing the problematic first points
                chunks = [chunk[1:] if i != 0 else chunk for i, chunk in enumerate(chunks)]

                self._sortedCache.append(chunks)

            self._dirty = False

        return self._sortedCache

    # Helper Functions
    def solve(self, xs):
        chains = self.function(xs)

        for index in range(len(chains)):
            if np.isscalar(chains[index]):
                chains[index] = np.repeat(chains[index], len(xs))

        return chains

    def checkReal(self, val: float) -> bool:
        if np.isnan(val) or np.isinf(val):
            return False
        else:
            return True
        
    def checkAsymptote(self, val: float, previousVal: float) -> bool:
        if np.isnan(val) or np.isinf(val):
            return True
        elif np.abs(previousVal - val) > self.step * (10**4):
            return True
        else:
            return False

    def getDecimalPlaces(self, val: float):
        decimalVal = Decimal(str(val))
        return np.abs(decimalVal.as_tuple().exponent)