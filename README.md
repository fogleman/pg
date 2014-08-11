## pg: The Python Graphics Framework

pg is a lightweight, high-level OpenGL graphics framework for Python. It is a
work in progress.

### Tutorial

A basic tutorial is available here:

http://pg.readthedocs.org/en/latest/tutorial.html

### Features

Many OpenGL applications have a lot of features in common, but there's a lot of
boilerplate involved when using OpenGL. This high-level framework lets you
focus on your application-specific functionality instead.

* shaders
    * compile and link
    * attributes and uniforms
    * built-in shaders for common use-cases
* vertex buffers
    * optionally interleaved
* matrices
    * translate, rotate, scale
    * perspective and orthographic projections
    * transpose, determinant, inverse
* textures
* geometric shapes
    * sphere, cuboid, plane, cylinder, cone, axes
* WASD movement
    * built-in!
* windowing and input
    * glfw-based
    * multiple windows

### Dependencies

    brew tap homebrew/versions
    brew install glfw3
    pip install Pillow PyOpenGL

### Examples

Clone the repository and run main.py to see these and several other examples.

![Screenshot](http://i.imgur.com/s5AEYei.gif)

```python
from math import sin, cos, pi
import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((14, 0, 0), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        sphere = pg.Sphere(3, 0.4, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.position)
        self.context.normal = pg.VertexBuffer(sphere.normal)
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        for z in range(-2, 3):
            for x in range(-10, 11):
                y = sin(self.time * pi + x * 0.5 + z * pi) * 3
                model_matrix = pg.Matrix().translate((x, y, z * 3))
                self.context.model_matrix = model_matrix
                self.context.matrix = matrix * model_matrix
                self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
```

pg includes basic support for CSG (Constructive Solid Geometry). It's pretty
slow currently - perhaps porting this portion to C will come soon.

![Screenshot](http://i.imgur.com/3QJFHw1.png)

```python
import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((-2, 2, 2), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        a = pg.Solid(pg.Cuboid(-1, 1, -1, 1, -1, 1))
        b = pg.Solid(pg.Sphere(2, 1.35))
        c = pg.Solid(pg.Cylinder((-1, 0, 0), (1, 0, 0), 0.5, 18))
        d = pg.Solid(pg.Cylinder((0, -1, 0), (0, 1, 0), 0.5, 18))
        e = pg.Solid(pg.Cylinder((0, 0, -1), (0, 0, 1), 0.5, 18))
        shape = (a & b) - (c | d | e)
        position, normal = shape.triangulate()
        self.context.position = pg.VertexBuffer(position)
        self.context.normal = pg.VertexBuffer(normal)
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
```
