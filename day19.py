#!/usr/bin/python3.5

import sys



def collect_word(grid):
    # grid is a list of lists thus grid[row][col], or grid[y][x]

    letters = []
    col = find_start(grid)
    go_straight(grid, (0, col), (1, 0), letters)

    return ''.join(letters)


def is_within_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def go_straight(grid, p, direction, letters):

    assert(is_within_bounds(grid, p[0], p[1]))
    c = grid[p[0]][p[1]]

    if c == ' ':
        # done, reclaim stack with great pride
        return

    elif c == '+':
        # change direction
        direction = get_turning_direction(grid, p, direction)

    elif c.isalpha():
        # collect letter, keep on going
        letters.append(c)

    else:
        assert(c in ('-', '|'))

    go_straight(grid, (p[0] + direction[0], p[1] + direction[1]), direction, letters)


def get_turning_direction(grid, p, direction):

    # going horizontal, switching to vertical
    if direction in ((0, 1), (0, -1)):
        # try upwards
        d = (p[0] - 1, p[1])
        if is_within_bounds(grid, d[0], d[1]):
            c = grid[d[0]][d[1]]
            if c.isalpha() or c == '|':
                return (-1, 0)

        # should be downwards
        d = (p[0] + 1, p[1])
        assert(is_within_bounds(grid, d[0], d[1]))
        c = grid[d[0]][d[1]]
        assert(c.isalpha() or c == '|')
        return (1, 0)

    # going vertical, switching to horizontal
    else:
        assert(direction in ((1, 0), (-1, 0)))
        # try right
        d = (p[0], p[1] + 1)
        if is_within_bounds(grid, d[0], d[1]):
            c = grid[d[0]][d[1]]
            if c.isalpha() or c == '-':
                return (0, 1)

        # should be left
        d = (p[0], p[1] - 1)
        assert(is_within_bounds(grid, d[0], d[1]))
        c = grid[d[0]][d[1]]
        assert(c.isalpha() or c == '-')
        return (0, -1)


def find_start(grid):
    return grid[0].index('|')


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def test():
    grid = [
       list('     |          '),
       list('     |  +--+    '),
       list('     A  |  C    '),
       list(' F---|----E|--+ '),
       list('     |  |  |  D '),
       list('     +B-+  +--+ '),
    ]
    assert(collect_word(grid) == 'ABCDEF')


def main():
    # test()

    with open('day19_input.txt') as f:
        grid = [list(l) for l in f.readlines()]

    # print_grid(grid)
    sys.setrecursionlimit(50000)
    print(collect_word(grid))


main()

