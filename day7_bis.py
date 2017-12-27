

class Disc(object):

    def __init__(self, name, weight, children_names):
        self.name = name
        self.weight = weight
        self.children_names = children_names
        self.children = []

    def __repr__(self):
        return '{} ({}) -> {}'.format(self.name, self.weight, str(self.children_names))

    @property
    def full_weight(self):
        return self.weight + sum(c.full_weight for c in self.children)

def find_unbalanced_children(disc):
    if not disc.children:
        return

    unique_weights = set(c.full_weight for c in disc.children)
    if len(unique_weights) != 1:
        for c in disc.children:
            print(c.name, c.weight, c.full_weight)
        print('################')

        for c in disc.children:
            find_unbalanced_children(c)



def get_disc_from_line(line):
    relations = line.split('->')
    node = relations[0].split('(')
    name = node[0].strip()
    weight = node[1][:node[1].index(')')]

    if len(relations) == 1:
        children_names = []
    else:
        children_names = [c.strip() for c in relations[1].split(',')]

    return Disc(name, int(weight), children_names)


def get_discs_from_lines(lines):
    discs_by_name = {d.name: d for d in (get_disc_from_line(l) for l in lines)}
    for disc in discs_by_name.values():
        disc.children = [discs_by_name[c] for c in disc.children_names]

    return discs_by_name


def get_root_name(discs_aux):
    discs = discs_aux.copy()
    for k, v in discs.items():
        if not v.children_names and k in discs:
            # no children_names, can't be root
            del discs[k]
        else:
            # no child can be root
            for c in v.children_names:
                if c in discs:
                    del discs[c]

    assert(len(discs) == 1)
    return discs.keys()[0]



if __name__ == '__main__':

    with open('day7_input.txt') as f:
        lines = f.readlines()

    discs = get_discs_from_lines(lines)
    root_name = get_root_name(discs)
    root = discs[root_name]
    find_unbalanced_children(root)
    
