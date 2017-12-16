

def get_captcha(s):
    length = len(s)
    return sum(int(s[i]) for i in range(length) if s[i] == s[(i+1) % length])

def read_file(filename):
    with open(filename) as f:
        return f.read().strip()

def test():
    assert(get_captcha('1122') == 3)
    assert(get_captcha('1111') == 4)
    assert(get_captcha('91212129') == 9)

if __name__ == '__main__':
    test()
    sequence = read_file('day1_input.txt')
    print(get_captcha(sequence))

