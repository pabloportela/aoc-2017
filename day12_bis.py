#!/usr/local/bin/python3


def get_q_networks(pipe_connections):
    pipe_group = {p: 0 for p in list(pipe_connections.keys())}
    group = 1
    for item in pipe_connections.keys():
        if pipe_group[item] == 0:
            pipe_group[item] = group
            set_group(item, pipe_connections, pipe_group, group)
            group += 1

    return len(set(pipe_group.values()))


def set_group(item, pipe_connections, pipe_group, group):
    for c in pipe_connections[item]:
        if pipe_group[c] is 0:
            pipe_group[c] = group
            set_group(c, pipe_connections, pipe_group, group)


def process_file(filename):
    with open(filename) as f:
        pipe_connections = {int(t[0]): [int(p) for p in t[1].split(',')] for t in [l.split('<->') for l in f.readlines()]}

    return get_q_networks(pipe_connections)

    process_file('day12_input.txt')


if __name__ == '__main__':
    assert(process_file('day12_input_alt.txt') == 2)

    print(process_file('day12_input.txt'))
