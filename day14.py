#!/usr/bin/python3.5


from functools import reduce



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

    return dense_hash(circle)


def dense_hash(circle):
    assert(len(circle) == 256)
    processed_block = [process_block(circle[i * 16: i * 16 + 16]) for i in range(16)]
    return ''.join(processed_block).lower()
        

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


def get_lengths(ascii_lengths):
    return [ord(c) for c in ascii_lengths] + [17, 31, 73, 47, 23]


def get_q_used_squares(key):
    return sum(get_q_used_squares_from_row(key, i) for i in range(1, 129))


def get_q_used_squares_from_row(key, i):
    return count_set_bits_from_hexa_str(get_hash('{}-{}'.format(key, i)))


def count_set_bits_from_hexa_str(s):
    return sum(count_set_bits_from_hexa_digit(int(c, 16)) for c in s)


def count_set_bits_from_hexa_digit(d):
    #return sum((n >> s) & 1 for s in range(4))
    assert(0 <= d < 16)
    count_lookup = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
    return count_lookup[d]



def main():
    assert(get_q_used_squares('flqrgnkx') == 8108)
    print(get_q_used_squares('wenycdww'))


if __name__ == '__main__':
    main()
