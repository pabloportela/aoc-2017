#!/usr/bin/python3.5


class Scanner(object):

    def __init__(self, layer_to_range):
        self.layer_to_range = layer_to_range
        self.q_layers = max(layer_to_range.keys()) + 1

    def _get_scanner_position(self, layer, interval):
        if layer not in self.layer_to_range:
            return None

        r = self.layer_to_range[layer]
        if r == 1:
            return 0

        if r == 2:
            return interval % 2

        # sequence 0, 1, 2,...,r-2,r-1,r-2,...1
        s = list(range(r)) + list(range(r-2, 0, -1))

        # sequence repeates itself every (range-1)*2 intervals
        p = interval % ((r-1) * 2)

        return s[p]

    def _is_interval_safe(self, layer, interval):
        if self._get_scanner_position(layer, interval) == 0:
            # busted
            return True

        else:
            # ass saved
            return False

    def _is_trip_safe(self, delay):
        for layer in range(self.q_layers):
            if self._is_interval_safe(layer, delay + layer):
                return True

        return False

    def get_safe_trip_wait_time(self):
        w = 0
        while self._is_trip_safe(w):
            w += 1

        if w % 10000 == 0:
            print(w)
        return w


def test():
    layer_to_range = {0: 3, 1: 2, 4: 4, 6: 4}
    scanner = Scanner(layer_to_range)

    # 10th picosecond
    assert(scanner._get_scanner_position(0, 10) == 2)
    assert(scanner._get_scanner_position(1, 10) == 0)
    assert(scanner._get_scanner_position(2, 10) == None)
    assert(scanner._get_scanner_position(3, 10) == None)
    assert(scanner._get_scanner_position(4, 10) == 2)
    assert(scanner._get_scanner_position(5, 10) == None)
    assert(scanner._get_scanner_position(6, 10) == 2)

    # 16th picosecond
    assert(scanner._get_scanner_position(0, 16) == 0)
    assert(scanner._get_scanner_position(1, 16) == 0)
    assert(scanner._get_scanner_position(2, 16) == None)
    assert(scanner._get_scanner_position(3, 16) == None)
    assert(scanner._get_scanner_position(4, 16) == 2)
    assert(scanner._get_scanner_position(5, 16) == None)
    assert(scanner._get_scanner_position(6, 16) == 2)

    assert(scanner.get_safe_trip_wait_time() == 10)


if __name__ == '__main__':
    test()
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
    print(scanner.get_safe_trip_wait_time())


