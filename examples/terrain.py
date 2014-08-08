from collections import defaultdict
import pg

def noise(x, z):
    a = pg.simplex2(-x * 0.02, -z * 0.02, 2)
    b = pg.simplex2(x * 0.1, z * 0.1, 2)
    return (a + 1) * 6 + b

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=30)
        self.wasd.look_at((-20, 12, -8), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.object_color = (0.2, 0.8, 0.4)
        normals = defaultdict(list)
        position = []
        size = 50
        height = {}
        for x in xrange(-size, size + 1):
            for z in xrange(-size, size + 1):
                height[(x, z)] = noise(x, z)
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
        normal = []
        for key, value in normals.items():
            normals[key] = pg.normalize(reduce(pg.add, value))
        for x, y, z in position:
            normal.append(normals[(x, z)])
        self.context.position, self.context.normal = (
            pg.VertexBuffer(pg.interleave(position, normal)).slices(3, 3))
    def update(self, t, dt):
        matrix = pg.Matrix()
        normal_matrix = matrix.inverse().transpose()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.normal_matrix = normal_matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window((800, 600))
    app.run()
