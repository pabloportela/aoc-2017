

def count_unique_cycles(banks):
    q_cycles = 1
    signatures = set([get_bank_signature(banks)])

    redistribute_banks(banks)
    signature = get_bank_signature(banks)

    while signature not in signatures:
        # accumulate
        q_cycles += 1
        signatures.add(signature)

        # try again
        redistribute_banks(banks)
        signature = get_bank_signature(banks)

    return q_cycles


def redistribute_banks(banks):
    ''' redistributes in-place '''

    size = len(banks)
    amount = max(banks)
    index = banks.index(amount)
    banks[index] = 0

    while amount:
        index += 1
        banks[index % size] += 1
        amount -= 1


def get_bank_signature(banks):
    return '-'.join(map(str, banks))


def parse_banks(filename):
    with open(filename) as f:
        line = f.read()

    return [int(f.strip()) for f in line.split()]


def test():
    assert(count_unique_cycles([0, 2, 7, 0]) == 5)
    assert(count_unique_cycles([1, 2, 3]) == 3)


if __name__ == '__main__':
    test()
    banks = parse_banks('day6_input.txt')
    count_unique_cycles(banks)
    # again, but start from the repeated position 
    print(count_unique_cycles(banks))

