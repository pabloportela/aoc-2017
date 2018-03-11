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


class Grid(object):

    grid_side = 128

    def __init__(self, key):
        self.grid = self._compute_grid(key)
        self.print_grid()

    def get_q_regions(self):
        nr = 1
        while self._set_next_region(nr):
            nr += 1

        self.print_grid()
        return nr - 1


    def _set_next_region(self, next_region):
        x, y = self._find_used_point()
        if x is None or y is None:
            # no more regions to cover
            return False

        self._bucket_paint(x, y, self.grid[x][y], next_region)

        return True


    def _bucket_paint(self, x, y, s, r):
        ''' Generic paint function '''
        if (
            0 <= x < self.grid_side and
            0 <= y < self.grid_side and
            self.grid[x][y] == s
        ):
            # within bonds and not painted
            self.grid[x][y] = r
            
            # try to find the next point to paint in all four directions
            self._bucket_paint(x + 1, y, s, r)
            self._bucket_paint(x - 1, y, s, r)
            self._bucket_paint(x, y + 1, s, r)
            self._bucket_paint(x, y - 1, s, r)
        

    def _find_used_point(self):
        for x in range(self.grid_side):
            for y in range(self.grid_side):
                if self.grid[x][y] == '#':
                    return x, y

        return None, None


    def print_grid(self):
        for r in self.grid[:20]:
            print(''.join('{}'.format(c) for c in r[:20]))


    @classmethod
    def _compute_grid(cls, key):
        return [cls._get_grid_row(get_hash('{}-{}'.format(key, i))) for i in range(128)]


    @staticmethod
    def _get_grid_row(s):
        return list(''.join('{:04b}'.format(int(c, 16)) for c in s).replace('0', '.').replace('1', '#'))


def main():
    grid = Grid('flqrgnkx')
    q_regions = grid.get_q_regions()
    print(q_regions)
    assert(q_regions == 1242)
    
    grid = Grid('wenycdww')
    print(grid.get_q_regions())


if __name__ == '__main__':
    main()
