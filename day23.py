#!/usr/bin/python3.5


from collections import defaultdict


class Processor(object):

    def __init__(self, lines):
        self._registers = defaultdict(int)
        self.mul_call_count = 0
        self._ops = {
            'set': self._op_set,
            'sub': self._op_sub,
            'mul': self._op_mul,
            'jnz': self._op_jnz,
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
        assert(isinstance(split_line, list) and len(split_line) == 3)
        assert(split_line[0] in self._ops)

        op = self._ops[split_line[0]]
        set_datatype = lambda x: x if x.isalpha() else int(x)
        arg1 = set_datatype(split_line[1])
        arg2 = set_datatype(split_line[2]) if len(split_line) == 3 else None

        return op, (arg1, arg2)

    # operations

    def _op_set(self, x, y):
        self._registers[x] = self._resolve(y)

    def _op_sub(self, x, y):
        self._registers[x] -= self._resolve(y)

    def _op_mul(self, x, y):
        self.mul_call_count += 1
        self._registers[x] *= self._resolve(y)

    def _op_jnz(self, x, y):
        if self._resolve(x) != 0:
            # minus one, to neutralise line increment from the executor
            self._curr_line += self._resolve(y) - 1


def main():

    with open('day23_input.txt') as f:
        lines = f.readlines()

    p = Processor(lines)
    print(p.mul_call_count)


main()
