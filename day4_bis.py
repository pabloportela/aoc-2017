


def count_valid_phrases(phrases):
    return sum(1 for p in phrases if not contains_anagrams(p))

def contains_anagrams(words):
    size = len(words)
    if size <= 1:
        return False

    for i in range(0, size - 1):
        for j in range(i+1, size):
            if is_anagram(words[i], words[j]):
                return True

    return False

def is_anagram(w1, w2):
    if len(w1) != len(w2):
        return False

    w2 = list(w2)

    for c in w1:
        try:
            w2.remove(c)
        except ValueError:
            return False
        
    return True


def test():
    assert(contains_anagrams('erwt trew'.split(' ')) is True)
    assert(contains_anagrams('erwt tre'.split(' ')) is False)
    assert(contains_anagrams('rwtt wtrw'.split(' ')) is False)
    assert(contains_anagrams('abcde fghij'.split(' ')) is False)
    assert(contains_anagrams('abcde xyz ecdab'.split(' ')) is True)
    assert(contains_anagrams('a ab abc abd abf abj'.split(' ')) is False)
    assert(contains_anagrams('iiii oiii ooii oooi oooo'.split(' ')) is False)
    assert(contains_anagrams('oiii ioii iioi iiio'.split(' ')) is True)


if __name__ == '__main__':
    test()

    with open('day4_input.txt') as f:
        lines = f.readlines()

    phrases = [[w for w in line.strip().split(' ')] for line in lines]

    print(count_valid_phrases(phrases))
