import sys


def solve():
    numbers = set()
    for line in sys.stdin:
        numbers.add(int(line.strip()))

    if sys.argv[1] == 'part1':
        for n in numbers:
            if abs(2020-n) in numbers:
                return n * abs(2020-n)
    if sys.argv[1] == 'part2':
        for n in numbers:
            for n1 in numbers - {n}:
                if n + n1 > 2020:
                    continue
                n2 = abs(2020 - n - n1)
                if n2 in numbers:
                    return n * n1 * n2



if __name__ == '__main__':
    print(solve())
