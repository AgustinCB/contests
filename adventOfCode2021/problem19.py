import sys
import typing


def is_corrupted(line: str) -> typing.Optional[str]:
    stack = []
    for c in line:
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


def solve():
    counter = 0
    for line in sys.stdin:
        closing = is_corrupted(line)
        if closing == ')':
            counter += 3
        elif closing == ']':
            counter += 57
        elif closing == '}':
            counter += 1197
        elif closing == '>':
            counter += 25137
    return counter


if __name__ == '__main__':
    print(solve())
