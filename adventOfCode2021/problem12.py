import collections
import multiprocessing
import sys

cache = {}


def children_for(i, days):
    if i >= days:
        return 0
    key = "{}x{}".format(i, days)
    if key in cache:
        return cache[key]
    children = 1
    days_left = days - i - 1
    for d in range(days_left // 7):
        children += children_for(i + 1 + 7 * d + 8, days) + 1
    cache[key] = children
    return children


def solve_for(d, tdays):
    children = children_for(d, tdays)
    children.reverse()
    total = len(children)
    j = 0
    print(d)
    print(children)
    while len(children) > 0:
        (i, days) = children.pop()
        new_children = children_for(i + days + 1, tdays)
        print("{} {} {} {} {}".format(i + days + 1, tdays, new_children, children, total))
        total += len(new_children)
        children.extend(new_children)
        j += 1
    return total


def solve_for1(i, tdays):
    if i in cache:
        return cache[i]
    lanternfishes = [i]
    d = 0
    while d < tdays:
        t = len(lanternfishes)
        for i in range(t):
            lanternfish = lanternfishes[i]
            if lanternfish == 0:
                lanternfishes[i] = 6
                lanternfishes.append(8)
            else:
                lanternfishes[i] -= 1
        d += 1
    total = len(lanternfishes)
    cache[i] = total
    return total


def solve():
    for line in sys.stdin:
        lanternfishes = [int(i) for i in line.split(",")]
    l_dict = collections.defaultdict(int)
    for l in lanternfishes:
        l_dict[l] += 1

    # return children_for(lanternfishes[4], 18)
    outputs = [children_for(l, 256) * n for (l, n) in l_dict.items()]
    return sum(outputs) + len(lanternfishes)


def solve2():
    for line in sys.stdin:
        lanternfishes = [int(i) for i in line.split(",")]

    pool = multiprocessing.Pool(len(lanternfishes))
    outputs = pool.map(solve_for, lanternfishes)
    return sum(outputs)


def solve1():
    for line in sys.stdin:
        lanternfishes = [int(i) for i in line.split(",")]

    all_children = [children_for(lanternfish, 256) for lanternfish in lanternfishes]
    children = []
    for cs in all_children:
        children.extend(cs)
    total = len(lanternfishes) + len(children)
    j = 0
    while len(children) > 0:
        (i, days) = children.pop()
        new_children = children_for(i, 256 - days)
        total += len(new_children)
        if j % 100000 == 0:
            print(total)
        children.extend(new_children)
        j += 1
    return total


if __name__ == '__main__':
    print(solve())
