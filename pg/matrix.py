from __future__ import division

from math import sin, cos, tan, pi
from util import normalize

class Matrix(object):
    def __init__(self, value=None):
        if value is None:
            value = [
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1,
            ]
        self.value = map(float, value)
    def __repr__(self):
        result = []
        for row in xrange(4):
            x = ','.join('% .3f' % self[(row, col)] for col in xrange(4))
            result.append('[%s]' % x)
        return '\n'.join(result)
    def __getitem__(self, index):
        return self.value[self.index(index)]
    def __setitem__(self, index, value):
        self.value[self.index(index)] = value
    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.matrix_multiply(other)
        elif len(other) == 3:
            x, y, z = other
            return self.vector_multiply((x, y, z, 1))
        else:
            return self.vector_multiply(other)
    def index(self, index):
        try:
            row, col = index
            return col * 4 + row
        except Exception:
            return index
    def matrix_multiply(self, other):
        result = Matrix()
        for col in xrange(4):
            for row in xrange(4):
                result[(row, col)] = sum(
                    self[(row, i)] * other[(i, col)] for i in xrange(4))
        return result
    def vector_multiply(self, other):
        return tuple(
            sum(self[(i, j)] * other[j] for j in xrange(4))
            for i in xrange(4))
    def identity(self):
        return Matrix()
    def transpose(self):
        result = Matrix()
        for col in xrange(4):
            for row in xrange(4):
                result[(row, col)] = self[(col, row)]
        return result
    def determinant(self):
        (
            m00, m10, m20, m30, m01, m11, m21, m31,
            m02, m12, m22, m32, m03, m13, m23, m33,
        ) = self.value
        return (
            m00 * m11 * m22 * m33 - m00 * m11 * m23 * m32 +
            m00 * m12 * m23 * m31 - m00 * m12 * m21 * m33 +
            m00 * m13 * m21 * m32 - m00 * m13 * m22 * m31 -
            m01 * m12 * m23 * m30 + m01 * m12 * m20 * m33 -
            m01 * m13 * m20 * m32 + m01 * m13 * m22 * m30 -
            m01 * m10 * m22 * m33 + m01 * m10 * m23 * m32 +
            m02 * m13 * m20 * m31 - m02 * m13 * m21 * m30 +
            m02 * m10 * m21 * m33 - m02 * m10 * m23 * m31 +
            m02 * m11 * m23 * m30 - m02 * m11 * m20 * m33 -
            m03 * m10 * m21 * m32 + m03 * m10 * m22 * m31 -
            m03 * m11 * m22 * m30 + m03 * m11 * m20 * m32 -
            m03 * m12 * m20 * m31 + m03 * m12 * m21 * m30)
    def inverse(self):
        (
            m00, m10, m20, m30, m01, m11, m21, m31,
            m02, m12, m22, m32, m03, m13, m23, m33,
        ) = self.value
        d = self.determinant()
        n00 = (m12 * m23 * m31 - m13 * m22 * m31 + m13 * m21 * m32 -
            m11 * m23 * m32 - m12 * m21 * m33 + m11 * m22 * m33) / d
        n01 = (m03 * m22 * m31 - m02 * m23 * m31 - m03 * m21 * m32 +
            m01 * m23 * m32 + m02 * m21 * m33 - m01 * m22 * m33) / d
        n02 = (m02 * m13 * m31 - m03 * m12 * m31 + m03 * m11 * m32 -
            m01 * m13 * m32 - m02 * m11 * m33 + m01 * m12 * m33) / d
        n03 = (m03 * m12 * m21 - m02 * m13 * m21 - m03 * m11 * m22 +
            m01 * m13 * m22 + m02 * m11 * m23 - m01 * m12 * m23) / d
        n10 = (m13 * m22 * m30 - m12 * m23 * m30 - m13 * m20 * m32 +
            m10 * m23 * m32 + m12 * m20 * m33 - m10 * m22 * m33) / d
        n11 = (m02 * m23 * m30 - m03 * m22 * m30 + m03 * m20 * m32 -
            m00 * m23 * m32 - m02 * m20 * m33 + m00 * m22 * m33) / d
        n12 = (m03 * m12 * m30 - m02 * m13 * m30 - m03 * m10 * m32 +
            m00 * m13 * m32 + m02 * m10 * m33 - m00 * m12 * m33) / d
        n13 = (m02 * m13 * m20 - m03 * m12 * m20 + m03 * m10 * m22 -
            m00 * m13 * m22 - m02 * m10 * m23 + m00 * m12 * m23) / d
        n20 = (m11 * m23 * m30 - m13 * m21 * m30 + m13 * m20 * m31 -
            m10 * m23 * m31 - m11 * m20 * m33 + m10 * m21 * m33) / d
        n21 = (m03 * m21 * m30 - m01 * m23 * m30 - m03 * m20 * m31 +
            m00 * m23 * m31 + m01 * m20 * m33 - m00 * m21 * m33) / d
        n22 = (m01 * m13 * m30 - m03 * m11 * m30 + m03 * m10 * m31 -
            m00 * m13 * m31 - m01 * m10 * m33 + m00 * m11 * m33) / d
        n23 = (m03 * m11 * m20 - m01 * m13 * m20 - m03 * m10 * m21 +
            m00 * m13 * m21 + m01 * m10 * m23 - m00 * m11 * m23) / d
        n30 = (m12 * m21 * m30 - m11 * m22 * m30 - m12 * m20 * m31 +
            m10 * m22 * m31 + m11 * m20 * m32 - m10 * m21 * m32) / d
        n31 = (m01 * m22 * m30 - m02 * m21 * m30 + m02 * m20 * m31 -
            m00 * m22 * m31 - m01 * m20 * m32 + m00 * m21 * m32) / d
        n32 = (m02 * m11 * m30 - m01 * m12 * m30 - m02 * m10 * m31 +
            m00 * m12 * m31 + m01 * m10 * m32 - m00 * m11 * m32) / d
        n33 = (m01 * m12 * m20 - m02 * m11 * m20 + m02 * m10 * m21 -
            m00 * m12 * m21 - m01 * m10 * m22 + m00 * m11 * m22) / d
        return Matrix([
            n00, n10, n20, n30, n01, n11, n21, n31,
            n02, n12, n22, n32, n03, n13, n23, n33])
    def translate(self, value):
        x, y, z = value
        matrix = Matrix([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            x, y, z, 1,
        ])
        return matrix * self
    def scale(self, value):
        x, y, z = value
        matrix = Matrix([
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1,
        ])
        return matrix * self
    def rotate(self, vector, angle):
        x, y, z = normalize(vector)
        s = sin(angle)
        c = cos(angle)
        m = 1 - c
        matrix = Matrix([
            m * x * x + c,
            m * x * y - z * s,
            m * z * x + y * s,
            0,
            m * x * y + z * s,
            m * y * y + c,
            m * y * z - x * s,
            0,
            m * z * x - y * s,
            m * y * z + x * s,
            m * z * z + c,
            0,
            0,
            0,
            0,
            1,
        ])
        return matrix * self
    def frustum(self, left, right, bottom, top, near, far):
        t1 = 2 * near
        t2 = right - left
        t3 = top - bottom
        t4 = far - near
        matrix = Matrix([
            t1 / t2,
            0,
            0,
            0,
            0,
            t1 / t3,
            0,
            0,
            (right + left) / t2,
            (top + bottom) / t3,
            (-far - near) / t4,
            -1,
            0,
            0,
            (-t1 * far) / t4,
            0,
        ])
        return matrix * self
    def perspective(self, fov, aspect, near, far):
        ymax = near * tan(fov * pi / 360)
        xmax = ymax * aspect
        return self.frustum(-xmax, xmax, -ymax, ymax, near, far)
    def orthographic(self, left, right, bottom, top, near, far):
        matrix = Matrix([
            2 / (right - left),
            0,
            0,
            0,
            0,
            2 / (top - bottom),
            0,
            0,
            0,
            0,
            -2 / (far - near),
            0,
            -(right + left) / (right - left),
            -(top + bottom) / (top - bottom),
            -(far + near) / (far - near),
            1,
        ])
        return matrix * self
