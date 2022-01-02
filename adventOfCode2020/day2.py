import sys
from collections import Counter
from typing import Tuple


def parse_password_policy(policy: str) -> Tuple[int, int, str]:
    policy_range, letter = policy.split(" ")
    range_from, range_to = policy_range.split("-")
    return int(range_from), int(range_to), letter


def parse_case(case: str) -> Tuple[Tuple[int, int, str], str]:
    policy_str, password = case.split(':')
    return parse_password_policy(policy_str), password


def validate_case(case: Tuple[Tuple[int, int, str], str]) -> bool:
    policy, password = case
    letter_counter = Counter(password.strip())
    return policy[0] <= (letter_counter[policy[2]] if policy[2] in letter_counter else 0) <= policy[1]


def validate_case_by_position(case: Tuple[Tuple[int, int, str], str]) -> bool:
    policy, password = case
    password = list(password.strip())
    return len([i for i in [policy[0], policy[1]] if password[i-1] == policy[2]]) == 1


def solve():
    cases = []
    for line in sys.stdin:
        cases.append(parse_case(line.strip()))

    if sys.argv[1] == 'part1':
        return len([1 for case in cases if validate_case(case)])
    if sys.argv[1] == 'part2':
        return len([1 for case in cases if validate_case_by_position(case)])


if __name__ == '__main__':
    print(solve())
