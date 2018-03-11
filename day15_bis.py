#!/usr/bin/python3.5


class DuelingGenerator(object):

    def __init__(self, seed, factor, max_iterations, multiple):
        self.seed = seed
        self.factor = factor
        self.max_iterations = max_iterations
        self.multiple = multiple

    def __iter__(self):
        self.current = self.seed * self.factor
        self.i_count = 0
        return self

    def __next__(self):
        if self.i_count == self.max_iterations:
            raise StopIteration

        self.i_count += 1

        while not self._successful_increment():
            pass

        return self.current

    def _successful_increment(self):
        self.current = (self.current * self.factor) % 2147483647
        return not bool(self.current % self.multiple)


def compute_judge_count(factor_a, factor_b):
    gen_a = DuelingGenerator(factor_a, 16807, 5000000, 4)
    gen_b = DuelingGenerator(factor_b, 48271, 5000000, 8)

    return sum(1 for a, b in zip(gen_a, gen_b) if (a & 65535) == (b & 65535))


def main():
    assert(compute_judge_count(65, 8921) == 309)
    print(compute_judge_count(703, 516))



main()
