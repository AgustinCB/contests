import sys
from typing import Tuple, List, Set, Dict

Point = Tuple[int, int]


def manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def walk(steps: List[str]) -> Set[Point]:
    points = set()
    current_step = (0, 0)
    for step in steps:
        instruction = step[0]
        argument = int(step[1:])
        for _ in range(argument):
            if instruction == 'R':
                current_step = (current_step[0] + 1, current_step[1])
            elif instruction == 'L':
                current_step = (current_step[0] - 1, current_step[1])
            elif instruction == 'U':
                current_step = (current_step[0], current_step[1] + 1)
            elif instruction == 'D':
                current_step = (current_step[0], current_step[1] - 1)
            points.add(current_step)
    return points


def walk_counting_steps(steps: List[str]) -> Dict[Point, int]:
    points = {}
    current_step = (0, 0)
    count = 0
    for step in steps:
        instruction = step[0]
        argument = int(step[1:])
        for _ in range(argument):
            if instruction == 'R':
                current_step = (current_step[0] + 1, current_step[1])
            elif instruction == 'L':
                current_step = (current_step[0] - 1, current_step[1])
            elif instruction == 'U':
                current_step = (current_step[0], current_step[1] + 1)
            elif instruction == 'D':
                current_step = (current_step[0], current_step[1] - 1)
            count += 1
            points[current_step] = count
    return points


def solve():
    first_steps = sys.stdin.readline().strip().split(",")
    second_steps = sys.stdin.readline().strip().split(",")
    if sys.argv[1] == 'part1':
        first_points = walk(first_steps)
        second_points = walk(second_steps)
        intersections = first_points.intersection(second_points)
        return min([manhattan_distance((0, 0), i) for i in intersections])
    if sys.argv[1] == 'part2':
        first_points = walk_counting_steps(first_steps)
        second_points = walk_counting_steps(second_steps)
        min_total = None
        for (p, count) in first_points.items():
            if p in second_points:
                steps = count + second_points[p]
                if min_total is None or steps < min_total:
                    min_total = steps
        return min_total


if __name__ == '__main__':
    print(solve())
