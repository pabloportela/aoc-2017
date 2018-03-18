#!/usr/bin/python3.5


def get_long_term_closest(particles):
    # from now on, 't' referst to time without overriding standard libraries
    t = 0

    # as a first approach, let's try reaching long term by running forever
    while True:
        print(get_closest_particle_position(particles, t))
        t += 1


def get_closest_particle_position(particle_positions, t):
    particle_distances = ((i, get_manhattan_distance(p, t)) for i, p in enumerate(particle_positions))
    return min(particle_distances, key=lambda x: x[1])[0]


def get_manhattan_distance(particle, t):
    return sum(map(abs, get_particle_position(particle, t)))


def get_displacement(v, a, t):
    ''' plain formulae from physics '''
    return v * t + (1/2) * a * (t ** 2) if t else 0


def get_particle_position(particle, t):
    position, velocity, acceleration = particle
    return tuple(get_displacement(velocity[i], acceleration[i], t) + position[i] for i in range(3))


def parse_particle_line(line):
    part_p, part_v, part_a = [x.strip()[x.index('<') + 1: -1] for x in line.split(', ')]
    parse = lambda x: list(map(int, x.split(',')))

    position = parse(part_p)
    acceleration = parse(part_a)
    velocity = tuple(v + a for v, a in zip(parse(part_v), acceleration))

    return position, velocity, acceleration


def main():

    with open('day20_input.txt') as f:
        particles = [parse_particle_line(l) for l in f.readlines()]

    get_long_term_closest(particles)


main()

