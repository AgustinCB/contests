from collections import Counter, defaultdict
import sys
from typing import Optional, Dict, Tuple


class SequenceNode(object):
    def __init__(self, value: str, next):
        self.value = value
        self.next = next


class Sequence(object):
    def __init__(self, starting_node: SequenceNode, counter: Dict[str, int]):
        self.starting_node = starting_node
        self.counter = counter
        self.reset()

    def reset(self):
        self.current_node = self.starting_node
        self.previous_node = None

    def add_node(self, value: str):
        if value not in self.counter:
            self.counter[value] = 0
        self.counter[value] += 1
        new_node = SequenceNode(value, self.previous_node.next)
        self.previous_node.next = new_node

    def get_current_pair(self) -> Optional[str]:
        if self.current_node.next is None:
            return None
        pair = self.current_node.value + self.current_node.next.value
        self.advance_current_node()
        return pair

    def advance_current_node(self):
        self.previous_node = self.current_node
        self.current_node = self.current_node.next


def create_sequence(string_value: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    possible_pairs = defaultdict(int)
    counter = dict(Counter(string_value))
    for i in range(1, len(string_value)):
        pair = string_value[i-1:i+1]
        possible_pairs[pair] += 1
    return possible_pairs, counter


def solve():
    sequence, counter = create_sequence(sys.stdin.readline().strip())
    sys.stdin.readline()
    steps = {}
    for line in sys.stdin:
        from_pair, add_node = line.strip().split(" -> ")
        steps[from_pair.strip()] = add_node.strip()

    for day in range(40):
        to_add = defaultdict(int)
        to_remove = defaultdict(int)
        for (pair, number) in sequence.items():
            if pair in steps:
                if steps[pair] not in counter:
                    counter[steps[pair]] = 0
                counter[steps[pair]] += number
                to_add[pair[0] + steps[pair]] += number
                to_add[steps[pair] + pair[1]] += number
                to_remove[pair] += number
        for (pair, number) in to_add.items():
            sequence[pair] += number
        for (pair, number) in to_remove.items():
            sequence[pair] -= number

    min_count = min(counter.values())
    max_count = max(counter.values())
    return max_count - min_count


if __name__ == '__main__':
    print(solve())
