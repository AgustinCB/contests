import collections
import sys


def solve():
    for line in sys.stdin:
        positions = [int(i) for i in line.split(",")]
    positions_cache = dict(collections.Counter(positions))
    min_fuel = None
    for (p, _) in positions_cache.items():
        fuel = 0
        for (p1, n1) in positions_cache.items():
            if p == p1: continue
            fuel += abs(p1-p) * n1
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


if __name__ == '__main__':
    print(solve())
