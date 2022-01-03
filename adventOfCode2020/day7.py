import sys
from collections import defaultdict
from typing import Dict, Set


def count_outer_colors(color: str, bags: Dict[str, Dict[str, int]], visited: Set[str] = set()) -> Set[str]:
    outer_colors = set()
    for outer_color, contents in bags.items():
        if color in contents and outer_color not in visited:
            outer_colors.add(outer_color)
    for c in outer_colors:
        outer_colors = outer_colors.union(count_outer_colors(c, bags, visited.union(outer_colors)))
    return outer_colors


def count_inside_bags(color: str, bags: Dict[str, Dict[str, int]], out_bags: int = 1) -> int:
    inside_bags = 0
    for inside_color, number in bags[color].items():
        inside_bags += out_bags * (number + count_inside_bags(inside_color, bags, number))
    return inside_bags


def solve():
    bags = defaultdict(lambda: defaultdict(int))
    for line in sys.stdin:
        container, content = line.replace(".", "").strip().split(" bags contain ")
        if content != "no other bags":
            for contained_bags in content.strip().split(", "):
                contained_bags = contained_bags.replace(" bags", "").replace(" bag", "").split(" ")
                number = int(contained_bags[0])
                color = ' '.join(contained_bags[1:])
                bags[container][color] += number

    if sys.argv[1] == 'part1':
        return len(count_outer_colors("shiny gold", bags))
    if sys.argv[1] == 'part2':
        return count_inside_bags("shiny gold", bags)


if __name__ == '__main__':
    print(solve())
