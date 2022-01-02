import sys
from collections import Counter, defaultdict


def solve():
    if sys.argv[1] == 'part1':
        answers = []
        current_questionnaire = defaultdict(int)
        for line in sys.stdin:
            if line.strip() == "":
                answers.append(current_questionnaire)
                current_questionnaire = defaultdict(int)
            else:
                for (k, v) in Counter(line.strip()).items():
                    current_questionnaire[k] += v
        answers.append(current_questionnaire)

        return sum(len(a.keys()) for a in answers)
    if sys.argv[1] == 'part2':
        answers = []
        current_questionnaire = defaultdict(int)
        people = 0
        for line in sys.stdin:
            if line.strip() == "":
                answers.append((people, current_questionnaire))
                current_questionnaire = defaultdict(int)
                people = 0
            else:
                for (k, v) in Counter(line.strip()).items():
                    current_questionnaire[k] += v
                people += 1
        answers.append((people, current_questionnaire))

        return sum(len([
            v
            for v in a.values()
            if v == people
        ]) for (people, a) in answers)


if __name__ == '__main__':
    print(solve())
