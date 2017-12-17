
def get_checksum(rows):
    return sum(row_even_division_sum(row) for row in rows)

def row_even_division_sum(row):
    acc = 0
    sr = sorted(row, reverse=True)
    l = len(sr)

    for i in range(1, l):
        for j in range(i, l):
            d, m = divmod(sr[i-1], sr[j])
            if not m:
                acc += d

    return acc

def test():
    rows = [
        [5, 9, 2, 8],
        [9, 4, 7, 3],
        [3, 8, 6, 5]]
    assert(get_checksum(rows) == 9)

if __name__ == '__main__':
    test()

    with open('day2_input.txt') as f:
        lines = f.readlines()

    rows = [[int(field) for field in line.split('\t')] for line in lines]

    print(get_checksum(rows))
