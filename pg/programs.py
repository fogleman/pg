from core import Program
from util import normalize

class BaseProgram(Program):
    def __init__(self):
        return super(BaseProgram, self).__init__(self.VS, self.FS)

class SolidColorProgram(BaseProgram):
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

    uniform vec3 color;

    void main() {
        gl_FragColor = vec4(color, 1.0);
    }
    '''
    def set_defaults(self, context):
        context.color = (1.0, 1.0, 1.0)

class DirectionalLightProgram(BaseProgram):
    VS = '''
    #version 120

    uniform mat4 matrix;

    attribute vec4 position;
    attribute vec3 normal;
    attribute vec2 uv;
    attribute vec3 color;

    varying vec3 frag_position;
    varying vec3 frag_normal;
    varying vec2 frag_uv;
    varying vec3 frag_color;

    void main() {
        gl_Position = matrix * position;
        frag_position = vec3(position);
        frag_normal = normal;
        frag_uv = uv;
        frag_color = color;
    }
    '''
    FS = '''
    #version 120

    uniform sampler2D sampler;
    uniform mat4 normal_matrix;
    uniform vec3 camera_position;

    uniform vec3 light_direction;
    uniform vec3 object_color;
    uniform vec3 ambient_color;
    uniform vec3 light_color;
    uniform float specular_power;
    uniform float specular_multiplier;
    uniform bool use_texture;
    uniform bool use_color;

    varying vec3 frag_position;
    varying vec3 frag_normal;
    varying vec2 frag_uv;
    varying vec3 frag_color;

    void main() {
        vec3 color = object_color;
        if (use_color) {
            color = frag_color;
        }
        if (use_texture) {
            color = vec3(texture2D(sampler, frag_uv));
        }
        float diffuse = max(dot(mat3(normal_matrix) * frag_normal,
            light_direction), 0.0);
        float specular = 0.0;
        if (diffuse > 0.0) {
            vec3 camera_vector = normalize(camera_position - frag_position);
            specular = pow(max(dot(camera_vector,
                reflect(-light_direction, frag_normal)), 0.0), specular_power);
        }
        vec3 light = ambient_color + light_color * diffuse +
            specular * specular_multiplier;
        gl_FragColor = vec4(min(color * light, vec3(1.0)), 1.0);
    }
    '''
    def set_defaults(self, context):
        context.light_direction = normalize((1, 1, 1))
        context.object_color = (0.4, 0.6, 0.8)
        context.ambient_color = (0.3, 0.3, 0.3)
        context.light_color = (0.7, 0.7, 0.7)
        context.specular_power = 32.0
        context.specular_multiplier = 1.0
        context.use_texture = False
        context.use_color = False
