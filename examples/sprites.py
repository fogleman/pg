from math import sin
import pg

class Window(pg.Window):
    def setup(self):
        self.sheet = pg.SpriteSheet('/Users/fogleman/Desktop/Sprites')
        self.sprites = [
            self.sheet.planet1(),
            self.sheet.planet2(),
            self.sheet.planet3(),
            self.sheet.planet4(),
        ]
        self.context = pg.Context(pg.TextureProgram())
        self.context.sampler = self.sheet.texture(0)
    def update(self, t, dt):
        w, h = self.size
        self.context.matrix = pg.Matrix().orthographic(0, w, 0, h, -1, 1)
        for i, sprite in enumerate(self.sprites):
            x = (i - 1.5) * sin(t) * 200
            sprite.position = (x + w / 2, h / 2)
            sprite.z = i / 10.0
    def draw(self):
        self.clear()
        for sprite in self.sprites:
            sprite.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
