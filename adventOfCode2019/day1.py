import sys


def fuel(size: int) -> int:
    return size // 3 - 2


def recursive_fuel(size: int) -> int:
    f = fuel(size)
    if f <= 0:
        return 0
    if f > 0:
        return f + recursive_fuel(f)


def solve():
    if sys.argv[1] == 'part1':
        return sum([fuel(int(s.strip())) for s in sys.stdin])
    if sys.argv[1] == 'part2':
        return sum([recursive_fuel(int(s.strip())) for s in sys.stdin])


if __name__ == '__main__':
    print(solve())
