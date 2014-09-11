from math import pi, sin
import pg

SCALE = 128
CIRCLE_SIZE = SCALE * 2
CIRCLE_SPACING = SCALE * 1
GRID_SIZE = 11
SPEED = 1.0
OFFSET_MULTIPLIER = 1.0

class Window(pg.Window):
    def setup(self):
        plane = pg.Plane((0, 0, 0), (0, 0, 1), 1)
        self.context = pg.Context(Program())
        self.context.position = pg.VertexBuffer(plane.positions)
        self.context.matrix = pg.Matrix().orthographic(-1, 1, -1, 1, -1, 1)
        self.positions = []
        n = GRID_SIZE
        m = CIRCLE_SPACING
        for i in xrange(n):
            for j in xrange(n):
                x = (i - (n - 1) / 2.0) * m
                y = (j - (n - 1) / 2.0) * m
                d = (x * x + y * y) ** 0.5
                self.positions.append((x, y, d))
        self.max_distance = max(x[-1] for x in self.positions)
    def circles(self):
        result = []
        for x, y, d in self.positions:
            t = d / self.max_distance * pi * OFFSET_MULTIPLIER
            r = sin(t + self.t * -SPEED) * CIRCLE_SIZE
            result.append((x, y, r))
        return result
    def draw(self):
        self.clear()
        self.context.w, self.context.h = self.size
        self.context.circles = self.circles()
        self.context.draw()

class Program(pg.BaseProgram):
    VS = '''
    #version 120

    uniform mat4 matrix;
    attribute vec4 position;

    void main() {
        gl_Position = matrix * position;
    }
    '''
    FS = '''
    #version 120

    uniform float w;
    uniform float h;
    uniform vec3 circles[256];

    void main() {
        int count = 0;
        vec2 point = gl_FragCoord.xy - vec2(w / 2.0, h / 2.0);
        for (int i = 0; i < 256; i++) {
            if (distance(point, circles[i].xy) <= circles[i].z) {
                count++;
            }
        }
        gl_FragColor = vec4(mod(count, 2));
    }
    '''

if __name__ == "__main__":
    pg.run(Window)
