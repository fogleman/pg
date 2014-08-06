from core import Program

class SingleColorProgram(Program):
    def __init__(self):
        vs = '''
        #version 120

        uniform mat4 matrix;

        attribute vec4 position;

        void main() {
            gl_Position = matrix * position;
        }
        '''
        fs = '''
        #version 120

        uniform vec3 color;

        void main() {
            gl_FragColor = vec4(color, 1.0);
        }
        '''
        return super(SingleColorProgram, self).__init__(vs, fs)
