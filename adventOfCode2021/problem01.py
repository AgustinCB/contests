import sys


def solve():
    prev_depth = None
    counter = 0
    for line in sys.stdin:
        depth = int(line)
        if prev_depth is not None and depth > prev_depth:
            counter += 1
        prev_depth = depth
    return counter


if __name__ == '__main__':
    print(solve())
