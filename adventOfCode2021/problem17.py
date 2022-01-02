import sys


def solve():
    map = []
    for line in sys.stdin:
        row = [int(c) for c in line.strip()]
        map.append(row)

    height = len(map)
    width = len(map[0])
    total_risk = 0

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
                total_risk += depth + 1

    return total_risk


if __name__ == '__main__':
    print(solve())
