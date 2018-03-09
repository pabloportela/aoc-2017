#!/usr/local/bin/python3


def get_network_size(item, pipe_connections):
    pipe_visited = {p: False for p in list(pipe_connections.keys())}
    pipe_visited[item] = True
    visit_connections(item, pipe_connections, pipe_visited)
    return sum(pipe_visited.values())


def visit_connections(item, pipe_connections, pipe_visited):
    for c in pipe_connections[item]:
        if pipe_visited[c] is False:
            pipe_visited[c] = True
            visit_connections(c, pipe_connections, pipe_visited)


def process_file(filename):
    with open(filename) as f:
        pipe_connections = {int(t[0]): [int(p) for p in t[1].split(',')] for t in [l.split('<->') for l in f.readlines()]}

    return get_network_size(0, pipe_connections)

    process_file('day12_input.txt')



if __name__ == '__main__':
    assert(process_file('day12_input_alt.txt') == 6)

    print(process_file('day12_input.txt'))
