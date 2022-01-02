import sys
from typing import Set


directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]


def get_adjacents(i, j) -> [(int, int)]:
    return [
        (i + dx, j + dy)
        for (dx, dy) in directions
        if 0 <= (i + dx) < 10 and 0 <= (j + dy) < 10
    ]


def flash(i, j, map: [[int]]):
    map[i][j] = 0
    adjacents = [(x, y) for (x, y) in get_adjacents(i, j) if 1 <= map[x][y] < 10]
    for (x, y) in adjacents:
        if map[x][y] != 0:
            map[x][y] += 1
        if map[x][y] > 9:
            flash(x, y, map)


def solve():
    map = []
    for line in sys.stdin:
        map.append([int(d) for d in line.strip()])

    steps = 0
    while True:
        for i in range(10):
            for j in range(10):
                map[i][j] += 1
        for i in range(10):
            for j in range(10):
                if map[i][j] > 9:
                    flash(i, j, map)
        steps += 1
        flashes = 0
        for i in range(10):
            for j in range(10):
                if map[i][j] == 0:
                    flashes += 1
        if flashes == 100:
            break
        if steps < 10 or steps % 10 == 0:
            print(steps)
            for row in map:
                print(row)
    return steps


if __name__ == '__main__':
    print(solve())
