#!/usr/bin/python3.5


class DuelingGenerator(object):

    def __init__(self, seed, factor, max_iterations):
        self.seed = seed
        self.factor = factor
        self.max_iterations = max_iterations

    def __iter__(self):
        self.current = self.seed
        self.i_count = 0
        return self

    def __next__(self):
        if self.i_count == self.max_iterations:
            raise StopIteration

        self.i_count += 1
        self.current = (self.current * self.factor) % 2147483647
        return self.current


def compute_judge_count(factor_a, factor_b):
    gen_a = DuelingGenerator(factor_a, 16807, 40000000)
    gen_b = DuelingGenerator(factor_b, 48271, 40000000)

    return sum(1 for a, b in zip(gen_a, gen_b) if (a & 65535) == (b & 65535))


def main():
    assert(compute_judge_count(65, 8921) == 588)
    print(compute_judge_count(703, 516))



main()
