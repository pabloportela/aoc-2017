#!/usr/bin/python3.5


from collections import deque



def main():
    assert(dance('abcde', ['s1', 'x3/4', 'pe/b'], 1) == 'baedc')

    moves = parse_moves('day16_input.txt')
    dancers = 'abcdefghijklmnop'
    print(dance(dancers, moves, 1000000000))


def parse_moves(filename):
    with open(filename) as f:
         return f.read().split(',')


def dance(dancers, moves, q_iterations):

    # pre-parse moves and have functions and arguments ready
    move_ops = list(map(get_move_op, moves))

    # using deque for efficient rotation
    dancers_queue = deque(dancers)

    for i in range(q_iterations):
        for move_op, args in move_ops:
            # they all take current dancers_queue as first param 
            # the other params are constant so they were computed already
            move_op(dancers_queue, *args)

        # check if dancers look just like the beginning, thus cyclic process
        if ''.join(dancers_queue) == dancers:
            # dancing till the remainder should be the same as till q_iterations
            return dance(dancers, moves, q_iterations % (i+1))

    # we get a string, we return a string
    return ''.join(dancers_queue)


def op_spin(dancers, offset):
    # rotate
    dancers.rotate(offset % len(dancers))


def op_exchange(dancers, a, b):
    # swap by offset
    dancers[a], dancers[b] = dancers[b], dancers[a]


def op_partner(dancers, val_a, val_b):
    # swap by value
    a = dancers.index(val_a)
    b = dancers.index(val_b)
    dancers[a], dancers[b] = dancers[b], dancers[a]


def get_move_op(move):
    op = move[0]
    data = move[1:]

    if op == 's':
        return op_spin, (int(data), )
                
    elif op == 'x':
        a, b = map(int, data.split('/'))
        return op_exchange, (a, b)

    elif op == 'p':
        a, b = data.split('/')
        return op_partner, (a, b)


main()
