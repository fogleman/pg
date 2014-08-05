from core import normalize

def _sphere(radius, detail, result, a, b, c):
    if detail == 0:
        result.extend(a)
        result.extend(b)
        result.extend(c)
    else:
        ab = normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
        ac = normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
        bc = normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
        _sphere(radius, detail - 1, result, a, ab, ac)
        _sphere(radius, detail - 1, result, b, bc, ab)
        _sphere(radius, detail - 1, result, c, ac, bc)
        _sphere(radius, detail - 1, result, ab, bc, ac)

def sphere(radius, detail):
    indices = [
        (4, 3, 0), (1, 4, 0), (3, 4, 5), (4, 1, 5),
        (0, 3, 2), (0, 2, 1), (5, 2, 3), (5, 1, 2),
    ]
    positions = [
        (0, 0, -1), (1, 0, 0), (0, -1, 0),
        (-1, 0, 0), (0, 1, 0), (0, 0, 1),
    ]
    result = []
    for a, b, c in indices:
        a, b, c = positions[a], positions[b], positions[c]
        _sphere(radius, detail, result, a, b, c)
    return result
