from collections import defaultdict


class StreamProcessor(object):
    
    def __init__(self, stream):
        self.stream = stream
        self.score = 0
        self.group_level = 0
        self.garbage_char_count = 0
        self.process()

    def process(self):
        self.processor_callable = self.process_non_garbage
        for c in self.stream:
            self.processor_callable(c)

    def process_non_garbage(self, c):
        if c == '{':
            self.group_level += 1
            self.score += self.group_level

        elif c == '<':
            self.processor_callable = self.process_garbage

        elif c == '}':
            assert(self.group_level > 0)
            self.group_level -= 1

    def process_garbage(self, c):
        if c == '>':
            self.processor_callable = self.process_non_garbage

        elif c == '!':
            self.processor_callable = self.process_garbage_comment

        else:
            self.garbage_char_count += 1


    def process_garbage_comment(self, c):
        self.processor_callable = self.process_garbage


def get_score(stream):
    sp = StreamProcessor(stream)
    return sp.score


def get_garbage_char_count(stream):
    sp = StreamProcessor(stream)
    return sp.garbage_char_count


def test():
    assert(get_score('{}') == 1)
    assert(get_score('{{{}}}') == 6)
    assert(get_score('{{},{}}') == 5)
    assert(get_score('{{{},{},{{}}}}') == 16)
    assert(get_score('{<a>,<a>,<a>,<a>}') == 1)
    assert(get_score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9)
    assert(get_score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9)
    assert(get_score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3)

if __name__ == '__main__':
    test()

    with open('day9_input.txt') as f:
        stream = f.read().strip()

    print(get_score(stream))
    print(get_garbage_char_count(stream))
