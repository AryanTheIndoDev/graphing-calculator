import pygame as pg


# Initialization
pg.init()

# Type Declaration
type Point = tuple[int, int]

# Graph
class Graph:
    def __init__(self, expr) -> None:
        self.expr = expr