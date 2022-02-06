import sys
from collections import Counter


def solve():
    from_n, to_n = sys.stdin.readline().strip().split('-')
    if sys.argv[1] == 'part1':
        passwords = []
        for n in range(int(from_n), int(to_n)):
            digits = str(n)
            increased = False
            one_repeat = False
            for (i, d) in enumerate(digits[:-1]):
                if d > digits[i + 1]:
                    increased = True
                    break
                if d == digits[i + 1]:
                    one_repeat = True
            if not increased and one_repeat:
                c = Counter(digits)
                values = set(c.values())
                if 2 in values:
                    passwords.append(n)
        return len(passwords)
    if sys.argv[1] == 'part2':
        pass


if __name__ == '__main__':
    print(solve())
