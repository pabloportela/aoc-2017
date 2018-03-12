#!/usr/bin/python3.5


from collections import deque



def main():
    assert(dance('abcde', ['s1', 'x3/4', 'pe/b']) == 'baedc')

    moves = parse_moves('day16_input.txt')
    dancers = 'abcdefghijklmnop'
    print(dance(dancers, moves))


def parse_moves(filename):
    with open(filename) as f:
         return f.read().split(',')


def dance(dancers, moves):
    dancers = deque(dancers)
    for move in moves:
        perform_move(move, dancers)

    return ''.join(dancers)


def perform_move(move, dancers):
    op = move[0]
    data = move[1:]
    q_dancers = len(dancers) 

    if op == 's':
        # spin (rotate)
        size = int(data) % q_dancers
        dancers.rotate(size)
                
    elif op == 'x':
        # exchange (swap by offset)
        a, b = map(int, data.split('/'))
        assert(0 <= a < q_dancers and 0 <= b < q_dancers)
        dancers[a], dancers[b] = dancers[b], dancers[a]

    elif op == 'p':
        # parner (swap by value)
        a, b = (dancers.index(c) for c in data.split('/'))
        assert(0 <= a < q_dancers and 0 <= b < q_dancers)
        dancers[a], dancers[b] = dancers[b], dancers[a]


main()
