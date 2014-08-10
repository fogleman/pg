from OpenGL.GL import *
import pg

class Window(pg.Window):
    def setup(self):
        self.font = pg.Font(0, 'Arial.ttf', 72)
    def draw(self):
        self.clear()
        w, h = self.size
        x, y = w / 2, h / 2
        self.font.render('Hello, world!', self.size, (x, y), (0.5, 0.5))

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
