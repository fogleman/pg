from OpenGL.GL import *
import glfw
import pg

# program.position = pg.VertexBuffer(3, pg.FLOAT, [...])
# program.matrix = pg.mat4(1).translate((0, 1, 0)).perspective(45, 1.5, 0.1, 100)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 480, 'Window', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    matrix = pg.Matrix()
    matrix = matrix.translate((0, 1, 0))
    matrix = matrix.perspective(45, 640 / 480.0, 0.1, 100)
    print matrix

    program = pg.Program('shaders/vertex.glsl', 'shaders/fragment.glsl')
    print program.get_attributes()
    print program.get_uniforms()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()
