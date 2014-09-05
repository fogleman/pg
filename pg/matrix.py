from __future__ import division

from math import sin, cos, tan, pi
from .util import normalize

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
        for r in xrange(4):
            x = ','.join('% .3f' % self.value[c * 4 + r] for c in xrange(4))
            result.append('[%s]' % x)
        return '\n'.join(result)
    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.matrix_multiply(other)
        elif isinstance(other, (tuple, list)):
            if len(other) == 3:
                return self.vector3_multiply(other)
            elif len(other) == 4:
                return self.vector4_multiply(other)
            else:
                return NotImplemented
        else:
            return NotImplemented
    # def __getitem__(self, index):
    #     return self.value[self.index(index)]
    # def __setitem__(self, index, value):
    #     self.value[self.index(index)] = value
    # def index(self, index):
    #     try:
    #         row, col = index
    #         return col * 4 + row
    #     except Exception:
    #         return index
    def matrix_multiply(self, other):
        (
            a00, a10, a20, a30, a01, a11, a21, a31,
            a02, a12, a22, a32, a03, a13, a23, a33,
        ) = self.value
        (
            b00, b10, b20, b30, b01, b11, b21, b31,
            b02, b12, b22, b32, b03, b13, b23, b33,
        ) = other.value
        c00 = a00 * b00 + a01 * b10 + a02 * b20 + a03 * b30
        c10 = a10 * b00 + a11 * b10 + a12 * b20 + a13 * b30
        c20 = a20 * b00 + a21 * b10 + a22 * b20 + a23 * b30
        c30 = a30 * b00 + a31 * b10 + a32 * b20 + a33 * b30
        c01 = a00 * b01 + a01 * b11 + a02 * b21 + a03 * b31
        c11 = a10 * b01 + a11 * b11 + a12 * b21 + a13 * b31
        c21 = a20 * b01 + a21 * b11 + a22 * b21 + a23 * b31
        c31 = a30 * b01 + a31 * b11 + a32 * b21 + a33 * b31
        c02 = a00 * b02 + a01 * b12 + a02 * b22 + a03 * b32
        c12 = a10 * b02 + a11 * b12 + a12 * b22 + a13 * b32
        c22 = a20 * b02 + a21 * b12 + a22 * b22 + a23 * b32
        c32 = a30 * b02 + a31 * b12 + a32 * b22 + a33 * b32
        c03 = a00 * b03 + a01 * b13 + a02 * b23 + a03 * b33
        c13 = a10 * b03 + a11 * b13 + a12 * b23 + a13 * b33
        c23 = a20 * b03 + a21 * b13 + a22 * b23 + a23 * b33
        c33 = a30 * b03 + a31 * b13 + a32 * b23 + a33 * b33
        return Matrix([
            c00, c10, c20, c30, c01, c11, c21, c31,
            c02, c12, c22, c32, c03, c13, c23, c33])
    def vector3_multiply(self, other):
        (
            a00, a10, a20, a30, a01, a11, a21, a31,
            a02, a12, a22, a32, a03, a13, a23, a33,
        ) = self.value
        b0, b1, b2 = other
        return (
            a00 * b0 + a01 * b1 + a02 * b2 + a03,
            a10 * b0 + a11 * b1 + a12 * b2 + a13,
            a20 * b0 + a21 * b1 + a22 * b2 + a23,
        )
    def vector4_multiply(self, other):
        (
            a00, a10, a20, a30, a01, a11, a21, a31,
            a02, a12, a22, a32, a03, a13, a23, a33,
        ) = self.value
        b0, b1, b2, b3 = other
        return (
            a00 * b0 + a01 * b1 + a02 * b2 + a03 * b3,
            a10 * b0 + a11 * b1 + a12 * b2 + a13 * b3,
            a20 * b0 + a21 * b1 + a22 * b2 + a23 * b3,
            a30 * b0 + a31 * b1 + a32 * b2 + a33 * b3,
        )
    def identity(self):
        return Matrix()
    def transpose(self):
        (
            a00, a10, a20, a30, a01, a11, a21, a31,
            a02, a12, a22, a32, a03, a13, a23, a33,
        ) = self.value
        return Matrix([
            a00, a01, a02, a03, a10, a11, a12, a13,
            a20, a21, a22, a23, a30, a31, a32, a33])
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
