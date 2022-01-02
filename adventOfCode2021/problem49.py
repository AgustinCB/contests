import bisect
import sys
from typing import List, Tuple


def move_left(positions: List[Tuple[int, int, str]], width: int) -> (int, List[Tuple[int, int, str]]):
    unique_positions = set([(x, y) for (x, y, _) in positions])
    final_positions = []
    moves = 0
    for (x, y, c) in positions:
        new_x = (x + 1) % width
        if c == '>' and (new_x, y) not in unique_positions:
            bisect.insort(final_positions, (new_x, y, c))
            moves += 1
        else:
            bisect.insort(final_positions, (x, y, c))
    return moves, final_positions


def move_down(positions: List[Tuple[int, int, str]], height: int) -> (int, List[Tuple[int, int, str]]):
    unique_positions = set([(x, y) for (x, y, _) in positions])
    final_positions = []
    moves = 0
    for (x, y, c) in positions:
        new_y = (y + 1) % height
        if c == 'v' and (x, new_y) not in unique_positions:
            bisect.insort(final_positions, (x, new_y, c))
            moves += 1
        else:
            bisect.insort(final_positions, (x, y, c))
    return moves, final_positions


def solve():
    height = 0
    width = None
    initial_positions = []
    for line in sys.stdin:
        if width is None:
            width = len(line.strip())
        for (current_x, c) in enumerate(line.strip()):
            if c == '>' or c == 'v':
                bisect.insort(initial_positions, (current_x, height, c))
        height += 1
    print(initial_positions)
    finished = False
    counter = 0
    positions = initial_positions[:]
    while not finished:
        (left_moves, positions) = move_left(positions, width)
        (down_moves, positions) = move_down(positions, height)
        finished = (left_moves + down_moves) == 0
        counter += 1
    return counter


if __name__ == '__main__':
    print(solve())
