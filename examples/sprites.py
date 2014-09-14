from math import sin, cos, pi
import pg

class Window(pg.Window):
    def setup(self):
        sheet = pg.SpriteSheet(0, '/Users/fogleman/Desktop/Sprites')
        self.batch = pg.SpriteBatch(sheet)
        n = 1000
        for y in range(-n, n + 1, 64):
            for x in range(-n, n + 1, 64):
                sprite = sheet.star(self.batch)
                sprite.position = (x, y)
        print len(self.batch.sprites)
    def update(self, t, dt):
        for sprite in self.batch.sprites:
            sprite.rotation = -t * 2
    def draw(self):
        w, h = self.size
        w, h = w / 2, h / 2
        matrix = pg.Matrix().orthographic(-w, w, -h, h, -1, 1)
        self.clear()
        self.batch.draw(matrix)

if __name__ == "__main__":
    pg.run(Window)
