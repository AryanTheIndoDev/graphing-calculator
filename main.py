import pygame as pg
from pygame import Surface, Clock, Color, Vector2, Rect

import colors
import constants as c

from grid import Grid
from input import Input

# Type Hint Declaration
type Point = tuple[int, int]

# Initializtion
pg.init()

# Titling
pg.display.set_caption("Graphity")

# Iconing
font = pg.font.SysFont("Segoe UI Emoji", 20)
icon: Surface = font.render("📈", True, Color(0, 0, 0, 0))

pg.display.set_icon(icon)

# Appstate
class AppState:
    def __init__(self) -> None:
        # Screen
        self.minWidth: int = 500
        self.minHeight: int = 200

        self.screen: Surface = pg.display.set_mode((c.STARTINGWIDTH, c.STARTINGHEIGHT), pg.RESIZABLE)

        # Clock
        self.clock: Clock = Clock()

        # Screen components
        self.inputWindow: Surface = Surface((c.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)
        self.graphWindow: Surface = Surface((self.screen.width - c.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)

        self.inputRect: Rect = self.inputWindow.get_rect()
        self.graphRect: Rect = self.graphWindow.get_rect(topleft = (c.INPUTWINDOWWIDTH, 0))

        # Input
        self.input: Input = Input(self.inputWindow)

        # Mouse
        self.mousePos: Vector2 = Vector2(pg.mouse.get_pos())
        self.mouseMovement: Vector2 = Vector2()
        self.mouseScroll: int = 0
        
        self.mouseJustPressed: tuple = pg.mouse.get_just_pressed()
        self.mousePressed: tuple = pg.mouse.get_pressed()

        # Keyboard
        self.keyPressed: pg.key.ScancodeWrapper = pg.key.get_pressed()

        # UI
        self.bgColor: Color = colors.Black

        self.grid: Grid = Grid(scale = 50)

        # Event handling
        self.events: list[pg.Event] = []

        # Main loop vars
        self.running: bool = True

        self.fps: float = 60
        self.dt: float = 0

    @property
    def width(self) -> int:
        return self.screen.width

    @property
    def height(self) -> int:
        return self.screen.height

    def update(self) -> None:
        # Mouse
        self.mouseMovement: Vector2 = pg.mouse.get_pos() - self.mousePos
        self.mousePos: Vector2 = Vector2(pg.mouse.get_pos())
        
        self.mouseJustPressed: tuple = pg.mouse.get_just_pressed()
        self.mousePressed: tuple = pg.mouse.get_pressed()

        # Keyboard
        self.keyPressed: pg.key.ScancodeWrapper = pg.key.get_pressed()

        # Grid Features
        if self.graphRect.collidepoint(self.mousePos):
            # Panning
            if self.mousePressed[0]:
                self.grid.pan(self.mouseMovement)
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

            # Zooming
            if self.mouseScroll != 0:
                relMousePos = self.mousePos - Vector2(self.graphRect.topleft)
                if pg.key.get_pressed()[pg.K_LCTRL]:
                    zoom = c.ZOOMINTENSITY * 5
                else:
                    zoom = c.ZOOMINTENSITY

                self.grid.zoom(self.mouseScroll, zoom, relMousePos, self.graphWindow)

        # Input Features
        if self.mouseJustPressed[1]:
            self.input.addBox()

        self.input.update(self.keyPressed, self.events, self.mousePos, self.dt)

        # Plotting
        for function in self.input.functions:
            if function[0] not in list(self.grid.graphs.keys()):
                self.grid.addFunction(function)

        currentKeys = [f[0] for f in self.input.functions]
        for key in list(self.grid.graphs.keys()):
            if key not in currentKeys:
                self.grid.graphs.pop(key)

        # Reset states
        self.mouseScroll = 0
        
    def draw(self) -> None:
        # Resetting surfaces
        self.screen.fill(self.bgColor)
        self.graphWindow.fill(self.bgColor)
        self.inputWindow.fill(self.bgColor)

        # Screen components
        self.grid.draw(self.graphWindow)
        self.input.draw()

        # Screen
        self.screen.blit(self.inputWindow, self.inputRect)
        self.screen.blit(self.graphWindow, self.graphRect)

    def onResize(self, new_dimensions: Point) -> None:
        newWidth, newHeight = new_dimensions

        # clamping dimensions
        width: int = int(pg.math.clamp(newWidth, self.minWidth, newWidth))
        height: int = int(pg.math.clamp(newHeight, self.minHeight, newHeight))

        # resizing screen
        self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)

        # resizing screen components
        self.inputWindow: Surface = Surface((c.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)
        self.graphWindow: Surface = Surface((self.screen.width - c.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)

        # resizing component rects
        self.inputRect: Rect = self.inputWindow.get_rect()
        self.graphRect: Rect = self.graphWindow.get_rect(topleft = (c.INPUTWINDOWWIDTH, 0))

        # parts
        self.grid.onResize(self.graphWindow)
        self.input.onResize(self.inputWindow)

    def quit(self) -> None:
        self.running: bool = False

app: AppState = AppState()

# main loop
while app.running:
    app.events = pg.event.get()
    for event in app.events:
        # mouse scroll
        if event.type == pg.MOUSEWHEEL:
            app.mouseScroll = event.y
        # resize
        if event.type == pg.VIDEORESIZE:
            app.onResize(event.size)
        # quit
        if event.type == pg.QUIT:
            app.quit()

    # update
    app.update()

    # draw
    app.draw()

    # pygame stuff
    pg.display.update()
    app.dt = app.clock.tick(app.fps) / 1000

pg.quit()