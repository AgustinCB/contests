import sys
from typing import Iterable, List


def parse(input_stream: Iterable[str]) -> List[List[int]]:
    tree_map = []
    for s in input_stream:
        tree_map.append([int(c) for c in s.strip()])
    return tree_map


DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1)
]


def check_visibility(visibility: List[List[bool]], tree_map: List[List[int]], x: int, y: int) -> bool:
    value = tree_map[y][x]
    for direction in DIRECTIONS:
        curr_x = x + direction[0]
        curr_y = y + direction[1]
        is_visible = True
        while 0 <= curr_x < len(visibility[0]) and 0 <= curr_y < len(visibility):
            if tree_map[curr_y][curr_x] >= value:
                is_visible = False
                break
            curr_x += direction[0]
            curr_y += direction[1]
        if is_visible:
            return True
        return False


def get_scenic_score(tree_map: List[List[int]], x: int, y: int) -> int:
    value = tree_map[y][x]
    scenic_score = 1
    for direction in DIRECTIONS:
        curr_x = x + direction[0]
        curr_y = y + direction[1]
        scenic_view = 1
        while 0 < curr_x < len(tree_map[0]) - 1 and 0 < curr_y < len(tree_map) - 1:
            if tree_map[curr_y][curr_x] >= value:
                break
            curr_x += direction[0]
            curr_y += direction[1]
            scenic_view += 1
        print(scenic_view, direction, curr_x, curr_y, x, y)
        scenic_score *= scenic_view
    return scenic_score


def fill_visibility(visibility: List[List[bool]], tree_map: List[List[int]]):
    for y in range(1, len(tree_map) - 1):
        for x in range(1, len(tree_map[0]) - 1):
            visibility[y][x] = check_visibility(visibility, tree_map, x, y)
            print(x, y, visibility[y][x])
    print(len(visibility[0]), len(visibility))


def fill_scenic_scores(scenic_scores: List[List[int]], tree_map: List[List[int]]):
    for y in range(1, len(tree_map) - 1):
        for x in range(1, len(tree_map[0]) - 1):
            scenic_scores[y][x] = get_scenic_score(tree_map, x, y)
            print(x, y, scenic_scores[y][x], tree_map[y][x])
    print(len(scenic_scores[0]), len(scenic_scores))


def solve():
    tree_map = parse(sys.stdin)
    visibility = [
        [
            False if x != 0 and y != 0 and x != len(tree_map) - 1 and y != len(tree_map[0]) - 1 else True
            for y in range(len(tree_map[0]))
        ]
        for x in range(len(tree_map))
    ]
    if sys.argv[1] == 'part1':
        fill_visibility(visibility, tree_map)
        return sum(sum([int(v) for v in visibility_row]) for visibility_row in visibility)
    if sys.argv[1] == 'part2':
        scenic_scores = [
            [0 for _ in range(len(tree_map[0]))]
            for _ in range(len(tree_map))
        ]
        fill_scenic_scores(scenic_scores, tree_map)
        return max(max(scores) for scores in scenic_scores)


if __name__ == '__main__':
    print(solve())
