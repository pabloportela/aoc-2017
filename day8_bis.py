from collections import defaultdict


def parse_lines(lines):
    return [l.strip().split(' ') for l in lines]

def comparison_is_true(a, op, b):
    ops = {
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
        '>':  lambda a, b: a > b,
        '<':  lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
    }
    return bool(ops[op](a, b))
    

def execute_instructions(instructions):
    max_value = -float("inf")
    registers = defaultdict(int)
    for ins in instructions:
        if not comparison_is_true(registers[str(ins[4])], ins[5], int(ins[6])):
            factor = 0
        elif ins[1] == 'inc':
            factor = 1
        else:
            factor = -1

        registers[ins[0]] += int(ins[2]) * factor
        max_value = max(registers[ins[0]], max_value)

    return registers, max_value

def largest_registry_value(registers):
    return max(registers.values())

def test():
    lines = [
        'b inc 5 if a > 1',
        'a inc 1 if b < 5',
        'c dec -10 if a >= 1',
        'c inc -20 if c == 10'
    ]
    instructions = parse_lines(lines)
    registers, max_value = execute_instructions(instructions)
    assert(max_value == 10)

if __name__ == '__main__':
    test()

    with open('day8_input.txt') as f:
        lines = f.readlines()

    instructions = parse_lines(lines)
    registers, max_value = execute_instructions(instructions)
    print(max_value)
