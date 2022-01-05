import functools
import sys


def solve():
    target = int(sys.stdin.readline())
    buses = sys.stdin.readline().strip().split(",")
    ids = [int(i) for i in buses if i != 'x']

    if sys.argv[1] == 'part1':
        (closest_bus, bus_id) = min([((target // bus_id + 1) * bus_id, bus_id) for bus_id in ids])
        return (closest_bus - target) * bus_id
    if sys.argv[1] == 'part2':
        values = [(i - buses.index(str(i))) % i for i in ids]
        N = functools.reduce(lambda x, y: x*y, ids, 1)
        ys = [N//i for i in ids]
        zs = [pow(y, -1, i) for (y, i) in zip(ys, ids)]
        return sum([y * a * z for (a, y, z) in zip(values, ys, zs)]) % N


if __name__ == '__main__':
    print(solve())
