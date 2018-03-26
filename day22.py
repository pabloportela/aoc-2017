#!/usr/bin/python3.5



class InfiniteGrid(object):

    def __init__(self, rows, c, r):
        self._initialise_quadrants(rows, c, r)

        #'123aq',
        #'456bw',
        #'789ct',
        #'defgy',
        #'hijku',

    def _initialise_quadrants(self, rows, c, r):
        self.quads = [
            # quad 1, x >= 0 , y > 0
            list(reversed([list(row[c:]) for row in rows[:r]])),

            # quad 2, x < 0 , y > 0
            list(reversed([list(reversed(row[:c])) for row in rows[:r]])),

            # quad 3, x < 0 , y <= 0
            list([list(reversed(row[:c])) for row in rows[r:]]),

            # quad 4, x >= 0 , y <= 0
            list(list(row[c:]) for row in rows[r:]),
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

        self.infection_count = 0

    def burst(self):
        # record how was position before this burst
        was_pre_burst_infected = self._is_current_position_infected()

        if not was_pre_burst_infected:
            self.infection_count += 1

        # toggle infection
        self.grid.set(self.current_row, self.current_col, not was_pre_burst_infected)

        # handle turn
        self._turn(was_pre_burst_infected)

        return not was_pre_burst_infected


    def _turn(self, was_pre_burst_infected):
        if self.direction == 'up':
            if was_pre_burst_infected:
                self.direction = 'right'
                self.current_col += 1
            else:
                self.direction = 'left'
                self.current_col -= 1

        elif self.direction == 'down':
            if was_pre_burst_infected:
                self.direction = 'left'
                self.current_col -= 1
            else:
                self.direction = 'right'
                self.current_col += 1

        elif self.direction == 'right':
            if was_pre_burst_infected:
                self.current_row -= 1
                self.direction = 'down'
            else:
                self.current_row += 1
                self.direction = 'up'

        elif self.direction == 'left':
            if was_pre_burst_infected:
                self.current_row += 1
                self.direction = 'up'
            else:
                self.current_row -= 1
                self.direction = 'down'


    def _is_position_infected(self, row, col):
        return self.grid.get(row, col) is True


    def _is_current_position_infected(self):
        return self._is_position_infected(self.current_row, self.current_col) is True


    def _was_current_position_initially_infected(self):
        return self.initial_grid.get(self.current_row, self.current_col) is True


    def print(self, qs=10):
        for col in range(-qs, qs):
            print('{}'.format(col), end='')
        print('\n ' + '-' * (qs * 6))
        for row in range(qs, -qs, -1):
            for col in range(-qs, qs):
                cell = '#' if self.grid.get(row, col) else '.'
                if self.current_row == row and self.current_col == col:
                    print('[{}]'.format(cell), end='')
                else:
                    print(' {} '.format(cell), end='')
            
            print('|', str(row))
        print(' ' + '-' * (qs * 6))



def get_infection_count(rows, r, c, q_bursts):
    g = InfectionGrid(rows, r, c)

    for _ in range(q_bursts):
        g.burst()

    return g.infection_count


def test():

    # test InfiniteGrid
    rows = [
        '123aq',
        '456bw',
        '789ct',
        'defgy',
        'hijku',
    ]
    g = InfiniteGrid(rows, 2, 2)

    # test quadrant spitting
    # print(g.quads)
    assert(g.quads == [
            [['6', 'b', 'w'], ['3', 'a', 'q']],
            [['5', '4'], ['2', '1']],
            [['8', '7'], ['e', 'd'], ['i', 'h']],
            [['9', 'c', 't'], ['f', 'g', 'y'], ['j', 'k', 'u']],
        ])

    # test quadrant and offset mapping
    assert(g.get(1, -1) == '5')
    assert(g.get(1, 0) == '6')
    assert(g.get(1, 1) == 'b')
    assert(g.get(0, -1) == '8')
    assert(g.get(0, 0) == '9')
    assert(g.get(0, 1) == 'c')
    assert(g.get(0, 2) == 't')
    assert(g.get(0, -2) == '7')
    assert(g.get(-1, -1) == 'e')
    assert(g.get(-1, 0) == 'f')
    assert(g.get(-1, 1) == 'g')
    assert(g.get(2, 2) == 'q')
    assert(g.get(2, -2) == '1')
    assert(g.get(2, 0) == '3')
    assert(g.get(-2, 0) == 'j')
    assert(g.get(-2, -2) == 'h')
    assert(g.get(-2, 2) == 'u')


    # test grid extension
    assert(g.get(-3, 2) is False)
    assert(g.get(0, 130) is False)
    assert(g.get(10, -130) is False)

    # test writting
    g.set(0, 130, 'k')
    assert(g.get(0, 130) == 'k')
    g.set(0, 130, 'r')
    assert(g.get(0, 130) == 'r')
    g.set(0, 0, '6')
    assert(g.get(0, 0) == '6')

    # test InfectionGrid
    rows = ['..#', '#..', '...']
    g = InfectionGrid(rows, 1, 1)
    # g.print()

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
    assert(get_infection_count(rows, 1, 1, 1) == 1)
    assert(get_infection_count(rows, 1, 1, 2) == 1)
    assert(get_infection_count(rows, 1, 1, 6) == 5)
    assert(get_infection_count(rows, 1, 1, 7) == 5)
    assert(get_infection_count(rows, 1, 1, 70) == 41)
    assert(get_infection_count(rows, 1, 1, 10000) == 5587)


def main():
    test()

    with open('day22_input.txt') as f:
        rows = [r.strip() for r in f.readlines()]
        # print(rows, len(rows))

    g = InfectionGrid(rows, 13, 13)
    g.current_row = 1
    g.current_col = -1
    g.print(20)
    for i in range(10000):
        g.burst()

    # g.print()
    print(g.infection_count)


main()
