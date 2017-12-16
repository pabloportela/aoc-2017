


def get_checksum(rows):
    return sum(row_diff(row) for row in rows)

def row_diff(row):
    return max(row) - min(row)

def test():
    rows = [
        [5, 1, 9, 5],
        [7, 5, 3],
        [2, 4, 6, 8]]
    assert(get_checksum(rows) == 18)


if __name__ == '__main__':
    test()

    with open('day2_input.txt') as f:
        lines = f.readlines()

    rows = [[int(field) for field in line.split('\t')] for line in lines]

    print(get_checksum(rows))

