import sys


points = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "A": 1,
    "B": 2,
    "C": 3,
}


resolution_points = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


possible_matches = {
    "A X": 3,
    "A Y": 6,
    "A Z": 0,
    "B X": 0,
    "B Y": 3,
    "B Z": 6,
    "C X": 6,
    "C Y": 0,
    "C Z": 3,
}


arranged_points = {
    "A X": 3,
    "A Y": 1,
    "A Z": 2,
    "B X": 1,
    "B Y": 2,
    "B Z": 3,
    "C X": 2,
    "C Y": 3,
    "C Z": 1,
}


def match_points(match: str) -> int:
    return possible_matches[match]


def arranged_match_points(match: str) -> int:
    return resolution_points[match[-1]]


def solve():
    if sys.argv[1] == 'part1':
        total = 0
        for match in sys.stdin:
            score = match_points(match.strip())
            option_points = points[match.strip()[-1]]
            total += score + option_points
        return total
    if sys.argv[1] == 'part2':
        total = 0
        for match in sys.stdin:
            score = arranged_match_points(match.strip())
            option_points = arranged_points[match.strip()]
            total += score + option_points
        return total


if __name__ == '__main__':
    print(solve())
