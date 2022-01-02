import sys


def solve():
    depth = 0
    horizontal = 0
    for line in sys.stdin:
        (command, quantity) = line.split(" ")
        quantity = int(quantity)
        if command == "forward":
            horizontal += quantity
        elif command == "down":
            depth += quantity
        else:
            depth -= quantity
    return depth * horizontal


if __name__ == '__main__':
    print(solve())
