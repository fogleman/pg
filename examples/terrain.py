from collections import defaultdict
import pg

def noise(x, z):
    a = pg.simplex2(-x * 0.02, -z * 0.02, 4)
    b = pg.simplex2(x * 0.1, z * 0.1, 4)
    return (a + 1) * 8 + b

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=30)
        self.wasd.look_at((-20, 12, -8), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.object_color = (0.2, 0.8, 0.4)
        self.context.specular_multiplier = 0.3
        normals = defaultdict(list)
        position = []
        size = 50
        # generate height map
        height = {}
        for x in xrange(-size, size + 1):
            for z in xrange(-size, size + 1):
                height[(x, z)] = noise(x, z)
        # generate triangles and track normals for all vertices
        for x in xrange(-size, size):
            for z in xrange(-size, size):
                t1 = [x + 0, z + 0, x + 1, z + 0, x + 0, z + 1]
                t2 = [x + 0, z + 1, x + 1, z + 0, x + 1, z + 1]
                for t in [t1, t2]:
                    x1, z1, x2, z2, x3, z3 = t
                    p1 = (x1, height[(x1, z1)], z1)
                    p2 = (x2, height[(x2, z2)], z2)
                    p3 = (x3, height[(x3, z3)], z3)
                    position.extend([p3, p2, p1])
                    n = pg.normalize(pg.cross(pg.sub(p3, p1), pg.sub(p2, p1)))
                    normals[(x1, z1)].append(n)
                    normals[(x2, z2)].append(n)
                    normals[(x3, z3)].append(n)
        # compute average normal for all vertices
        normal = []
        for key, value in normals.items():
            normals[key] = pg.normalize(reduce(pg.add, value))
        for x, y, z in position:
            normal.append(normals[(x, z)])
        # generate vertex buffer
        self.context.position, self.context.normal = (
            pg.VertexBuffer(pg.interleave(position, normal)).slices(3, 3))
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 200)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
