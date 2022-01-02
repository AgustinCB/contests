import sys
from typing import Dict


class Battle(object):
    def __init__(self, first_word: str, second_word: str, values: Dict[str, float]):
        self.first_word = first_word
        self.second_word = second_word
        self.values = values

    def score_word(self, word: str) -> float:
        score = 0
        for c in word:
            score += self.values[c]
        return score

    def perform_battle(self) -> str:
        first_score = self.score_word(self.first_word)
        second_score = self.score_word(self.second_word)
        if first_score > second_score:
            return self.first_word
        elif second_score > first_score:
            return self.second_word
        else:
            return '-'


def parse_words(words: str) -> (str, str):
    (f, s) = words.split("-")
    return f, s


def parse_value(v: str) -> float:
    if '/' in v:
        (num, den) = [int(c) for c in v.split('/')]
        return num/den
    return float(v)


def parse_values_from_dict(values: str) -> Dict[str, float]:
    kv_pairs = values[1:-1].strip().split(",")
    values = {}
    for kv_pair in kv_pairs:
        (k, v) = kv_pair.strip().split(':')
        values[k.strip()[1:-1]] = parse_value(v.strip())
    return values


def parse_values_from_tuples(values: str) -> Dict[str, float]:
    kv_pairs = values[2:-2].strip().split("), (")
    values = {}
    for kv_pair in kv_pairs:
        (k, v) = kv_pair.strip().split(',')
        values[k.strip()[1:-1]] = parse_value(v.strip())
    return values


def parse_values_from_assignments(values: str) -> Dict[str, float]:
    kv_pairs = values.strip().split(",")
    values = {}
    for kv_pair in kv_pairs:
        (k, v) = kv_pair.strip().split('=')
        values[k.strip()] = parse_value(v.strip())
    return values


def parse_values(values: str) -> Dict[str, float]:
    if '{' == values[0]:
        return parse_values_from_dict(values)
    elif '[' == values[0]:
        return parse_values_from_tuples(values)
    else:
        return parse_values_from_assignments(values)


def parse_battle() -> Battle:
    test = sys.stdin.readline().strip()
    (words, values) = test.split("|")
    (first_word, second_word) = parse_words(words)
    values = parse_values(values)
    return Battle(first_word, second_word, values)


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        battle = parse_battle()
        print("Case #{}: {}".format(test + 1, battle.perform_battle()))


if __name__ == '__main__':
    solve()

