from OpenGL.GL import *
import pg

class Window(pg.Window):
    def setup(self):
        self.font = pg.Font(self, 0, '/Library/Fonts/Arial.ttf', 24)
    def draw(self):
        self.clear()
        self.font.render('%.1f fps' % self.fps, (5, 0))

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
