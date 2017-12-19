

def direction_generator():
    while True:
        yield 1, 0
        yield 0, 1
        yield -1 ,0
        yield 0, -1

def movement_generator():
    direction = direction_generator()
    yield direction.next()
    yield direction.next()
    side = 2
    while True:
        # cover two sides, then increment side size
        next_direction = direction.next()
        for i in range(side):
            yield next_direction

        next_direction = direction.next()
        for i in range(side):
            yield next_direction

        side += 1

def get_step_gte(n):
    movement = movement_generator()
    x = y = 0
    g = Grid(10)
    g.set(0, 0, 1)
    # import pdb
    # pdb.set_trace()
    v = 1
    while v < n:
        next_movement = movement.next()
        x += next_movement[0]
        y += next_movement[1]
        v = g.get_surroundings_sum(x, y)
        g.set(x, y, v)

    return v


class Grid(object):
    def __init__(self, size):
        self.offset = size // 2
        self.size = size
        self.grid = [None] * size
        for i in range(size):
            self.grid[i] = [0] * size

    def print_grid(self):
        for i in self.grid:
            print(i)

    def set(self, x, y, v):
        try:
            self.grid[x + self.offset][y + self.offset] = v
            self.print_grid()
        except IndexError:
            print('Try a bigger grid for', (x, y))
            raise

    def get(self, x, y):
        try:
            return self.grid[x - self.offset][y - self.offset]
        except IndexError:
            print('Try a bigger grid for', (x, y))
            raise

    def get_surroundings(self, x, y):
        return [
            self.get(x+1, y),
            self.get(x+1, y+1),
            self.get(x, y+1),
            self.get(x-1, y+1),
            self.get(x-1, y),
            self.get(x-1, y-1),
            self.get(x, y-1),
            self.get(x+1, y-1)]

    def get_surroundings_sum(self, x, y):
        return sum(self.get_surroundings(x, y))


def test():
    assert(get_step_gte(1) == 1)
    assert(get_step_gte(2) == 2)
    assert(get_step_gte(3) == 4)
    assert(get_step_gte(6) == 10)
    assert(get_step_gte(23) == 23)
    assert(get_step_gte(24) == 25)
    assert(get_step_gte(59) == 59)
    assert(get_step_gte(331) == 351)

if __name__ == '__main__':
    test()
    print(get_step_gte(265149))

