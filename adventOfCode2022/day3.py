import sys


def char_to_priority(char: str) -> int:
    padding = 0 if char.islower() else 26
    return padding + ord(char.lower()) - 96


def solve():
    if sys.argv[1] == 'part1':
        commons = []
        for line in sys.stdin:
            first_half = line[:len(line) // 2]
            second_half = line[len(line) // 2:]
            common = list(set(list(first_half)) & set(list(second_half)))[0]
            commons.append(common)
        print([(common, char_to_priority(common)) for common in commons])
        return sum(char_to_priority(common) for common in commons)
    if sys.argv[1] == 'part2':
        group = []
        commons = []
        for line in sys.stdin:
            if len(group) == 3:
                commons.append(list(group[0] & group[1] & group[2])[0])
                group = []
            group.append(set(list(line.strip())))
        commons.append(list(group[0] & group[1] & group[2])[0])
        print([(common, char_to_priority(common)) for common in commons])
        return sum(char_to_priority(common) for common in commons)


if __name__ == '__main__':
    print(solve())
