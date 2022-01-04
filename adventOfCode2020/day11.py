import sys
from typing import Tuple, Set, List, Optional

DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]


def neighbors(position: Tuple[int, int], height: int, width: int) -> Set[Tuple[int, int]]:
    return set([
        d
        for d in [(position[0] + d[0], position[1] + d[1]) for d in DIRECTIONS]
        if 0 <= d[0] < width and 0 <= d[1] < height
    ])


def print_map(seating_map: List[List[str]]):
    for row in seating_map:
        print(' '.join(row))
    print()


def look_in_direction(position: Tuple[int, int], direction: Tuple[int, int], seating_map: List[List[str]]) -> Optional[str]:
    current_position = (position[0] + direction[0], position[1] + direction[1])
    while 0 <= current_position[0] < len(seating_map[0]) and 0 <= current_position[1] < len(seating_map):
        if seating_map[current_position[1]][current_position[0]] != '.':
            return seating_map[current_position[1]][current_position[0]]
        current_position = (current_position[0] + direction[0], current_position[1] + direction[1])
    return None


def complex_simulation(seating_map: List[List[str]]):
    finished = False

    while not finished:
        to_swap = set()
        for (r, row) in enumerate(seating_map):
            for (c, seat) in enumerate(row):
                if seat != '.':
                    neighbors_by_direction = [look_in_direction((c, r), d, seating_map) for d in DIRECTIONS]
                    occupied_neighbors = len([1 for ns in neighbors_by_direction if ns == '#'])
                    if (seat == 'L' and occupied_neighbors == 0) or (seat == '#' and occupied_neighbors >= 5):
                        to_swap.add((c, r))
        for (c, r) in to_swap:
            if seating_map[r][c] == '#':
                seating_map[r][c] = 'L'
            elif seating_map[r][c] == 'L':
                seating_map[r][c] = '#'
        finished = len(to_swap) == 0


def simple_simulation(seating_map: List[List[str]]):
    finished = False

    while not finished:
        to_swap = set()
        for (r, row) in enumerate(seating_map):
            for (c, seat) in enumerate(row):
                if seat != '.':
                    seat_neighbors = neighbors((c, r), len(seating_map), len(row))
                    occupied_neighbors = len([1 for (c, r) in seat_neighbors if seating_map[r][c] == '#'])
                    if (seat == 'L' and occupied_neighbors == 0) or (seat == '#' and occupied_neighbors >= 4):
                        to_swap.add((c, r))
        for (c, r) in to_swap:
            if seating_map[r][c] == '#':
                seating_map[r][c] = 'L'
            elif seating_map[r][c] == 'L':
                seating_map[r][c] = '#'
        finished = len(to_swap) == 0


def solve():
    seating_map = [list(line.strip()) for line in sys.stdin]

    if sys.argv[1] == 'part1':
        simple_simulation(seating_map)
        return sum(len([s for s in row if s == '#']) for row in seating_map)
    if sys.argv[1] == 'part2':
        complex_simulation(seating_map)
        return sum(len([s for s in row if s == '#']) for row in seating_map)


if __name__ == '__main__':
    print(solve())
