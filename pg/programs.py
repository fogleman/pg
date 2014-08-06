from core import Program

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
