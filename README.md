## pg: Python Graphics Framework

pg is a lightweight OpenGL graphics framework for Python. It is a work in
progress.

### Tutorial

A basic tutorial is available here:

http://pg.readthedocs.org/en/latest/tutorial.html

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

### Examples

Clone the repository and run main.py to see several other examples.

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
