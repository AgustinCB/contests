import sys
from typing import Tuple, Set, Optional

Range = Tuple[int, int]
Cuboid = Tuple[Range, Range, Range]


def ranges_intersect(range1: Range, range2: Range) -> bool:
    return range_contains(range1, range2) or range_contains(range2, range1) or \
           (range2[0] <= range1[0] <= range2[1]) or \
           (range1[0] <= range2[0] <= range1[1])


def range_contains(range1: Range, range2: Range) -> bool:
    return range1[0] <= range2[0] and range1[1] >= range2[1]


def range_intersection(range1: Range, range2: Range) -> Range:
    if range_contains(range1, range2):
        return range2
    if range_contains(range2, range1):
        return range1
    if range1[0] <= range2[0] <= range1[1]:
        return range2[0], range1[1]
    return range1[0], range2[1]


def cuboid_intersection(cuboid1: Cuboid, cuboid2: Cuboid) -> Cuboid:
    return (
        range_intersection(cuboid1[0], cuboid2[0]),
        range_intersection(cuboid1[1], cuboid2[1]),
        range_intersection(cuboid1[2], cuboid2[2]),
    )


def cuboids_intersect(cuboid1: Cuboid, cuboid2: Cuboid) -> bool:
    return all(ranges_intersect(r0, r1) for r0, r1 in zip(cuboid1, cuboid2))


def count_cubes_in_cuboid(cuboid: Cuboid) -> int:
    cubes = 1
    for from_pos, to_pos in cuboid:
        cubes *= (to_pos + 1) - from_pos
    return cubes


def parse_range(range_string: str) -> Range:
    range_parts = range_string.split("..")
    start = int(range_parts[0])
    end = int(range_parts[1])
    return start, end


def parse_cuboid_instruction(line: str) -> Optional[Tuple[Cuboid, bool]]:
    instruction, limits = line.split(" ")
    ranges = limits.replace("x=", "").replace("y=", "").replace("z=", "").split(",")
    range0 = parse_range(ranges[0])
    range1 = parse_range(ranges[1])
    range2 = parse_range(ranges[2])
    return (range0, range1, range2), True if instruction == "on" else False


def solve():
    instructions = []
    for line in sys.stdin:
        new_instruction = parse_cuboid_instruction(line.strip())
        new_instructions = []
        for (existing_cuboid, is_adding) in instructions:
            if cuboids_intersect(existing_cuboid, new_instruction[0]):
                new_instructions.append((cuboid_intersection(existing_cuboid, new_instruction[0]), not is_adding))
        instructions.extend(new_instructions)
        if new_instruction[1]:
            instructions.append(new_instruction)
    cubes = 0
    for (cuboid, is_adding) in instructions:
        if is_adding:
            cubes += count_cubes_in_cuboid(cuboid)
        else:
            cubes -= count_cubes_in_cuboid(cuboid)
    return cubes


if __name__ == '__main__':
    print(solve())
