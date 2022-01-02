import sys


def solve():
    for line in sys.stdin:
        lanternfishes = [int(i) for i in line.split(",")]

    day = 0
    while day < 80:
        new_lanternfishes = []
        for lanternfish in lanternfishes:
            if lanternfish == 0:
                new_lanternfishes.append(6)
                new_lanternfishes.append(8)
            else:
                new_lanternfishes.append(lanternfish - 1)
        lanternfishes = new_lanternfishes

        day += 1
    return len(lanternfishes)


if __name__ == '__main__':
    print(solve())
