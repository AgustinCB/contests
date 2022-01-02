import sys


def solve():
    scores = []
    for line in sys.stdin:
        if ':' in line:
            (fdie, sdie) = [int(c) for c in line.split(':')]
            scores.append(fdie + sdie)

    for (i, score) in enumerate(scores):
        needed = score + 1 if score < 12 else '-'
        print("Case #{}: {}".format(i + 1, needed))


if __name__ == '__main__':
    solve()

