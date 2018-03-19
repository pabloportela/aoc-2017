#!/usr/bin/python3.5


def print_q_prevailing_particles(particles):
    # from now on, 't' referst to time, without overriding standard libraries
    t = 0

    # as a first approach, let's try reaching long term by running forever
    while True:
        remove_colliding_particles(particles, t)
        print(len(particles))
        t += 1


def remove_colliding_particles(particles, t):
    ''' calculate all particle positions for the time being, remove duplicates in-place '''

    # calculate positions for the current time
    particle_positions = [get_particle_position(p, t) for p in particles]

    # find dupes
    collisions = set(x for x in particle_positions if particle_positions.count(x) > 1)
    if collisions:

        # see to which indices they belong to in our main, side-effect-bound array of particles
        collision_indices = [i for i, p in enumerate(particle_positions) if p in collisions]

        # filter those out
        particles[:] = [p for i, p in enumerate(particles) if i not in collision_indices]


def get_displacement(v, a, t):
    ''' get linear displacement from origin, big thanks to the greeks '''
    return t * v + a * t * (t + 1) / 2


def get_particle_position(particle, t):
    ''' return original position plus displacement for the time being, in an (x,y,x) tuple '''
    position, velocity, acceleration = particle
    return tuple(get_displacement(velocity[i], acceleration[i], t) + position[i] for i in range(3))


def parse_particle_line(line):
    p, v, a = [x.strip()[x.index('<') + 1: -1] for x in line.split(', ')]
    parse = lambda x: tuple(map(int, x.split(',')))

    return parse(p), parse(v), parse(a)


def main():

    with open('day20_input.txt') as f:
        particles = [parse_particle_line(l) for l in f.readlines()]

    print_q_prevailing_particles(particles)


main()
