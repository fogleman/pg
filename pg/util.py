def hex_color(value):
    r = ((value >> (8 * 2)) & 255) / 255.0
    g = ((value >> (8 * 1)) & 255) / 255.0
    b = ((value >> (8 * 0)) & 255) / 255.0
    return (r, g, b)

def normalize(vector):
    d = sum(x * x for x in vector) ** 0.5
    return tuple(x / d for x in vector)

def distance(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def interleave(sizes, arrays):
    result = []
    count = len(sizes)
    indexes = [0] * count
    length = min(len(array) / size for size, array in zip(sizes, arrays))
    for _ in xrange(length):
        for i in xrange(count):
            index = indexes[i]
            size = sizes[i]
            result.extend(arrays[i][index:index+size])
            indexes[i] += size
    return result
