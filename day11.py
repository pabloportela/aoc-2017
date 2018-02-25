

def get_distance(steps):
    steps = steps.split(',')
    north, east = get_summarised_steps(steps)

    if north * 2 > east:
        # above the line
        return int(north + (float(east) / 2))

    else:
        # on or down such rect
        return east


def get_summarised_steps(steps):
    north = 0
    east = 0
    for step in steps:
        if step == 's':
            north -= 1
        elif step == 'n':
            north += 1
        elif step == 'ne':
            north += 0.5
            east += 1
        elif step == 'nw':
            north += 0.5
            east -= 1
        elif step == 'sw':
            north -= 0.5
            east -= 1
        elif step == 'se':
            north -= 0.5
            east += 1

    # abs so we make everything analogue to the first cuadrant
    return abs(north), abs(east)


def read_file(filename):
    with open(filename) as f:
        return f.read().strip()

def test():
    assert(get_distance('ne,ne,ne') == 3)
    assert(get_distance('ne,ne,sw,sw') == 0)
    assert(get_distance('ne,ne,s,s') == 2)
    assert(get_distance('se,sw,se,sw,sw') == 3)

if __name__ == '__main__':
    test()

    steps = read_file('day11_input.txt')
    print(get_distance(steps))
