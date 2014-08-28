from collections import defaultdict

def hex_color(value):
    '''Accepts a hexadecimal color `value` in the format ``0xrrggbb`` and
    returns an (r, g, b) tuple where 0.0 <= r, g, b <= 1.0.
    '''
    r = ((value >> (8 * 2)) & 255) / 255.0
    g = ((value >> (8 * 1)) & 255) / 255.0
    b = ((value >> (8 * 0)) & 255) / 255.0
    return (r, g, b)

def normalize(vector):
    '''Normalizes the `vector` so that its length is 1. `vector` can have
    any number of components.
    '''
    d = sum(x * x for x in vector) ** 0.5
    return tuple(x / d for x in vector)

def distance(p1, p2):
    '''Computes and returns the distance between two points, `p1` and `p2`.
    The points can have any number of components.
    '''
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def cross(v1, v2):
    '''Computes the cross product of two vectors.
    '''
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )

def dot(v1, v2):
    '''Computes the dot product of two vectors.
    '''
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return x1 * x2 + y1 * y2 + z1 * z2

def add(v1, v2):
    '''Adds two vectors.
    '''
    return tuple(a + b for a, b in zip(v1, v2))

def sub(v1, v2):
    '''Subtracts two vectors.
    '''
    return tuple(a - b for a, b in zip(v1, v2))

def mul(v, s):
    '''Multiplies a vector and a scalar.
    '''
    return tuple(a * s for a in v)

def neg(vector):
    '''Negates a vector.
    '''
    return tuple(-x for x in vector)

def interpolate(v1, v2, t):
    '''Interpolate from one vector to another.
    '''
    return add(v1, mul(sub(v2, v1), t))

def normal_from_points(a, b, c):
    '''Computes a normal vector given three points.
    '''
    x1, y1, z1 = a
    x2, y2, z2 = b
    x3, y3, z3 = c
    ab = (x2 - x1, y2 - y1, z2 - z1)
    ac = (x3 - x1, y3 - y1, z3 - z1)
    x, y, z = cross(ab, ac)
    d = (x * x + y * y + z * z) ** 0.5
    return (x / d, y / d, z / d)

def smooth_normals(positions, normals):
    '''Assigns an averaged normal to each position based on all of the normals
    originally used for the position.
    '''
    lookup = defaultdict(list)
    for position, normal in zip(positions, normals):
        lookup[position].append(normal)
    result = []
    for position in positions:
        tx = ty = tz = 0
        for x, y, z in lookup[position]:
            tx += x
            ty += y
            tz += z
        d = (tx * tx + ty * ty + tz * tz) ** 0.5
        result.append((tx / d, ty / d, tz / d))
    return result

def bounding_box(positions):
    '''Computes the bounding box for a list of 3-dimensional points.
    '''
    (x0, y0, z0) = (x1, y1, z1) = positions[0]
    for x, y, z in positions:
        x0 = min(x0, x)
        y0 = min(y0, y)
        z0 = min(z0, z)
        x1 = max(x1, x)
        y1 = max(y1, y)
        z1 = max(z1, z)
    return (x0, y0, z0), (x1, y1, z1)

def recenter(positions):
    '''Returns a list of new positions centered around the origin.
    '''
    (x0, y0, z0), (x1, y1, z1) = bounding_box(positions)
    dx = x1 - (x1 - x0) / 2.0
    dy = y1 - (y1 - y0) / 2.0
    dz = z1 - (z1 - z0) / 2.0
    result = []
    for x, y, z in positions:
        result.append((x - dx, y - dy, z - dz))
    return result

def interleave(*args):
    '''Interleaves the elements of the provided arrays.

        >>> a = [(0, 0), (1, 0), (2, 0), (3, 0)]
        >>> b = [(0, 0), (0, 1), (0, 2), (0, 3)]
        >>> interleave(a, b)
        [(0, 0, 0, 0), (1, 0, 0, 1), (2, 0, 0, 2), (3, 0, 0, 3)]

    This is useful for combining multiple vertex attributes into a single
    vertex buffer. The shader attributes can be assigned a slice of the
    vertex buffer.
    '''
    result = []
    for array in zip(*args):
        result.append(tuple(flatten(array)))
    return result

def flatten(array):
    '''Flattens the elements of the provided array, `data`.

        >>> a = [(0, 0), (1, 0), (2, 0), (3, 0)]
        >>> flatten(a)
        [0, 0, 1, 0, 2, 0, 3, 0]

    The flattening process is not recursive, it is only one level deep.
    '''
    result = []
    for value in array:
        result.extend(value)
    return result

def distinct(iterable, keyfunc=None):
    '''Yields distinct items from `iterable` in the order that they appear.
    '''
    seen = set()
    for item in iterable:
        key = item if keyfunc is None else keyfunc(item)
        if key not in seen:
            seen.add(key)
            yield item

def ray_triangle_intersection(v1, v2, v3, o, d):
    '''Computes the distance from a point to a triangle given a ray.
    '''
    eps = 1e-6
    e1 = sub(v2, v1)
    e2 = sub(v3, v1)
    p = cross(d, e2)
    det = dot(e1, p)
    if abs(det) < eps:
        return None
    inv = 1.0 / det
    t = sub(o, v1)
    u = dot(t, p) * inv
    if u < 0 or u > 1:
        return None
    q = cross(t, e1)
    v = dot(d, q) * inv
    if v < 0 or v > 1:
        return None
    t = dot(e2, q) * inv
    if t > eps:
        return t
    return None
