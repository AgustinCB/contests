import sys
from typing import Dict, Tuple, List, Union

Rule = Union[str, Tuple[List[int], List[int]], List[int]]
Rules = Dict[int, Rule]


def parse_rules() -> Rules:
    rules = {}
    for line in sys.stdin:
        if line.strip() == "":
            break
        id_string, rule_string = line.strip().split(": ")
        if '"' in rule_string:
            rules[int(id_string)] = rule_string.replace('"', "")
        elif "|" in rule_string:
            option1, option2 = rule_string.split(" | ")
            rules[int(id_string)] = ([int(c) for c in option1.split(" ")], [int(c) for c in option2.split(" ")])
        else:
            rules[int(id_string)] = [int(c) for c in rule_string.split(" ")]
    return rules


def match_list(content: str, rule: List[int], rules: Rules) -> (bool, str):
    current_content = content
    for rule in rule:
        matched, current_content = match_rule(current_content, rule, rules)
        if not matched:
            return False, content
    return True, current_content


def match_rule(content: str, rule: int, rules: Rules) -> (bool, str):
    rule = rules[rule]
    if content == "":
        return False, content
    if type(rule) == str:
        if content.startswith(rule):
            return True, content[len(rule):]
        return False, content
    if type(rule) == list:
        return match_list(content, rule, rules)
    if type(rule) == tuple:
        matched, remaining = match_list(content, rule[0], rules)
        if not matched:
            return match_list(content, rule[1], rules)
        return True, remaining


def solve():
    rules = parse_rules()
    candidates = [line.strip() for line in sys.stdin]
    if sys.argv[1] == 'part1':
        total = 0
        for c in candidates:
            matched, remaining = match_rule(c, 0, rules)
            if matched and remaining == "":
                total += 1
        return total
    if sys.argv[1] == 'part2':
        rules[8] = ([42], [42, 8])
        rules[11] = ([42, 31], [42, 11, 31])
        """
        Given that 0 = [8, 11],
        The input has to have the form:
        [42] [42] ... [42] [31] [31] ... [31]
        Where the numbers of 42s is major than the number of 31s
        """
        total = 0
        for c in candidates:
            remaining = c
            matched = True
            total_42 = 0
            while matched:
                matched, remaining = match_rule(remaining, 42, rules)
                if matched:
                    total_42 += 1
            if total_42 < 1:
                continue
            matched = True
            total_31 = 0
            while matched:
                matched, remaining = match_rule(remaining, 31, rules)
                if matched:
                    total_31 += 1
            if total_31 < 1 or total_31 >= total_42 or remaining != "":
                continue
            total += 1

        return total


if __name__ == '__main__':
    print(solve())
