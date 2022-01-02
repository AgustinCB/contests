import sys
from collections import Counter
from typing import Tuple, List


def check_trees_for_slow(tree_map: List[str], slope: Tuple[int, int]) -> int:
    current_column = slope[1]
    trees = 0
    for row_index in range(slope[0], len(tree_map), slope[0]):
        row = tree_map[row_index]
        trees += int(row[current_column] == '#')
        current_column = (current_column + slope[1]) % len(row)
    return trees


def solve():
    tree_map = []
    for line in sys.stdin:
        tree_map.append(line.strip())

    if sys.argv[1] == 'part1':
        return check_trees_for_slow(tree_map, (1, 3))
    if sys.argv[1] == 'part2':
        return check_trees_for_slow(tree_map, (1, 3)) * \
               check_trees_for_slow(tree_map, (1, 1)) * \
               check_trees_for_slow(tree_map, (1, 5)) * \
               check_trees_for_slow(tree_map, (1, 7)) * \
               check_trees_for_slow(tree_map, (2, 1))


if __name__ == '__main__':
    print(solve())
