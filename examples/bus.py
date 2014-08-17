import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=4)
        self.wasd.look_at((-3, 1, -6), (0, 0, -2))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.ambient_color = (0.7, 0.7, 0.7)
        self.context.light_color = (0.3, 0.3, 0.3)
        self.context.use_texture = True
        self.context.sampler = pg.Texture(0, 'examples/bus.jpg')
        self.mesh = pg.OBJ('examples/bus.obj').centered().smoothed()
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
