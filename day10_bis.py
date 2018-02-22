

def get_hash(ascii_lengths):
    lengths = get_lengths(ascii_lengths)
    circle = list(range(256))
    current_position = 0
    skip_size = 0

    for _ in range(64):
        for length in lengths:
            reverse_range(circle, current_position, length)
            current_position += length + skip_size
            skip_size += 1

    return dense_hash(circle).lower()


def dense_hash(circle):
    assert(len(circle) == 256)
    
    processed_block = [process_block(circle[i * 16: i * 16 + 16]) for i in range(16)]
    return ''.join(processed_block)
        

def process_block(block):
    block = list(block)
    hexa = reduce(lambda x, y: x ^ y, block)
    return '{:02X}'.format(hexa)

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


def ascii_to_int(ascii_lengths):
    return [ord(c) for c in ascii_lengths]


def get_lengths(ascii_lengths):
    return ascii_to_int(ascii_lengths) + [17, 31, 73, 47, 23]


def test():
    assert(ascii_to_int('1,2,3') == [49, 44, 50, 44, 51])
    assert(get_lengths('1,2,3') == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23])

    assert(get_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272')
    assert(get_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd')
    assert(get_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d')
    assert(get_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e')


if __name__ == '__main__':
    test()
    ascii_lengths = '88,88,211,106,141,1,78,254,2,111,77,255,90,0,54,205'
    print(get_hash(ascii_lengths))
