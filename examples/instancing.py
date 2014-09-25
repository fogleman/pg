from ctypes import create_string_buffer
from OpenGL.GL import *
import pg

class DataTexture(object):
    def __init__(self, size):
        self.size = size
        self.data = create_string_buffer(self.size)
        self.handle = glGenTextures(1)
        self.bind()
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage1D(
            GL_TEXTURE_1D, 0, GL_RGBA, self.size, 0, GL_RGBA,
            GL_UNSIGNED_BYTE, None)
        self.update()
    def update(self):
        self.bind()
        glTexSubImage1D(
            GL_TEXTURE_1D, 0, 0, self.size, GL_RGBA, GL_UNSIGNED_BYTE,
            self.data)
    def get_uniform_value(self):
        return 0
    def bind(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, self.handle)

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=10)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        sphere = pg.Sphere(4, 0.5, (0, 0, 0))
        self.texture = DataTexture(256 * 4)
        self.context = pg.Context(Program())
        self.context.sampler = self.texture
        self.context.position = pg.VertexBuffer(sphere.positions)
        self.context.normal = pg.VertexBuffer(sphere.normals)
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 10000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
        for i in xrange(256):
            self.texture.data[i * 4] = chr(i % 256)
            self.texture.data[i * 4 + 1] = chr(i % 256)
        self.texture.update()
    def draw(self):
        self.clear()
        self.context.draw(instances=256)

class Program(pg.BaseProgram):
    VS = '''
    #version 150

    uniform mat4 matrix;
    uniform mat4 model_matrix;
    uniform mat4 normal_matrix;
    uniform sampler1D sampler;

    in vec4 position;
    in vec3 normal;

    out vec3 frag_position;
    out vec3 frag_normal;

    void main() {
        vec4 data = texture(sampler, gl_InstanceID / 255.0);
        mat4 translate = mat4(
            vec4(1, 0, 0, 0),
            vec4(0, 1, 0, 0),
            vec4(0, 0, 1, 0),
            vec4(data.r * 256, data.g, 0, 1)
        );
        gl_Position = matrix * translate * position;
        frag_position = vec3(translate * position);
        frag_normal = mat3(normal_matrix) * normal;
    }
    '''
    FS = '''
    #version 150

    uniform vec3 camera_position;
    uniform vec3 light_direction;
    uniform vec3 object_color;
    uniform vec3 ambient_color;
    uniform vec3 light_color;
    uniform float specular_power;
    uniform float specular_multiplier;

    in vec3 frag_position;
    in vec3 frag_normal;
    out vec4 frag_color;

    void main() {
        vec3 color = object_color;
        float diffuse = max(dot(frag_normal, light_direction), 0.0);
        float specular = 0.0;
        if (diffuse > 0.0) {
            vec3 camera_vector = normalize(camera_position - frag_position);
            specular = pow(max(dot(camera_vector,
                reflect(-light_direction, frag_normal)), 0.0), specular_power);
        }
        vec3 light = ambient_color + light_color * diffuse +
            specular * specular_multiplier;
        frag_color = vec4(min(color * light, vec3(1.0)), 1.0);
    }
    '''
    def set_defaults(self, context):
        context.model_matrix = pg.Matrix()
        context.normal_matrix = pg.Matrix().inverse().transpose()
        context.light_direction = pg.normalize((1, 1, 1))
        context.object_color = (0.4, 0.6, 0.8)
        context.ambient_color = (0.3, 0.3, 0.3)
        context.light_color = (0.7, 0.7, 0.7)
        context.specular_power = 32.0
        context.specular_multiplier = 1.0
        context.use_texture = False
        context.use_color = False

if __name__ == "__main__":
    pg.run(Window)
