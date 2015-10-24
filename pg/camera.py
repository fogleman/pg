from math import sin, cos, pi, atan2, asin
from .matrix import Matrix
from .util import normalize

class Camera(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.rx = 0
        self.ry = 0
    @property
    def position(self):
        return (self.x, self.y, self.z)
    def look_at(self, position, target):
        px, py, pz = position
        tx, ty, tz = target
        dx, dy, dz = normalize((tx - px, ty - py, tz - pz))
        self.x = px
        self.y = py
        self.z = pz
        self.rx = 2 * pi - (atan2(dx, dz) + pi)
        self.ry = asin(dy)
    def get_matrix(self, matrix=None, translate=True):
        matrix = matrix or Matrix()
        if translate:
            matrix = matrix.translate((-self.x, -self.y, -self.z))
        matrix = matrix.rotate((cos(self.rx), 0, sin(self.rx)), self.ry)
        matrix = matrix.rotate((0, 1, 0), -self.rx)
        return matrix
