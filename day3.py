

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

def get_q_steps(n):
    movement = movement_generator()
    x = y = 0
    # import pdb
    # pdb.set_trace()
    for i in range(n-1):
        next_movement = movement.next()
        x += next_movement[0]
        y += next_movement[1]

    return abs(x) + abs(y)

def test():
    assert(get_q_steps(1) == 0)
    assert(get_q_steps(12) == 3)
    assert(get_q_steps(23) == 2)
    assert(get_q_steps(1024) == 31)

if __name__ == '__main__':
    test()
    print(get_q_steps(265149))

