import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((0, 0, 3), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        shape = pg.OBJ('examples/suzanne.obj')
        position = pg.recenter(shape.position)
        normal = shape.normal
        smooth = pg.smooth_normals(position, normal)
        vb1 = pg.VertexBuffer(pg.interleave(position, normal))
        vb2 = pg.VertexBuffer(pg.interleave(position, smooth))
        self.data = [vb1.slices(3, 3), vb2.slices(3, 3)]
    def update(self, t, dt):
        self.context.position, self.context.normal = self.data[int(t % 2.0)]
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    pg.run(Window)
