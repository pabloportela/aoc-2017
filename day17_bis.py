#!/usr/bin/python3.5



def get_value_after_zero(q_steps):

    # for i in range(1, 50000000):
    after_zero = None
    position = 0

    for i in range(1, 50000001):
        position = (position + q_steps + 1) % i
        if position == 0:
            after_zero = i

    return after_zero


def main():
    print(get_value_after_zero(328))



main()
