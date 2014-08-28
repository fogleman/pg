from pg import glfw
import pg

class SphereScene(pg.Scene):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.sphere = pg.Sphere(4, 0.5, (0, 0, 0))
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.window.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.window.clear()
        self.sphere.draw(self.context)
    def on_mouse_button(self, button, action, mods):
        if action == glfw.PRESS:
            self.window.replace_scene(self.window.cube_scene)

class CubeScene(pg.Scene):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.cube = pg.Cuboid(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.window.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.window.clear()
        self.cube.draw(self.context)
    def on_mouse_button(self, button, action, mods):
        if action == glfw.PRESS:
            self.window.replace_scene(self.window.sphere_scene)

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.sphere_scene = SphereScene(self)
        self.cube_scene = CubeScene(self)
        self.push_scene(self.sphere_scene)

if __name__ == "__main__":
    pg.run(Window)
