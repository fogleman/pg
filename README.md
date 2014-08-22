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

#### 3D Pipes

**[pipes.py](https://github.com/fogleman/pg/blob/master/examples/pipes.py)**

<a href="http://www.youtube.com/watch?feature=player_embedded&v=KpsjFiYDp5g
" target="_blank"><img src="http://img.youtube.com/vi/KpsjFiYDp5g/0.jpg" 
alt="3D Pipes" width="800" height="600" border="10" /></a>

#### Gusev Crater

**[gusev.py](https://github.com/fogleman/pg/blob/master/examples/gusev.py)**

![Screenshot](http://i.imgur.com/fiIJKIt.png)

#### CSG (Constructive Solid Geometry)

pg includes basic support for constructive solid geometry (CSG).

**[csg.py](https://github.com/fogleman/pg/blob/master/examples/csg.py)**

![Screenshot](http://i.imgur.com/3QJFHw1.png)
