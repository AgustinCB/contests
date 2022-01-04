import functools
import sys


def solve():
    numbers = [0]
    for line in sys.stdin:
        numbers.append(int(line.strip()))
    numbers.sort()
    numbers.append(numbers[-1] + 3)

    if sys.argv[1] == 'part1':
        difference1 = len([j for (i, j) in enumerate(numbers[1:]) if j - 1 == numbers[i]])
        difference3 = len([j for (i, j) in enumerate(numbers[1:]) if j - 3 == numbers[i]])
        return difference1 * difference3
    if sys.argv[1] == 'part2':
        combinations_per_ones = [0, 2, 4, 7, 13]
        differences = ''.join([str(j - numbers[i]) for (i, j) in enumerate(numbers[1:])])
        groups = differences.split('3')
        combinations = [combinations_per_ones[len(g) - 1] for g in groups if g]
        return functools.reduce(lambda x, y: x*y, [c for c in combinations if c > 0])


if __name__ == '__main__':
    print(solve())
