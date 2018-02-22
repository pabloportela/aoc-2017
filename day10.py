
def get_hash(list_size, lengths):
    circle = list(range(list_size))
    current_position = 0
    skip_size = 0

    for length in lengths:
        reverse_range(circle, current_position, length)
        current_position += length + skip_size
        skip_size += 1

    return circle[0] * circle[1]
        
def reverse_range(circle, start, length):
    size = len(circle)
    finish = start + length - 1

    while start < finish:
        wrapped_swap(circle, start, finish)
        start += 1
        finish -= 1

def wrapped_swap(circle, a, b):
    size = len(circle)
    a %= size
    b %= size
    circle[a], circle[b] = circle[b], circle[a]


def test():
    l = list(range(3))
    reverse_range(l, 0, 3)
    assert(l == [2, 1, 0])

    l = list(range(5))
    reverse_range(l, 4, 2)
    assert(l == [4, 1, 2, 3, 0])

    assert(get_hash(5, [3, 4, 1, 5]) == 12)


if __name__ == '__main__':
    test()
    lengths = [88, 88, 211, 106, 141, 1, 78, 254, 2, 111, 77, 255, 90, 0, 54, 205]
    print(get_hash(256, lengths))
