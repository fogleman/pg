from ctypes import *
from OpenGL.GL import *
import os

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
        for index in range(count.value):
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
        for index in range(count.value):
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
