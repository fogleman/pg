from util import normalize

def _sphere(detail, radius, center, result, a, b, c):
    if detail == 0:
        result.extend([radius * a[i] + center[i] for i in xrange(3)])
        result.extend([radius * b[i] + center[i] for i in xrange(3)])
        result.extend([radius * c[i] + center[i] for i in xrange(3)])
    else:
        ab = normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
        ac = normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
        bc = normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
        _sphere(detail - 1, radius, center, result, a, ab, ac)
        _sphere(detail - 1, radius, center, result, b, bc, ab)
        _sphere(detail - 1, radius, center, result, c, ac, bc)
        _sphere(detail - 1, radius, center, result, ab, bc, ac)

def sphere(detail, radius=0.5, center=(0, 0, 0)):
    indices = [
        (0, 3, 4), (0, 4, 1), (5, 4, 3), (5, 1, 4),
        (2, 3, 0), (1, 2, 0), (3, 2, 5), (2, 1, 5),
    ]
    positions = [
        (0, 0, -1), (1, 0, 0), (0, -1, 0),
        (-1, 0, 0), (0, 1, 0), (0, 0, 1),
    ]
    result = []
    for a, b, c in indices:
        a, b, c = positions[a], positions[b], positions[c]
        _sphere(detail, radius, center, result, a, b, c)
    return result
