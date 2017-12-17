

def get_captcha(s):
    length = len(s)
    half = length / 2
    return sum(int(s[i]) for i in range(length) if s[i] == s[(i+half) % length])

def read_file(filename):
    with open(filename) as f:
        return f.read().strip()

def test():
    assert(get_captcha('1212') == 6)
    assert(get_captcha('1221') == 0)
    assert(get_captcha('123425') == 4)
    assert(get_captcha('123123') == 12)
    assert(get_captcha('12131415') == 4)

if __name__ == '__main__':
    test()
    sequence = read_file('day1_input.txt')
    print(get_captcha(sequence))

