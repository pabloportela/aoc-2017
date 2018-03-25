#!/usr/bin/python3.5



class InfiniteGrid(object):

    def __init__(self, rows, c, r):
        self._initialise_quadrants(rows, c, r)


    def _initialise_quadrants(self, rows, c, r):
        self.quads = [
            list(reversed([list(row[c:]) for row in rows[:r]])),
            list(reversed([list(row[:c]) for row in reversed(rows[:r])])),
            [list(row[:c]) for row in rows[r:]],
            [list(row[c:]) for row in rows[r:]],
        ]


    def set(self, r, c, value):
        quad, r, c = self._map_quad_and_position(r, c)
        self._ensure_position_is_allocated(quad, r, c)
        quad[r][c] = value


    def get(self, r, c):
        quad, r, c = self._map_quad_and_position(r, c)
        self._ensure_position_is_allocated(quad, r, c)
        return quad[r][c]


    @staticmethod
    def _ensure_position_is_allocated(quad, r, c):
        ''' r and c are already mapped into internal offsets '''

        q_rows = len(quad)
        if q_rows <= r:
            quad.extend([] for _ in range(r + 1 - q_rows))

        q_cols = len(quad[r])
        if q_cols <= c:
            quad[r].extend(False for _ in range(c + 1 - q_cols))


    def _map_quad_and_position(self, r, c):
        if r > 0 and c >= 0:
            quad_index = 0
            r -= 1

        elif r > 0 and c < 0:
            quad_index = 1
            r -= 1
            c += 1

        elif r <= 0 and c < 0:
            quad_index = 2
            c += 1

        elif r <= 0 and c >= 0:
            quad_index = 3

        return self.quads[quad_index], abs(r), abs(c)



class InfectionGrid(object):

    def __init__(self, rows, center_row, center_col):
    
        # convert # and . to True and False
        rows = [[bool(item == '#') for item in row] for row in rows]

        self.grid = InfiniteGrid(rows, center_row, center_col)

        self.current_row = 0
        self.current_col = 0
        self.direction = 'up'


    def burst(self):
        # record how was position before this burst
        was_pre_burst_infected = self._is_current_position_infected()

        # toggle infection
        self.grid.set(self.current_row, self.current_col, not was_pre_burst_infected)

        # handle turn
        self._turn(was_pre_burst_infected)

        return not was_pre_burst_infected


    def _turn(self, was_pre_burst_infected):
        if \
            self.direction == 'up' and was_pre_burst_infected is True or \
            self.direction == 'down' and was_pre_burst_infected is False \
        :
            self.current_col += 1
            self.direction = 'right'

        elif \
            self.direction == 'up' and was_pre_burst_infected is False or \
            self.direction == 'down' and was_pre_burst_infected is True \
        :
            self.current_col -= 1
            self.direction = 'left'

        elif \
            self.direction == 'right' and was_pre_burst_infected is True or \
            self.direction == 'left' and was_pre_burst_infected is False \
        :
            self.current_row -= 1
            self.direction = 'down'

        else:
            assert( \
                self.direction == 'right' and was_pre_burst_infected is False or \
                self.direction == 'left' and was_pre_burst_infected is True \
            )
            self.current_row += 1
            self.direction = 'up'


    def _is_position_infected(self, row, col):
        return self.grid.get(row, col) is True


    def _is_current_position_infected(self):
        return self._is_position_infected(self.current_row, self.current_col) is True


    def print(self):
        print(self.grid.quads)



def get_infection_count(rows, r, c, q_bursts):
    g = InfectionGrid(rows, r, c)
    return sum(1 for _ in range(q_bursts) if g.burst())


def test():

    # test InfiniteGrid
    rows = ['123', '456', '789']
    g = InfiniteGrid(rows, 1, 1)

    # test quadrant spitting
    assert(g.quads == [[['2', '3']], [['1']], [['4'], ['7']], [['5', '6'], ['8', '9']]])

    # test quadrant and offset mapping
    assert(g.get(1, -1) == '1')
    assert(g.get(1, 0) == '2')
    assert(g.get(1, 1) == '3')
    assert(g.get(0, -1) == '4')
    assert(g.get(0, 0) == '5')
    assert(g.get(0, 1) == '6')
    assert(g.get(-1, -1) == '7')
    assert(g.get(-1, 0) == '8')
    assert(g.get(-1, 1) == '9')

    # test grid extension
    assert(g.get(0, 130) is False)
    assert(g.get(10, -130) is False)
    g.set(0, 130, 'k')
    assert(g.get(0, 130) == 'k')


    # test InfectionGrid
    rows = ['..#', '#..', '...']
    g = InfectionGrid(rows, 1, 1)

    # test infection test
    assert(g._is_position_infected(1, -1) is False)
    assert(g._is_position_infected(0, -1) is True)
    assert(g._is_position_infected(140, 200) is False)

    # test infection state change
    assert(g.current_row == 0)
    assert(g.current_col == 0)
    assert(g._is_position_infected(0, 0) is False)
    assert(g._is_current_position_infected() is False)
    assert(g.burst() is True)
    assert(g._is_position_infected(0, 0) is True)
    assert(g.current_row == 0)
    assert(g.current_col == -1)

    # test de-infection state change
    assert(g._is_position_infected(0, -1) is True)
    assert(g._is_current_position_infected() is True)
    assert(g.burst() is False)
    assert(g._is_position_infected(0, -1) is False)
    assert(g.current_row == 1)
    assert(g.current_col == -1)


    # integration test
    print(get_infection_count(rows, 1, 1, 70))
    assert(get_infection_count(rows, 1, 1, 70) == 41)
    assert(get_infection_count(rows, 1, 1, 10000) == 5587)


def main():
    test()

    with open('day22_input.txt') as f:
        rows = [r.strip() for r in f.readlines()]

    print(get_infection_count(rows, 13, 13, 10000))


main()
