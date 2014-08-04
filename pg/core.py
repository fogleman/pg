from ctypes import *
from OpenGL.GL import *
from math import sin, cos, tan, pi
import glfw
import os
import time

ATTRIBUTE_DATA_TYPES = {
    GL_FLOAT: 'GL_FLOAT',
    GL_FLOAT_VEC2: 'GL_FLOAT_VEC2',
    GL_FLOAT_VEC3: 'GL_FLOAT_VEC3',
    GL_FLOAT_VEC4: 'GL_FLOAT_VEC4',
    GL_FLOAT_MAT2: 'GL_FLOAT_MAT2',
    GL_FLOAT_MAT3: 'GL_FLOAT_MAT3',
    GL_FLOAT_MAT4: 'GL_FLOAT_MAT4',
}

UNIFORM_DATA_TYPES = {
    GL_FLOAT: 'GL_FLOAT',
    GL_FLOAT_VEC2: 'GL_FLOAT_VEC2',
    GL_FLOAT_VEC3: 'GL_FLOAT_VEC3',
    GL_FLOAT_VEC4: 'GL_FLOAT_VEC4',
    GL_INT: 'GL_INT',
    GL_INT_VEC2: 'GL_INT_VEC2',
    GL_INT_VEC3: 'GL_INT_VEC3',
    GL_INT_VEC4: 'GL_INT_VEC4',
    GL_BOOL: 'GL_BOOL',
    GL_BOOL_VEC2: 'GL_BOOL_VEC2',
    GL_BOOL_VEC3: 'GL_BOOL_VEC3',
    GL_BOOL_VEC4: 'GL_BOOL_VEC4',
    GL_FLOAT_MAT2: 'GL_FLOAT_MAT2',
    GL_FLOAT_MAT3: 'GL_FLOAT_MAT3',
    GL_FLOAT_MAT4: 'GL_FLOAT_MAT4',
    GL_SAMPLER_2D: 'GL_SAMPLER_2D',
    GL_SAMPLER_CUBE: 'GL_SAMPLER_CUBE',
}

class Shader(object):
    def __init__(self, shader_type, shader_source):
        if os.path.exists(shader_source):
            with open(shader_source, 'r') as fp:
                shader_source = fp.read()
        self.handle = glCreateShader(shader_type)
        glShaderSource(self.handle, shader_source)
        glCompileShader(self.handle)
        log = glGetShaderInfoLog(self.handle)
        if log:
            raise Exception(log)

class VertexShader(Shader):
    def __init__(self, shader_source):
        super(VertexShader, self).__init__(GL_VERTEX_SHADER, shader_source)

class FragmentShader(Shader):
    def __init__(self, shader_source):
        super(FragmentShader, self).__init__(GL_FRAGMENT_SHADER, shader_source)

class Attribute(object):
    def __init__(self, location, name, size, data_type):
        self.location = location
        self.name = name
        self.size = size
        self.data_type = data_type
    def __repr__(self):
        return 'Attribute%s' % str(
            (self.location, self.name, self.size, self.data_type))

class Uniform(object):
    def __init__(self, location, name, size, data_type):
        self.location = location
        self.name = name
        self.size = size
        self.data_type = data_type
    def __repr__(self):
        return 'Uniform%s' % str(
            (self.location, self.name, self.size, self.data_type))

class Program(object):
    def __init__(self, vs, fs):
        if not isinstance(vs, Shader):
            vs = VertexShader(vs)
        if not isinstance(fs, Shader):
            fs = FragmentShader(fs)
        self.vs = vs
        self.fs = fs
        self.handle = glCreateProgram()
        glAttachShader(self.handle, self.vs.handle)
        glAttachShader(self.handle, self.fs.handle)
        glLinkProgram(self.handle)
        log = glGetProgramInfoLog(self.handle)
        if log:
            raise Exception(log)
    def get_attributes(self):
        result = []
        count = c_int()
        glGetProgramiv(self.handle, GL_ACTIVE_ATTRIBUTES, byref(count))
        name = create_string_buffer(256)
        size = c_int()
        data_type = c_int()
        for index in xrange(count.value):
            glGetActiveAttrib(
                self.handle, index, 256, None,
                byref(size), byref(data_type), name)
            location = glGetAttribLocation(self.handle, name.value)
            attribute = Attribute(
                location, name.value, size.value, data_type.value)
            result.append(attribute)
        return result
    def get_uniforms(self):
        result = []
        count = c_int()
        glGetProgramiv(self.handle, GL_ACTIVE_UNIFORMS, byref(count))
        for index in xrange(count.value):
            name, size, data_type = glGetActiveUniform(self.handle, index)
            location = glGetUniformLocation(self.handle, name)
            uniform = Uniform(location, name, size, data_type)
            result.append(uniform)
        return result

