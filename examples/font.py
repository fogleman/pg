from OpenGL.GL import *
import pg

class Window(pg.Window):
    def setup(self):
        self.font = pg.Font(self, 0, '/Library/Fonts/Arial.ttf', 72)
    def draw(self):
        self.clear()
        w, h = self.size
        self.font.render('Hello, world!', (w / 2, h / 2), (0.5, 0.5))

if __name__ == "__main__":
    pg.run(Window)
