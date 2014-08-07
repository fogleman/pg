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
