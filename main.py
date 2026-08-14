import pygame as pg
from pygame import Surface, Clock, Color, Vector2, Rect

from grid import Grid

# Type Hint Declaration
type Point = tuple[int, int]

# Initializtion
pg.init()

# Titling
pg.display.set_caption("Graphing Calculator")

# Iconing
font = pg.font.SysFont("Segoe UI Emoji", 20)
icon: Surface = font.render("📈", True, Color(0, 0, 0, 0))

pg.display.set_icon(icon)

# Appstate
class AppState:
    INPUTWINDOWWIDTH: int = 200
    ZOOMINTESITY: int = 5

    def __init__(self) -> None:
        # Screen
        self.minWidth: int = 400
        self.minHeight: int = 0

        startingWidth: int = 800
        startingHeight: int = 600

        self.screen: Surface = pg.display.set_mode((startingWidth, startingHeight), pg.RESIZABLE)

        # Clock
        self.clock: Clock = Clock()

        # Screen components
        self.inputWindow: Surface = Surface((self.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)
        self.graphWindow: Surface = Surface((self.screen.width - self.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)

        self.inputRect: Rect = self.inputWindow.get_rect()
        self.graphRect: Rect = self.graphWindow.get_rect(topleft = (self.INPUTWINDOWWIDTH, 0))

        # Mouse
        self.mousePos: Vector2 = Vector2(pg.mouse.get_pos())
        self.mouseMovement: Vector2 = Vector2()
        self.mouseScroll: int = 0
        
        self.mouseJustPressed: tuple = pg.mouse.get_just_pressed()
        self.mousePressed: tuple = pg.mouse.get_pressed()

        # UI
        self.bgColor: Color = Color(0, 0, 0)

        self.gridPan: Vector2 = Vector2()
        self.grid: Grid = Grid(scale = 100, pan = self.gridPan)

        # Main loop vars
        self.running: bool = True

        self.fps: float = 60
        self.dt: float = 60 / 1000

    @property
    def width(self) -> int:
        return self.screen.width

    @property
    def height(self) -> int:
        return self.screen.height

    def update(self):
        # Mouse
        self.mouseMovement: Vector2 = pg.mouse.get_pos() - self.mousePos
        self.mousePos: Vector2 = Vector2(pg.mouse.get_pos())
        
        self.mouseJustPressed: tuple = pg.mouse.get_just_pressed()
        self.mousePressed: tuple = pg.mouse.get_pressed()

        # Panning
        if self.graphRect.collidepoint(self.mousePos):
            if self.mousePressed[0]:
                self.gridPan += self.mouseMovement

        # Zooming
        self.grid.zoom(self.mouseScroll, self.ZOOMINTESITY)
        self.mouseScroll = 0

    def draw(self):
        self.screen.fill(self.bgColor)
        self.graphWindow.fill(self.bgColor)

        self.grid.draw(self.graphWindow)

        self.screen.blit(self.inputWindow, self.inputRect)
        self.screen.blit(self.graphWindow, self.graphRect)

    def onResize(self, new_dimensions: Point):
        newWidth, newHeight = new_dimensions

        # clamping dimensions
        width: int = int(pg.math.clamp(newWidth, self.minWidth, newWidth))
        height: int = int(pg.math.clamp(newHeight, self.minHeight, newHeight))

        # resizing screen
        self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)

        # resizing screen components
        self.inputWindow: Surface = Surface((self.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)
        self.graphWindow: Surface = Surface((self.screen.width - self.INPUTWINDOWWIDTH, self.screen.height), pg.SRCALPHA)

    def quit(self):
        self.running: bool = False

app: AppState = AppState()

# main loop
while app.running:
    for event in pg.event.get():
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