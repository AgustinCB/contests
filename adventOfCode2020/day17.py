import sys
from typing import Tuple, Set, Union, Callable

Point = Tuple[int, int, int]
Point4d = Tuple[int, int, int, int]


def neighbors_4d(point: Point4d) -> Set[Point4d]:
    point_3d = (point[0], point[1], point[2])
    layer_template = neighbors(point_3d).union({point_3d})
    result = set()
    for w_offset in [-1, 0, 1]:
        for p in layer_template:
            result.add((p[0], p[1], p[2], point[3] + w_offset))
    return result - {point}


def neighbors(point: Point) -> Set[Point]:
    return {
        (point[0] - 1, point[1], point[2]),
        (point[0] + 1, point[1], point[2]),
        (point[0], point[1] - 1, point[2]),
        (point[0], point[1] + 1, point[2]),
        (point[0] - 1, point[1] + 1, point[2]),
        (point[0] + 1, point[1] + 1, point[2]),
        (point[0] - 1, point[1] - 1, point[2]),
        (point[0] + 1, point[1] - 1, point[2]),
        (point[0], point[1], point[2] + 1),
        (point[0] - 1, point[1], point[2] + 1),
        (point[0] + 1, point[1], point[2] + 1),
        (point[0], point[1] - 1, point[2] + 1),
        (point[0], point[1] + 1, point[2] + 1),
        (point[0] - 1, point[1] + 1, point[2] + 1),
        (point[0] + 1, point[1] + 1, point[2] + 1),
        (point[0] - 1, point[1] - 1, point[2] + 1),
        (point[0] + 1, point[1] - 1, point[2] + 1),
        (point[0], point[1], point[2] - 1),
        (point[0] - 1, point[1], point[2] - 1),
        (point[0] + 1, point[1], point[2] - 1),
        (point[0], point[1] - 1, point[2] - 1),
        (point[0], point[1] + 1, point[2] - 1),
        (point[0] - 1, point[1] + 1, point[2] - 1),
        (point[0] + 1, point[1] + 1, point[2] - 1),
        (point[0] - 1, point[1] - 1, point[2] - 1),
        (point[0] + 1, point[1] - 1, point[2] - 1),
    }


def simulate(
        occupied_spaces: Set[Union[Point, Point4d]],
        iterations: int,
        ns: Callable[[Union[Point, Point4d]], Set[Union[Point, Point4d]]]
) -> Set[Point]:
    current_iteration = 0
    current_occupied_spaces = occupied_spaces
    while current_iteration < iterations:
        visited = set()
        new_occupied_spaces = current_occupied_spaces.copy()
        for point in current_occupied_spaces:
            point_neighbors = ns(point)
            if len(current_occupied_spaces.intersection(point_neighbors)) not in [2, 3]:
                new_occupied_spaces.remove(point)
            for neighbor in point_neighbors - current_occupied_spaces - visited:
                neighbor_neighbors = ns(neighbor)
                if len(neighbor_neighbors.intersection(current_occupied_spaces)) == 3:
                    new_occupied_spaces.add(neighbor)
            visited = visited.union(point_neighbors).union({point})
        current_occupied_spaces = new_occupied_spaces
        current_iteration += 1
    return current_occupied_spaces


def solve():
    initial_map = [list(line.strip()) for line in sys.stdin]
    occupied_spaces = set()
    for (r, row) in enumerate(initial_map):
        for (c, cell) in enumerate(row):
            if cell == "#":
                occupied_spaces.add((c, r, 1))

    if sys.argv[1] == 'part1':
        return len(simulate(occupied_spaces, 6, neighbors))
    if sys.argv[1] == 'part2':
        occupied_spaces = {(p[0], p[1], p[2], 1) for p in occupied_spaces}
        return len(simulate(occupied_spaces, 6, neighbors_4d))


if __name__ == '__main__':
    print(solve())
