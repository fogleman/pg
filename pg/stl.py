from .core import Mesh
import os
import struct

def parse_binary_stl(path):
    if os.path.exists(path):
        with open(path, 'rb') as fp:
            path = fp.read()
    data = path
    positions = []
    normals = []
    uvs = []
    count = struct.unpack('<I', data[80:84])[0]
    for i in xrange(count):
        index = 84 + i * 50
        face = struct.unpack('<ffffffffffff', data[index:index+48])
        nx, ny, nz, x1, y1, z1, x2, y2, z2, x3, y3, z3 = face
        positions.append((x1, y1, z1))
        positions.append((x2, y2, z2))
        positions.append((x3, y3, z3))
        normals.append((nx, ny, nz))
        normals.append((nx, ny, nz))
        normals.append((nx, ny, nz))
    return positions, normals, uvs

class STL(Mesh):
    def __init__(self, path):
        super(STL, self).__init__()
        positions, normals, uvs = parse_binary_stl(path)
        self.positions = positions
        self.normals = normals
        self.uvs = uvs
