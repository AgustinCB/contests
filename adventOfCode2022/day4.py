import sys
from typing import Iterable, List, Tuple


Range = Tuple[int, int]


def range_contains_range(first: Range, second: Range) -> bool:
    return (
        first[0] <= second[0] and first[1] >= second[1]
    ) or (
        second[0] <= first[0] and second[1] >= first[1]
    )


def ranges_overlap(first: Range, second: Range) -> bool:
    return (range_contains_range(first, second) or
        (second[0] <= first[0] <= second[1]) or
        (first[0] <= second[0] <= first[1]) or
        (second[0] <= first[1] <= second[1]) or
        (first[0] <= second[1] <= first[1])
    )


def parse(input_stream: Iterable[str]) -> List[Tuple[Range, Range]]:
    ranges = []
    for s in input_stream:
        range_parts = s.strip().split(",")
        ranges.append((
            tuple([int(p) for p in range_parts[0].split("-")]),
                    tuple([int(p) for p in range_parts[1].split("-")])
        ))
    return ranges


def solve():
    if sys.argv[1] == 'part1':
        ranges = parse(sys.stdin)
        return sum(int(range_contains_range(range1, range2)) for (range1, range2) in ranges)
    if sys.argv[1] == 'part2':
        ranges = parse(sys.stdin)
        return sum(int(ranges_overlap(range1, range2)) for (range1, range2) in ranges)


if __name__ == '__main__':
    print(solve())
