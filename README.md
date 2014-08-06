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
    * built-in shaders for common functions
* vertex buffers
* matrices
    * translate, rotate, scale
    * perspective and orthographic projections
    * transpose, determinant, inverse
* textures
* geometric shapes
    * sphere, cuboid, plane, cylinder, axes
* WASD movement
    * built-in!
* windowing and input
    * glfw-based
    * multiple windows

### Dependencies

    brew install glfw3
    pip install glfw Pillow PyOpenGL

### Example

![Screenshot](http://i.imgur.com/2rx9Mtq.png)

    from math import sin, cos, radians, pi
    import pg

    class Window(pg.Window):
        def __init__(self):
            super(Window, self).__init__((800, 600))
            self.wasd = pg.WASD(self)
            self.wasd.look_at((-3, 3, 3), (0, 0, 0))
        def setup(self):
            program = pg.Program('shaders/vertex.glsl', 'shaders/fragment.glsl')
            self.context = pg.Context(program)
            self.context.sampler = pg.Texture(0, 'textures/bronze.jpg')
            data = []
            r = 0.4
            d = 2.0
            for angle in range(0, 360, 60):
                x, z = sin(radians(angle)) * d, cos(radians(angle)) * d
                sphere = pg.Sphere(3, r, (x, 0, z))
                data.extend(pg.interleave(
                    sphere.position, sphere.normal, sphere.uv))
            for angle in range(30, 360, 60):
                x, z = sin(radians(angle)) * d, cos(radians(angle)) * d
                cuboid = pg.Cuboid(x - r, x + r, -r, r, z - r, z + r)
                data.extend(pg.interleave(
                    cuboid.position, cuboid.normal, cuboid.uv))
            plane = pg.Plane((0, 0, 0), (1, 1, 1))
            data.extend(pg.interleave(
                plane.position, plane.normal, plane.uv))
            cylinder = pg.Cylinder((1, 1, -1), (-1, 1, 1), 0.25, 36)
            data.extend(pg.interleave(
                cylinder.position, cylinder.normal, cylinder.uv))
            self.context.position, self.context.normal, self.context.uv = (
                pg.VertexBuffer(data).slices(3, 3, 2))
            self.axes = pg.Context(pg.SolidColorProgram())
            self.axes.color = (0.3, 0.3, 0.3)
            self.axes.position = pg.VertexBuffer(pg.Axes(100).position)
        def update(self, t, dt):
            matrix = pg.Matrix().rotate((0, 1, 0), t * 2 * pi / 60)
            self.context.normal_matrix = matrix.inverse().transpose()
            matrix = self.wasd.get_matrix(matrix)
            matrix = matrix.perspective(65, self.aspect, 0.1, 100)
            self.context.matrix = matrix
            self.axes.matrix = matrix
        def draw(self):
            self.clear()
            self.context.draw(pg.GL_TRIANGLES)
            self.axes.draw(pg.GL_LINES)

    if __name__ == "__main__":
        app = pg.App()
        Window()
        app.run()
