import pg

class SphereScene(pg.Scene):
    def setup(self):
        print 'SphereScene.setup()'
        self.wasd = pg.WASD(self)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.sphere = pg.Sphere(4, 0.5, (0, 0, 0))
    def enter(self):
        print 'SphereScene.enter()'
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.window.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.window.clear()
        self.sphere.draw(self.context)
    def exit(self):
        print 'SphereScene.exit()'
    def teardown(self):
        print 'SphereScene.teardown()'
    def on_mouse_button(self, button, action, mods):
        if action == pg.PRESS:
            self.window.set_scene(CylinderScene(self.window))

class CylinderScene(pg.Scene):
    def setup(self):
        print 'CylinderScene.setup()'
        self.wasd = pg.WASD(self)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.cylinder = pg.Cylinder((0, -0.5, 0), (0, 0.5, 0), 0.5, 18)
    def enter(self):
        print 'CylinderScene.enter()'
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.window.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.window.clear()
        self.cylinder.draw(self.context)
    def exit(self):
        print 'CylinderScene.exit()'
    def teardown(self):
        print 'CylinderScene.teardown()'
    def on_mouse_button(self, button, action, mods):
        if action == pg.PRESS:
            self.window.set_scene(SphereScene(self.window))

class Window(pg.Window):
    def setup(self):
        self.set_scene(SphereScene(self))

if __name__ == "__main__":
    pg.run(Window)
