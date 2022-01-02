import collections
import sys


def solve():
    for line in sys.stdin:
        positions = [int(i) for i in line.split(",")]
    positions_cache = dict(collections.Counter(positions))
    min_fuel = None
    from_p = min(positions_cache.keys())
    to_p = max(positions_cache.keys())
    for p in range(from_p, to_p + 1):
        fuel = 0
        for (p1, n1) in positions_cache.items():
            if p == p1: continue
            n1 = positions_cache[p1]
            distance = abs(p1-p)
            fuel_cost = (1 + distance) * distance / 2
            fuel += fuel_cost * n1
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
    return min_fuel


if __name__ == '__main__':
    print(solve())
