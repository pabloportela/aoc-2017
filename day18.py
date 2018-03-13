#!/usr/bin/python3.5


from collections import defaultdict


class Processor(object):
    '''
    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
    '''


    def __init__(self, lines):
        self._registers = defaultdict(int)
        self.last_note = None
        self._ops = {
            'snd': self._op_snd,
            'set': self._op_set,
            'add': self._op_add,
            'mul': self._op_mul,
            'mod': self._op_mod,
            'rcv': self._op_rcv,
            'jgz': self._op_jgz,
        }
        self._instructions = self._parse_lines(lines)
        self._q_instructions = len(self._instructions)

        self._process()


    def _resolve(self, arg):
        if isinstance(arg, int):
            # integer value
            return arg

        else:
            # string, dereference register
            return self._registers[arg]


    def _process(self):
        self._curr_line = 0
        while 0 <= self._curr_line < self._q_instructions:
            op, args = self._instructions[self._curr_line]
            op(*args)
            self._curr_line += 1


    def _parse_lines(self, lines):
        return [self._parse_line(line) for line in lines]


    def _parse_line(self, line):
        ''' takes a line string, returns an op tuple '''
        assert(isinstance(line, str))
        split_line = [x.strip() for x in line.split(' ')]
        assert(isinstance(split_line, list) and 2 <= len(split_line) <= 3)
        assert(split_line[0] in self._ops)

        op = self._ops[split_line[0]]
        set_datatype = lambda x: x if x.isalpha() else int(x)
        arg1 = set_datatype(split_line[1])
        arg2 = set_datatype(split_line[2]) if len(split_line) == 3 else None

        return op, (arg1, arg2)

    # operations

    def _op_snd(self, x, y):
        self.last_note = self._resolve(x)

    def _op_set(self, x, y):
        self._registers[x] = self._resolve(y)

    def _op_add(self, x, y):
        self._registers[x] += self._resolve(y)

    def _op_mul(self, x, y):
        self._registers[x] *= self._resolve(y)

    def _op_mod(self, x, y):
        self._registers[x] %= self._resolve(y)

    def _op_rcv(self, x, y):
        if self._registers[x] != 0:
            # force bail out
            self._curr_line = -2

    def _op_jgz(self, x, y):
        if self._resolve(x) > 0:
            # minus one, to neutralise line increment from the executor
            self._curr_line += self._resolve(y) - 1


def test():
    lines = [
        'set a 1',
        'add a 2',
        'mul a a',
        'mod a 5',
        'snd a',
        'set a 0',
        'rcv a',
        'jgz a -1',
        'set a 1',
        'jgz a -2'
    ]
    p = Processor(lines)
    assert(p.last_note == 4)


def main():
    test()

    with open('day18_input.txt') as f:
        lines = f.readlines()

    p = Processor(lines)
    print(p.last_note)


main()
