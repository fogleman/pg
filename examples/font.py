from OpenGL.GL import *
import pg

class Window(pg.Window):
    def setup(self):
        font = pg.FontTexture('Chalkduster.ttf', 72)
        self.context = pg.Context(pg.TextProgram())
        self.context.sampler = pg.Texture(0, font.im)
        position, uv = font.render((0, 0), 'Hello, world!')
        self.context.position = pg.VertexBuffer(position)
        self.context.uv = pg.VertexBuffer(uv)
    def update(self, t, dt):
        w, h = self.size
        self.context.matrix = pg.Matrix().orthographic(0, w, h, 0, -1, 1)
    def draw(self):
        self.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.context.draw(pg.GL_TRIANGLES)
        glDisable(GL_BLEND)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
