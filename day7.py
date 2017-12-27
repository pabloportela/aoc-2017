

def parse_line(line):
    pair = line.split('->')
    name = pair[0].split()[0].strip()

    if len(pair) == 1:
        children = []
    else:
        children = [c.strip() for c in pair[1].split(',')]

    return name, children


def parse_lines(lines):
    return {p[0]: p[1] for p in (parse_line(l) for l in lines)}


if __name__ == '__main__':
    # test()

    with open('day7_input.txt') as f:
        lines = f.readlines()

    discs = parse_lines(lines)

    for k, v in discs.items():
        if not v and k in discs:
            # no children, can't be root
            del discs[k]
        else:
            # no child can be root
            for c in v:
                if c in discs:
                    del discs[c]

    assert(len(discs) == 1)
    print(discs.keys()[0])