class Context(object):
    def __init__(self, program):
        self.program = program
    def draw(self, mode):
        pass

def normalize(vector):
    d = sum(x * x for x in vector) ** 0.5
    return tuple(x / d for x in vector)

class Matrix(object):
    def __init__(self, value=None):
        if value is None:
            value = [
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1,
            ]
        self.value = value
    def __repr__(self):
        result = []
        for row in xrange(4):
            x = ','.join('% .3f' % self[(row, col)] for col in xrange(4))
            result.append('[%s]' % x)
        return '\n'.join(result)
    def __getitem__(self, index):
        return self.value[self.index(index)]
    def __setitem__(self, index, value):
        self.value[self.index(index)] = value
    def __mul__(self, other):
        return self.multiply(other)
    def index(self, index):
        try:
            row, col = index
            return col * 4 + row
        except Exception:
            return index
    def multiply(self, other):
        result = Matrix()
        for col in xrange(4):
            for row in xrange(4):
                result[(row, col)] = sum(
                    self[(row, i)] * other[(i, col)] for i in xrange(4))
        return result
    def identity(self):
        return Matrix()
    def translate(self, value):
        dx, dy, dz = value
        matrix = Matrix([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            dx, dy, dz, 1,
        ])
        return matrix * self
    def scale(self, value):
        sx, sy, sz = value
        matrix = Matrix([
            sx, 0, 0, 0,
            0, sy, 0, 0,
            0, 0, sz, 0,
            0, 0, 0, 1,
        ])
        return matrix * self
    def rotate(self, vector, angle):
        x, y, z = normalize(vector)
        s = sin(angle)
        c = cos(angle)
        m = 1 - c
        matrix = Matrix([
            m * x * x + c,
            m * x * y - z * s,
            m * z * x + y * s,
            0,
            m * x * y + z * s,
            m * y * y + c,
            m * y * z - x * s,
            0,
            m * z * x - y * s,
            m * y * z + x * s,
            m * z * z + c,
            0,
            0,
            0,
            0,
            1,
        ])
        return matrix * self
    def frustum(self, left, right, bottom, top, near, far):
        t1 = 2.0 * near
        t2 = right - left
        t3 = top - bottom
        t4 = far - near
        matrix = Matrix([
            t1 / t2,
            0,
            0,
            0,
            0,
            t1 / t3,
            0,
            0,
            (right + left) / t2,
            (top + bottom) / t3,
            (-far - near) / t4,
            -1,
            0,
            0,
            (-t1 * far) / t4,
            0,
        ])
        return matrix * self
    def perspective(self, fov, aspect, near, far):
        ymax = near * tan(fov * pi / 360)
        xmax = ymax * aspect
        return self.frustum(-xmax, xmax, -ymax, ymax, near, far)
    def orthographic(self, left, right, bottom, top, near, far):
        matrix = Matrix([
            2 / (right - left),
            0,
            0,
            0,
            0,
            2 / (top - bottom),
            0,
            0,
            0,
            0,
            -2 / (far - near),
            0,
            -(right + left) / (right - left),
            -(top + bottom) / (top - bottom),
            -(far + near) / (far - near),
            1,
        ])
        return matrix * self

class App(object):
    def create_window(self):
        if not glfw.init():
            raise Exception
        title = 'Python Graphics'
        self.window = glfw.create_window(640, 480, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception
        glfw.make_context_current(self.window)
    def setup(self):
        pass
    def update(self, dt):
        pass
    def draw(self):
        pass
    def teardown(self):
        pass
    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
    def run(self):
        self.create_window()
        self.setup()
        self.time = time.time()
        while not glfw.window_should_close(self.window):
            now = time.time()
            dt = now - self.time
            self.time = now
            self.update(dt)
            self.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        self.teardown()
        glfw.terminate()
