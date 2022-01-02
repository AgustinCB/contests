import sys
import typing


def is_corrupted(line: str) -> typing.Optional[str]:
    stack = []
    for c in line.strip():
        if c in ['(', '{', '[', '<']:
            stack.append(c)
        else:
            closing = stack.pop()
            if (closing == '(' and c != ')') or \
                (closing == '[' and c != ']') or \
                (closing == '{' and c != '}') or \
                (closing == '<' and c != '>'):
                return c
    return None


def is_incomplete(line: str) -> typing.Optional[str]:
    stack = []
    for c in line.strip():
        if c in ['(', '{', '[', '<']:
            stack.append(c)
        else:
            stack.pop()
    missing = ""
    for c in reversed(stack):
        if c == '(':
            missing += ')'
        elif c == '[':
            missing += ']'
        elif c == '{':
            missing += '}'
        elif c == '<':
            missing += '>'
    return missing


scoring = {')': 1, ']': 2, '}': 3, '>': 4}


def solve():
    scores = []
    for line in sys.stdin:
        closing = is_corrupted(line)
        if closing is None:
            missing = is_incomplete(line)
            score = 0
            for c in missing:
                score *= 5
                score += scoring[c]
            scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


if __name__ == '__main__':
    print(solve())
