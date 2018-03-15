#!/usr/bin/python3.5


from collections import defaultdict, deque



class BlockException(Exception):
    pass

class Processor(object):

    def __init__(self, lines, program_id):
        self._registers = defaultdict(int)
        self._registers['p'] = program_id
        self._in_queue = deque()
        self._out_queue = None
        self._snd_call_count = 0
        self._curr_line = 0

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


    def _is_incomplete(self):
        return 0 <= self._curr_line < self._q_instructions


    def get_snd_call_count(self):
        return self._snd_call_count


    def set_out_queue(self, queue):
        self._out_queue = queue


    def get_in_queue(self):
        return self._in_queue


    def _resolve(self, arg):
        if isinstance(arg, int):
            # integer value
            return arg

        else:
            # string, dereference register
            return self._registers[arg]


    def try_to_run(self):

        if self._is_incomplete():
            try:
                op, args = self._instructions[self._curr_line]
                op(*args)
                self._curr_line += 1
                return True

            except BlockException:
                return False

        else:
            return False


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
    # some are obsolete but they still have to execute for compatibility

    def _op_snd(self, x, y):
        self._snd_call_count += 1
        self._out_queue.append(self._resolve(x))

    def _op_set(self, x, y):
        self._registers[x] = self._resolve(y)

    def _op_add(self, x, y):
        self._registers[x] += self._resolve(y)

    def _op_mul(self, x, y):
        self._registers[x] *= self._resolve(y)

    def _op_mod(self, x, y):
        self._registers[x] %= self._resolve(y)

    def _op_rcv(self, x, y):
        if not self._in_queue:
            raise BlockException()

        else:
            self._registers[x] = self._in_queue.popleft()


    def _op_jgz(self, x, y):
        if self._resolve(x) > 0:
            # minus one, to neutralise line increment from the executor
            self._curr_line += self._resolve(y) - 1



def dual_concurrent_run(p0, p1):
    p0.set_out_queue(p1.get_in_queue())
    p1.set_out_queue(p0.get_in_queue())

    while p0.try_to_run() or p1.try_to_run():
        pass

def test():
    lines = [
        'snd 1',
        'snd 2',
        'snd p',
        'rcv a',
        'rcv b',
        'rcv c',
        'rcv d',
    ]
    p0 = Processor(lines, 0)
    p1 = Processor(lines, 1)
    dual_concurrent_run(p0, p1)

    assert(p1.get_snd_call_count() == 3)


def main():
    test()

    with open('day18_input.txt') as f:
        lines = f.readlines()

    p0 = Processor(lines, 0)
    p1 = Processor(lines, 1)
    dual_concurrent_run(p0, p1)

    print(p1.get_snd_call_count())



main()
