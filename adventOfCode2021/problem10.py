import sys
from collections import defaultdict


def parse_point(point):
    (x, y) = point.split(",")
    return [int(x), int(y)]

def solve():
    points_count = defaultdict(int)
    for line in sys.stdin:
        (from_point, to_point) = line.split(" -> ")
        from_point = parse_point(from_point)
        to_point = parse_point(to_point)
        diff_from = abs(from_point[0] - to_point[0])
        diff_to = abs(from_point[1] - to_point[1])
        if from_point[0] == to_point[0]:
            if from_point[1] > to_point[1]:
                to_point[1], from_point[1] = from_point[1], to_point[1]
            for y in range(from_point[1], to_point[1] + 1):
                points_count["{}x{}".format(from_point[0], y)] += 1
        elif from_point[1] == to_point[1]:
            if from_point[0] > to_point[0]:
                to_point[0], from_point[0] = from_point[0], to_point[0]
            for x in range(from_point[0], to_point[0] + 1):
                points_count["{}x{}".format(x, from_point[1])] += 1
        elif diff_from == diff_to:
            if from_point[0] > to_point[0]:
                direction_x = -1
            else:
                direction_x = 1
            if from_point[1] > to_point[1]:
                direction_y = -1
            else:
                direction_y = 1
            for i in range(diff_from + 1):
                points_count["{}x{}".format(from_point[0] + i * direction_x, from_point[1] + i * direction_y)] += 1

    count = len([0 for c in points_count.values() if c >= 2])
    return count


if __name__ == '__main__':
    print(solve())
