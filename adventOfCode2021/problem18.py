import sys
from typing import Set, Iterator


def solve():
    map = []
    for line in sys.stdin:
        row = [int(c) for c in line.strip()]
        map.append(row)

    height = len(map)
    width = len(map[0])

    def search_basin(i: int, j: int, visited: Set[str]):
        """
        [i - 1, j] if i > 0 and "{}x{}".format(i - 1, j) not in visited and map[i - 1][j] > map[i][j] and map[i - 1][j] != 9 else None,
        [i + 1, j] if i < height - 1 and map[i + 1][j] > map[i][j] and map[i + 1][j] != 9 and "{}x{}".format(i + 1, j) not in visited else None,
        [i, j - 1] if j > 0 and map[i][j - 1] > map[i][j] and map[i][j - 1] != 9 and "{}x{}".format(i, j + 1) not in visited else None,
        [i, j + 1] if j < width - 1 and map[i][j + 1] > map[i][j] and map[i][j + 1] != 9 and "{}x{}".format(i, j + 1) not in visited else None,
        """
        adjacent_alternatives = [
            [i - 1, j] if i > 0 and "{}x{}".format(i - 1, j) not in visited and map[i - 1][j] != 9 else None,
            [i + 1, j] if i < height - 1 and map[i + 1][j] != 9 and "{}x{}".format(i + 1, j) not in visited else None,
            [i, j - 1] if j > 0 and map[i][j - 1] != 9 and "{}x{}".format(i, j - 1) not in visited else None,
            [i, j + 1] if j < width - 1 and map[i][j + 1] != 9 and "{}x{}".format(i, j + 1) not in visited else None,
        ]
        adjacent_points = [p for p in adjacent_alternatives if p is not None]

        for (pi, pj) in adjacent_points:
            visited.add("{}x{}".format(pi, pj))

        for (pi, pj) in adjacent_points:
            search_basin(pi, pj, visited)

    basin_sizes = []
    for i in range(height):
        for j in range(width):
            depth = map[i][j]
            adjacent_alternatives = [
                map[i-1][j] if i > 0 else None,
                map[i+1][j] if i < height-1 else None,
                map[i][j-1] if j > 0 else None,
                map[i][j+1] if j < width-1 else None,
            ]
            adjacent_points = [p for p in adjacent_alternatives if p is not None]
            if depth in adjacent_points:
                continue
            min_depth = min(adjacent_points + [depth])
            if min_depth == depth:
                visited = {"{}x{}".format(i, j)}
                search_basin(i, j, visited)
                basin_sizes.append(len(visited))

    basin_sizes.sort()
    result = 1
    for s in basin_sizes[-3:]:
        result *= s
    return result


if __name__ == '__main__':
    print(solve())
