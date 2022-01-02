import sys


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

    fold = folds[0]
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
    return len(new_points)


if __name__ == '__main__':
    print(solve())
