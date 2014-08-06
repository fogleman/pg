## pg: Python Graphics Framework

pg is a lightweight OpenGL graphics framework for Python.

It is a work in progress.

### Features

Most OpenGL applications have a lot of features in common, but there's a lot of
boilerplate involved when using bare OpenGL. This framework provides a clean
API for managing these common features so you can focus on your application-
specific functionality instead.

* shaders
    * compile and link
    * attributes and uniforms
* vertex buffers
* matrices
    * translate, rotate, scale
    * perspective and orthographic projections
    * transpose, determinant, inverse
* textures
    * load
* geometric shapes
    * sphere, cube
* WASD movement
    * built-in!
* windowing and input
    * glfw-based
    * multiple windows

### Screenshot

![Screenshot](http://i.imgur.com/JD0ObXJ.png)

### Sample

    from math import sin, cos, radians
    import pg
    import random

    class Window(pg.Window):
        def __init__(self):
            super(Window, self).__init__((800, 600))
            self.wasd = pg.WASD(self, speed=3)
        def on_size(self, width, height):
            self.aspect = float(width) / height
        def setup(self):
            self.program = pg.Program(
                'shaders/vertex.glsl', 'shaders/fragment.glsl')
            self.context = pg.Context(self.program)
            position = []
            for angle in xrange(0, 360, 30):
                x, z = sin(radians(angle)), cos(radians(angle))
                position.extend(pg.sphere(3, 0.2, (x, 0, z)))
            color = []
            for i in xrange(12 * 8):
                n = len(position) / 3 / 12 / 8
                color.extend(pg.hex_color(random.randint(0, 0xffffff)) * n)
            self.context.position = pg.VertexBuffer(3, position)
            self.context.color = pg.VertexBuffer(3, color)
        def update(self, t, dt):
            matrix = pg.Matrix().rotate((0, 1, 0), t)
            matrix = self.wasd.get_matrix(matrix)
            matrix = matrix.perspective(65, self.aspect, 0.1, 100)
            self.context.matrix = matrix
        def draw(self):
            self.clear()
            self.context.draw(pg.GL_TRIANGLES)

    if __name__ == "__main__":
        app = pg.App()
        Window()
        app.run()

### Dependencies

    brew install glfw3
    pip install glfw Pillow PyOpenGL
