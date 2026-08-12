import pygame as pg
from pygame import Surface, Clock, Color

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
    def __init__(self) -> None:
        # Pygame stuff
        self.width: int = 600
        self.height: int = 400

        self.screen: Surface = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        self.clock: Clock = Clock()

        # UI
        self.bgColor: Color = Color(0, 0, 0)

        # Main loop vars
        self.running: bool = True

        self.fps: float = 60
        self.dt: float = 60 / 1000

    def update(self):
        ...

    def draw(self):
        self.screen.fill(self.bgColor)

    def quit(self):
        self.running: bool = False

app: AppState = AppState()

# Main loop
while app.running:
    for event in pg.event.get():
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