#!/usr/bin/python3.5



class InfiniteGrid(object):

    def __init__(self, rows, c, r):
        self._initialise_quadrants(rows, c, r)


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

    states = ['.', 'W', '#', 'F']
    q_states = 4


    def __init__(self, rows, center_row, center_col):

        rows = [[self._encode_state(item) for item in row] for row in rows]
        self.grid = InfiniteGrid(rows, center_row, center_col)

        self.current_row = 0
        self.current_col = 0
        self.direction = 'up'

        self.infection_count = 0


    @classmethod
    def _encode_state(cls, state):
        return cls.states.index(state)


    @classmethod
    def _decode_state(cls, code):
        return cls.states[code]


    def burst(self):
        # record how was position before this burst
        pre_burst_state_code = self.grid.get(self.current_row, self.current_col)
        pre_burst_state = self._decode_state(pre_burst_state_code)

        # cycle state code
        post_burst_state_code = (pre_burst_state_code + 1) % self.q_states
        self.grid.set(self.current_row, self.current_col, post_burst_state_code)

        # check if we have just 
        post_burst_state= self._decode_state(post_burst_state_code)
        if post_burst_state == '#':
            self.infection_count += 1

        # handle turn
        self._turn(pre_burst_state)


    def _turn(self, state):
        
        if self.direction == 'up':
            if state == '#':
                self.direction = 'right'
                self.current_col += 1
            elif state == 'F':
                self.direction = 'down'
                self.current_row -= 1
            elif state == '.':
                self.direction = 'left'
                self.current_col -= 1
            elif state == 'W':
                # keep on heading upwards
                self.current_row += 1

        elif self.direction == 'down':
            if state == '#':
                self.direction = 'left'
                self.current_col -= 1
            elif state == 'F':
                self.direction = 'up'
                self.current_row += 1
            elif state == '.':
                self.direction = 'right'
                self.current_col += 1
            elif state == 'W':
                # keep on heading downwards
                self.current_row -= 1

        elif self.direction == 'right':
            if state == '#':
                self.current_row -= 1
                self.direction = 'down'
            elif state == 'F':
                self.current_col -= 1
                self.direction = 'left'
            elif state == '.':
                self.current_row += 1
                self.direction = 'up'
            elif state == 'W':
                # keep on righteous
                self.current_col += 1

        elif self.direction == 'left':
            if state == '#':
                self.current_row += 1
                self.direction = 'up'
            elif state == 'F':
                self.current_col += 1
                self.direction = 'right'
            elif state == '.':
                self.current_row -= 1
                self.direction = 'down'
            elif state == 'W':
                # keep on lefty
                self.current_col -= 1


    def _get_current_position_status(self):
        return self._decode_state(self.current_row, self.current_col)


    def print(self, qs=10):
        print('\n ' + '-' * (qs * 6))
        for row in range(qs, -qs, -1):
            print('|', end='')
            for col in range(-qs, qs):
                cell = self.states[self.grid.get(row, col)]
                if self.current_row == row and self.current_col == col:
                    print('[{}]'.format(cell), end='')
                else:
                    print(' {} '.format(cell), end='')
            
            print('|')
        print(' ' + '-' * (qs * 6))


def test():

    # test InfectionGrid
    rows = ['..#', '#..', '...']
    g = InfectionGrid(rows, 1, 1)

    # integration test
    def get_infection_count(rows, r, c, q_bursts):
        g = InfectionGrid(rows, r, c)

        for _ in range(q_bursts):
            g.burst()

        return g.infection_count

    assert(get_infection_count(rows, 1, 1, 100) == 26)
    assert(get_infection_count(rows, 1, 1, 10000000) == 2511944)


def main():
    test()

    with open('day22_input.txt') as f:
        rows = [r.strip() for r in f.readlines()]

    g = InfectionGrid(rows, 12, 12)
    g.print(15)

    for i in range(10000000):
        g.burst()

    print(g.infection_count)


main()
