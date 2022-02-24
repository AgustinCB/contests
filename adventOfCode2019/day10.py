import math
import sys
from itertools import permutations
from typing import Tuple, Set, List

Position = Tuple[int, int]


def parse_map() -> [List[Position], int, int]:
    positions = []
    height = 0
    width = 0
    for (i, line) in enumerate(sys.stdin):
        width = len(line)
        for (j, c) in enumerate(line):
            if c == '#':
                positions.append((j, i))
        height += 1
    positions.sort()
    return positions, width, height


def get_all_angles(x: int, y: int, width: int, height: int) -> List[Position]:
    directions = []
    angles = []

    if x < width-1 and y < height-1:
        directions.append((1, 1))
        angles.append((1, 1))
    if x > 0 and y > 0:
        directions.append((-1, -1))
        angles.append((-1, -1))
    if x > 0 and y < height - 1:
        directions.append((-1, 1))
        angles.append((-1, 1))
    if y > 0 and x < width - 1:
        directions.append((1, -1))
        angles.append((1, -1))

    if 0 < x < width - 1:
        angles.append((1, 0))
        angles.append((-1, 0))
    elif x == 0:
        angles.append((1, 0))
    else:
        angles.append((-1, 0))

    if 0 < y < width - 1:
        angles.append((0, 1))
        angles.append((0, -1))
    elif y == 0:
        angles.append((0, 1))
    else:
        angles.append((0, -1))

    for angle in permutations(range(1, width), 2):
        for direction in directions:
            angles.append((angle[0] * direction[0], angle[1] * direction[1]))

    return angles


def get_all_asteroids_in_line(
        already_seen: Set[Position],
        asteroid_map: Set[Position],
        position: Position,
        x_increment: int,
        y_increment: int,
        width: int,
        height: int,
) -> Set[Position]:
    current_x = position[0]
    current_y = position[1]
    positions_in_line = set()
    while width > current_x >= 0 and height > current_y >= 0:
        position = (current_x, current_y)
        if position in asteroid_map and position not in already_seen:
            positions_in_line.add((current_x, current_y))
        current_x += x_increment
        current_y += y_increment
    return positions_in_line


def find_optimal_position(asteroid_map: List[Position], width: int, height: int, asteroid_map_set: Set[Position]) -> Tuple[Position, int]:
    max_detected = None
    max_position = None
    for asteroid in asteroid_map:
        covered = {asteroid}
        detected = 0
        angles = get_all_angles(asteroid[0], asteroid[1], width, height)

        for (x_step, y_step) in angles:
            new_covered = get_all_asteroids_in_line(
                covered, asteroid_map_set, asteroid, x_step, y_step, width, height
            )
            if len(new_covered) > 0:
                detected += 1
            covered = covered.union(new_covered)

        if max_detected is None or detected > max_detected:
            max_position = asteroid
            max_detected = detected
    return max_position, max_detected


def solve():
    asteroid_map, width, height = parse_map()
    asteroid_map_set = set(asteroid_map)
    if sys.argv[1] == 'part1':
        return find_optimal_position(asteroid_map, width, height, asteroid_map_set)
    if sys.argv[1] == 'part2':
        asteroid, _ = find_optimal_position(asteroid_map, width, height, asteroid_map_set)
        asteroids_per_line = {}
        covered = {asteroid}
        angles = get_all_angles(asteroid[0], asteroid[1], width, height)

        for (x_step, y_step) in angles:
            new_covered = get_all_asteroids_in_line(
                covered, asteroid_map_set, asteroid, x_step, y_step, width, height
            )
            if len(new_covered) > 0:
                asteroids_per_line[(x_step, y_step)] = sorted(new_covered, key=lambda p: abs(p[0] - asteroid[0]) + abs(p[1] - asteroid[1]), reverse=True)
            covered = covered.union(new_covered)
        angles = [(((math.atan2(-k[0], k[1]) + math.pi) * (180 / math.pi)) % 360, k) for k in asteroids_per_line.keys()]
        angles.sort()
        last_pos = None
        i = 0
        for c in range(200):
            while len(asteroids_per_line[angles[i][1]]) == 0:
                i = (i + 1) % len(angles)
            last_pos = asteroids_per_line[angles[i][1]].pop()
            i = (i + 1) % len(angles)
        return last_pos, last_pos[0] * 100 + last_pos[1]


if __name__ == '__main__':
    print(solve())
