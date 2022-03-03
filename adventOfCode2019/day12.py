import itertools
import numpy as np
import sys
from typing import Tuple, List

Position = Tuple[int, int, int]
Velocity = Tuple[int, int, int]


def parse_line(line: str) -> Position:
    x, y, z = line[1:-1].split(", ")
    return int(x.replace("x=", "")), int(y.replace("y=", "")), int(z.replace("z=", ""))


def parse_positions() -> List[Position]:
    return [parse_line(line.strip()) for line in sys.stdin]


def find_zero_for(initial_positions: List[Position], index: int) -> int:
    positions = initial_positions[:]
    velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    w = 0
    while True:
        velocity_deltas = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for (i, j) in list(itertools.permutations(range(4), 2)):
            if positions[i][0] < positions[j][0]:
                velocity_deltas[i][0] += 1
            elif positions[i][0] > positions[j][0]:
                velocity_deltas[i][0] -= 1
            if positions[i][1] < positions[j][1]:
                velocity_deltas[i][1] += 1
            elif positions[i][1] > positions[j][1]:
                velocity_deltas[i][1] -= 1
            if positions[i][2] < positions[j][2]:
                velocity_deltas[i][2] += 1
            elif positions[i][2] > positions[j][2]:
                velocity_deltas[i][2] -= 1

        velocities = [
            [v[0] + vd[0], v[1] + vd[1], v[2] + vd[2]]
            for (v, vd) in zip(velocities, velocity_deltas)
        ]
        positions = [
            [p[0] + v[0], p[1] + v[1], p[2] + v[2]]
            for (p, v) in zip(positions, velocities)
        ]
        w += 1
        if all(velocity[index] == 0 for velocity in velocities):
            return w


def solve():
    initial_positions = parse_positions()
    if sys.argv[1] == 'part1':
        positions = initial_positions[:]
        velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for w in range(1000):
            velocity_deltas = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

            for (i, j) in list(itertools.permutations(range(4), 2)):
                if positions[i][0] < positions[j][0]:
                    velocity_deltas[i][0] += 1
                elif positions[i][0] > positions[j][0]:
                    velocity_deltas[i][0] -= 1
                if positions[i][1] < positions[j][1]:
                    velocity_deltas[i][1] += 1
                elif positions[i][1] > positions[j][1]:
                    velocity_deltas[i][1] -= 1
                if positions[i][2] < positions[j][2]:
                    velocity_deltas[i][2] += 1
                elif positions[i][2] > positions[j][2]:
                    velocity_deltas[i][2] -= 1

            velocities = [
                [v[0] + vd[0], v[1] + vd[1], v[2] + vd[2]]
                for (v, vd) in zip(velocities, velocity_deltas)
            ]
            positions = [
                [p[0] + v[0], p[1] + v[1], p[2] + v[2]]
                for (p, v) in zip(positions, velocities)
            ]
        return sum([
            sum([abs(i) for i in p]) * sum([abs(i) for i in v]) for (p, v) in zip(positions, velocities)
        ])
    if sys.argv[1] == 'part2':
        first_zero_for_x = find_zero_for(initial_positions, 0)
        first_zero_for_y = find_zero_for(initial_positions, 1)
        first_zero_for_z = find_zero_for(initial_positions, 2)
        lcm = np.lcm(np.lcm(first_zero_for_x, first_zero_for_y), first_zero_for_z)
        return lcm * 2


if __name__ == '__main__':
    print(solve())
