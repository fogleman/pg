import pg
import random

PIPES = 8
SIZE = 16
UPDATE_RATE = 0.05
RESTART_RATE = 30

DIRECTIONS = [
    (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1),
]

COLORS = [
    0x1f77b4, 0xaec7e8, 0xff7f0e, 0xffbb78, 0x2ca02c,
    0x98df8a, 0xd62728, 0xff9896, 0x9467bd, 0xc5b0d5,
    0x8c564b, 0xc49c94, 0xe377c2, 0xf7b6d2, 0x7f7f7f,
    0xc7c7c7, 0xbcbd22, 0xdbdb8d, 0x17becf, 0x9edae5,
]

SPHERE = pg.Sphere(2, 0.25, (0, 0, 0))

CYLINDERS = [
    pg.Cylinder((-0.5, 0, 0), (0.5, 0, 0), 0.25, 18, True),
    pg.Cylinder((0, -0.5, 0), (0, 0.5, 0), 0.25, 18, True),
    pg.Cylinder((0, 0, -0.5), (0, 0, 0.5), 0.25, 18, True),
]

def add_cylinder(vb, position, axis):
    mesh = pg.Matrix().translate(position) * CYLINDERS[axis]
    vb.extend(pg.interleave(mesh.position, mesh.normal))

def add_sphere(vb, position):
    mesh = pg.Matrix().translate(position) * SPHERE
    vb.extend(pg.interleave(mesh.position, mesh.normal))

class Pipe(object):
    def __init__(self, occupied):
        self.occupied = occupied
        self.vb = pg.VertexBuffer()
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.object_color = pg.hex_color(random.choice(COLORS))
        self.context.position, self.context.normal = self.vb.slices(3, 3)
        self.restart()
    def restart(self):
        while True:
            x = random.randint(-SIZE, SIZE)
            y = random.randint(-SIZE, SIZE)
            z = random.randint(-SIZE, SIZE)
            if (x, y, z) not in self.occupied:
                break
        self.position = (x, y, z)
        self.direction = random.choice(DIRECTIONS)
        self.occupied.add(self.position)
        add_sphere(self.vb, self.position)
    def update(self):
        x, y, z = self.position
        directions = list(DIRECTIONS)
        random.shuffle(directions)
        if random.random() < 0.7:
            directions.remove(self.direction)
            directions.insert(0, self.direction)
        for direction in directions:
            dx, dy, dz = direction
            nx, ny, nz = x + dx, y + dy, z + dz
            if nx < -SIZE or ny < -SIZE or nz < -SIZE:
                continue
            if nx > SIZE or ny > SIZE or nz > SIZE:
                continue
            if (nx, ny, nz) in self.occupied:
                continue
            self.position = (nx, ny, nz)
            self.occupied.add(self.position)
            mx, my, mz = x + dx / 2.0, y + dy / 2.0, z + dz / 2.0
            axis = map(bool, direction).index(True)
            add_cylinder(self.vb, (mx, my, mz), axis)
            if direction != self.direction:
                add_sphere(self.vb, (x, y, z))
            self.direction = direction
            return
        self.restart()

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=10)
        self.wasd.look_at((SIZE + 10, 0, 0), (0, 0, 0))
        self.pipes = []
        self.restart()
        self.last_update = 0
        self.last_restart = 0
    def restart(self):
        for pipe in self.pipes:
            pipe.vb.delete()
        occupied = set()
        self.pipes = [Pipe(occupied) for _ in xrange(PIPES)]
    def update(self, t, dt):
        if t - self.last_restart >= RESTART_RATE:
            self.last_restart += RESTART_RATE
            self.restart()
        if t - self.last_update >= UPDATE_RATE:
            self.last_update += UPDATE_RATE
            for pipe in self.pipes:
                pipe.update()
    def draw(self):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.clear()
        for pipe in self.pipes:
            pipe.context.matrix = matrix
            pipe.context.camera_position = self.wasd.position
            pipe.context.draw()

if __name__ == "__main__":
    pg.run(Window)
