import sys
from typing import Set


def fold_paper(fold: [str], points: Set[str]) -> Set[str]:
    breaking_point = int(fold[1])
    index = 0 if fold[0] == 'x' else 1
    new_points = points.copy()
    for point in points:
        p = [int(i) for i in point.strip().split(",")]
        if p[index] == breaking_point:
            new_points.remove(point)
        elif p[index] > breaking_point:
            new_points.remove(point)
            p[index] = p[index] - (p[index] - breaking_point) * 2
            new_point = "{},{}".format(p[0], p[1])
            new_points.add(new_point)
    return new_points


def print_points(string_points: [str]):
    points = []
    width = None
    length = None
    for sp in string_points:
        p = [int(c) for c in sp.split(",")]
        points.append(p)
        if width == None or p[1] > width:
            width = p[1]
        if length == None or p[0] > length:
            length = p[0]
    point_map = [['.' for _ in range(width + 1)] for _ in range(length + 1)]
    for (x, y) in points:
        point_map[x][y] = '#'
    print(width, length, points)
    for row in point_map:
        print(" ".join(row))


def solve():
    points = set()
    folds = []
    parsing_points = True
    for line in sys.stdin:
        if line.strip() == "":
            parsing_points = False
        elif parsing_points:
            points.add(line.strip())
        else:
            fold = line.split("fold along")[1].strip()
            folds.append(fold.split("="))

    for fold in folds:
        points = fold_paper(fold, points)
    print_points(points)
    return len(points)


if __name__ == '__main__':
    print(solve())
