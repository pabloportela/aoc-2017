


def count_valid_phrases(phrases):
    return sum(int(is_phrase_valid(p)) for p in phrases)

def is_phrase_valid(words):
    return len(words) == len(set(words))

def test():
    assert(is_phrase_valid('aa bb cc dd ee'.split(' ')) is True)
    assert(is_phrase_valid('aa bb cc dd aa'.split(' ')) is False)
    assert(is_phrase_valid('aa bb cc dd aaa'.split(' ')) is True)


if __name__ == '__main__':
    test()

    with open('day4_input.txt') as f:
        lines = f.readlines()

    phrases = [[w for w in line.strip().split(' ')] for line in lines]
    print(phrases)

    print(count_valid_phrases(phrases))

