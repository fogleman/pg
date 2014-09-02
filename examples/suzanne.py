import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((0, 0, 3), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        mesh1 = pg.OBJ('examples/suzanne.obj').center()
        mesh2 = mesh1.smooth_normals()
        self.meshes = [mesh1, mesh2]
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        mesh = self.meshes[int(self.t % len(self.meshes))]
        mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
