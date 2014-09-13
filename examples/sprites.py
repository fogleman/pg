import pg

class Window(pg.Window):
    def setup(self):
        self.sheet = pg.SpriteSheet('/Users/fogleman/Desktop/Sprites')
        self.sprite = self.sheet.rocket()
        self.context = pg.Context(pg.TextureProgram())
        self.context.sampler = self.sheet.texture(0)
    def update(self, t, dt):
        w, h = self.size
        self.context.matrix = pg.Matrix().orthographic(0, w, 0, h, -1, 1)
        self.sprite.rotation = t
        self.sprite.position = (w / 2, h / 2)
    def draw(self):
        self.clear()
        self.sprite.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
