#!/usr/bin/python3.6


class Scanner(object):

    def __init__(self, layer_to_range):
        self.layer_to_range = layer_to_range
        self.q_layers = max(layer_to_range.keys()) + 1

    def _get_scanner_position(self, i):
        r = self.layer_to_range[i]
        if r == 1:
            return 0

        if r == 2:
            return i % 2

        # sequence 0, 1, 2,...,r-2,r-1,r-2,...1
        s = list(range(r)) + list(range(r-2, 0, -1))

        # sequence repeates itself every (range-1)*2 intervals
        p = i % ((r-1) * 2)

        return s[p]

    def _get_interval_severity(self, i):
        if i not in self.layer_to_range:
            # no scanning in this layer
            return 0

        elif self._get_scanner_position(i) == 0:
            # busted
            return i * self.layer_to_range[i]

        else:
            # ass saved
            return 0

    def get_trip_severity(self):
        return sum(self._get_interval_severity(i) for i in range(self.q_layers))


def test():
    layer_to_range = {0: 3, 1: 2, 4: 4, 6: 4}
    scanner = Scanner(layer_to_range)
    assert(scanner.get_trip_severity() == 24)


if __name__ == '__main__':
    layer_to_range = {
        0: 5,
        1: 2,
        2: 3,
        4: 4,
        6: 6,
        8: 4,
        10: 6,
        12: 10,
        14: 6,
        16: 8,
        18: 6,
        20: 9,
        22: 8,
        24: 8,
        26: 8,
        28: 12,
        30: 12,
        32: 8,
        34: 8,
        36: 12,
        38: 14,
        40: 12,
        42: 10,
        44: 14,
        46: 12,
        48: 12,
        50: 24,
        52: 14,
        54: 12,
        56: 12,
        58: 14,
        60: 12,
        62: 14,
        64: 12,
        66: 14,
        68: 14,
        72: 14,
        74: 14,
        80: 14,
        82: 14,
        86: 14,
        90: 18,
        92: 17}

    scanner = Scanner(layer_to_range)
    print(scanner.get_trip_severity())


