import sys
from typing import Tuple, List, Optional, Iterator, Dict

Range = Tuple[int, int]


def number_complies_rule(number: int, rule: List[Range]) -> bool:
    return any(rule_range[0] <= number <= rule_range[1] for rule_range in rule)


def is_number_valid(number: int, rules: Iterator[List[Range]]) -> bool:
    return any(number_complies_rule(number, rule) for rule in rules)


def is_ticket_invalid(numbers: List[int], rules: Iterator[List[Range]]) -> Optional[int]:
    for number in numbers:
        if not is_number_valid(number, rules):
            return number
    return None


def column_complies_rule(column: List[int], rule: List[Range]) -> bool:
    return all(number_complies_rule(n, rule) for n in column)


def match_columns_and_rules(tickets: List[List[int]], rules: Dict[str, List[Range]]) -> Dict[str, int]:
    matching = {}
    columns = [[ticket[i] for ticket in tickets] for i in range(len(tickets[0]))]
    while len(matching) < len(rules):
        for (i, column) in enumerate(columns):
            matching_rules = [rule_name for (rule_name, rule) in rules.items() if rule_name not in matching and column_complies_rule(column, rule)]
            if len(matching_rules) == 1:
                matching[matching_rules[0]] = i
    return matching


def solve():
    rules = {}
    for line in sys.stdin:
        if line.strip() == "":
            break
        rule_name, ranges = line.strip().split(": ")
        ranges = [(int(r.split('-')[0]), int(r.split('-')[1])) for r in ranges.split(" or ")]
        rules[rule_name] = ranges
    sys.stdin.readline()
    my_ticket = [int(c) for c in sys.stdin.readline().strip().split(',')]
    sys.stdin.readline()
    sys.stdin.readline()
    nearby_tickets = []
    for line in sys.stdin:
        nearby_tickets.append([int(c) for c in line.strip().split(',')])

    if sys.argv[1] == 'part1':
        invalid_numbers = [is_ticket_invalid(ticket, rules.values()) for ticket in nearby_tickets]
        return sum(n for n in invalid_numbers if n is not None)
    if sys.argv[1] == 'part2':
        valid_tickets = [ticket for ticket in nearby_tickets if is_ticket_invalid(ticket, rules.values()) is None]
        matching = match_columns_and_rules(valid_tickets, rules)
        total = 1
        for (rule_name, column) in matching.items():
            if rule_name.startswith("departure "):
                total *= my_ticket[column]
        return total


if __name__ == '__main__':
    print(solve())
