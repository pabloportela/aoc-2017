

def count_jumps_out(maze):
    i = 0
    last = len(maze) - 1
    q_jumps = 0

    while 0 <= i <= last:
        jump = maze[i]
        maze[i] += -1 if maze[i] >= 3 else 1
        i += jump
        q_jumps += 1

    return q_jumps

def test():
    assert(count_jumps_out([0, 3, 0, 1, -3]) == 10)

if __name__ == '__main__':
    test()

    with open('day5_input.txt') as f:
        lines = f.readlines()

    maze = [int(l.strip()) for l in lines]

    print(count_jumps_out(maze))

