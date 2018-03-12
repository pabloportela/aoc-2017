#!/usr/bin/python3.5



class Item(object):

    def __init__(self, value):
        self.value = value
        self.next = None

    def step(self, i):
        current = self
        for _ in range(i):
            current = current.next
        
        return current

    def print_list(self):
        current = self
        while True:
            print('{} '.format(current.value), end='')
            current = current.next
            if current is self:
                break

        print('')


def get_value_after_2017(q_steps):

    current = Item(0)
    # original = current
    current.next = current

    for i in range(1, 2018):
        new = Item(i)
        aux = current.next
        current.next = new
        new.next = aux
        current = new.step(q_steps)
        # original.print_list()

    return new.next.value



def main():
    assert(get_value_after_2017(3) == 638)
    print(get_value_after_2017(328))



main()
