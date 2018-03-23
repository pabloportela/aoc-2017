#!/usr/bin/python3.5


import pdb


class EnhancementRules(object):

    def __init__(self, raw_rules):
        self.rules_2x2 = self._parse_rules(raw_rules, 20, 16)
        self.rules_3x3 = self._parse_rules(raw_rules, 34, 512)


    @classmethod
    def _parse_rules(cls, raw_rules, line_len, q_rules):
        '''
        parse enhancement rules <raw_rules> on lines <line_len> long for a square with side <line_len>
        precalculate all equivalent flips and rotations in a flat array with the input bits as indexes
        '''

        rules = [None] * q_rules
        base_raw_rules = (tuple(r.split(' => ')) for r in raw_rules if len(r) == line_len)

        for r in base_raw_rules:
            input_pattern = tuple(map(tuple, r[0].split('/')))
            output_pattern = tuple(r[1].split('/'))
            output_rows = cls.pattern_to_image_rows(output_pattern)

            for p in cls._get_equivalent_patterns(input_pattern):
                index = cls._index(cls.pattern_to_image_rows(p))
                rules[index] = output_rows

        return rules


    def match(self, square_rows):
        p_length = len(square_rows)
        index = self._index(square_rows)
        if p_length == 2:
            rules = self.rules_2x2
        else:
            assert(p_length == 3)
            rules = self.rules_3x3

        return rules[index]


    @staticmethod
    def pattern_to_image_rows(pattern):
        return tuple(tuple(1 if c == '#' else 0 for c in row) for row in pattern)


    @staticmethod
    def _index(square_rows):
        flattened = tuple(i for row in square_rows for i in row)
        return sum(v * 2 ** i for i, v in enumerate(flattened[::-1]))


    @classmethod
    def _get_equivalent_patterns(cls, pattern):
        ''' returns all eight combinations from flipping and rotating the pattern array '''

        # original pattern
        patterns = [pattern]

        # rotate three times
        for _ in range(3):
            pattern = tuple(zip(*reversed(pattern)))
            patterns.append(pattern)

        # flip it
        pattern = tuple(reversed(pattern))
        patterns.append(pattern)
        # rotate flipped three times
        for _ in range(3):
            pattern = tuple(zip(*reversed(pattern)))
            patterns.append(pattern)

        return patterns


class Image(object):

    def __init__(self, image_rows, enhancement_rules):
        self.image_rows = image_rows
        self.enhancement_rules = enhancement_rules


    @property
    def side(self):
        return len(self.image_rows)


    @property
    def sub_square_side(self):
        if self.side % 2 == 0:
            return 2
        else:
            assert(self.side % 3 == 0)
            return 3


    @property
    def sub_squares_per_side(self):
        return int(self.side / self.sub_square_side)


    def enhance(self):
        ''' maps each sub-square and puts up a new image '''

        sub_squares_per_side = self.sub_squares_per_side
        current_side = self.side
        current_sub_side = self.sub_square_side

        new_sub_side = current_sub_side + 1
        new_side = new_sub_side * sub_squares_per_side

        linear_image = [None] * (new_side ** 2)

        # iterate through each current sub square
        for i in range(sub_squares_per_side ** 2):
            # map square from current image
            current_r = ((i * current_sub_side) // current_side) * current_sub_side
            current_c = (i * current_sub_side) % current_side
            input_square = self._get_sub_square(current_r, current_c, current_sub_side) 
            output_square = self._match(input_square)

            # patch it towards the enhanced one
            new_r = ((i * new_sub_side) // new_side) * new_sub_side
            new_c = (i * new_sub_side) % new_side
            self._linear_patch(linear_image, new_side, new_sub_side, new_r, new_c, output_square)

        # pdb.set_trace()
        # transform from linear to matrix and replace
        self.image_rows = tuple(tuple(linear_image[i * new_side: i * new_side + new_side]) for i in range(new_side))


    @staticmethod
    def _linear_patch(linear_image, side, sub_side, r, c, patch_rows):
        for i, row in enumerate(patch_rows):
            start = (r+i) * side + c
            linear_image[start: start + sub_side] = row


    def _match(self, square_rows):
        return self.enhancement_rules.match(square_rows)


    def _get_sub_square(self, r, c, side):
        return tuple(self.image_rows[i][c:c + side] for i in range(r, r + side))


    def get_active_pixel_count(self):
        return sum(sum(r) for r in self.image_rows)


    def print(self):
        for r in self.image_rows:
            print(''.join(map(str, r)).replace('1','#').replace('0','.'))


def main():
    with open('day21_input.txt') as f:
        rule_lines = [l.strip() for l in f.readlines()]

    # parse and encode rules
    enhancement_rules = EnhancementRules(rule_lines)

    # encode image pixels
    image_rows = EnhancementRules.pattern_to_image_rows(['.#.', '..#', '###'])

    # initialise image, with enhancement ruleset, strategy pattern
    image = Image(image_rows, enhancement_rules)

    for _ in range(18):
        image.enhance()
        print(image.get_active_pixel_count())


main()
