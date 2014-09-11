from math import pi, sin
import pg

SCALE = 220
CIRCLE_SIZE = SCALE * 3
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
            r = (sin(t + self.t * -SPEED) + 1) / 2.0 * CIRCLE_SIZE
            result.append((x, y, r))
        return result
    def draw(self):
        self.clear()
        self.context.w, self.context.h = self.framebuffer_size
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
    uniform vec3 circles[128];

    const vec4 palette[4] = vec4[4](
        vec4(0.13, 0.71, 0.69, 1.00),
        vec4(0.98, 0.76, 0.08, 1.00),
        vec4(0.94, 0.42, 0.00, 1.00),
        vec4(0.94, 0.06, 0.11, 1.00)
    );

    void main() {
        int count = 0;
        vec2 point = gl_FragCoord.xy - vec2(w / 2.0, h / 2.0);
        for (int i = 0; i < 128; i++) {
            if (distance(point, circles[i].xy) <= circles[i].z) {
                count++;
            }
        }
        if (mod(count, 2) == 0) {
            gl_FragColor = vec4(0, 0, 0, 1);
        }
        else {
            gl_FragColor = palette[int(mod(count / 2, palette.length()))];
        }
    }
    '''

if __name__ == "__main__":
    pg.run(Window)
