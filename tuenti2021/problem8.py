import sys
from collections import defaultdict
from typing import Dict, Set, Optional

NEXT_NOTE = {
    'C': 'D',
    'D': 'E',
    'E': 'F',
    'F': 'G',
    'G': 'A',
    'A': 'B',
    'B': 'C',
}
NOTE_INTERVALS = {
    'C': 2,
    'D': 2,
    'E': 1,
    'F': 2,
    'G': 2,
    'A': 2,
    'B': 1,
}


class Scale(object):
    def __init__(self, root: str, intervals: [int]):
        self.root = root
        self.intervals = intervals

    def notes(self) -> [str]:
        notes = [self.root]
        last_whole_note = self.root[0]
        for interval in self.intervals:
            next_whole_note = NEXT_NOTE[last_whole_note]
            last_whole_note = next_whole_note
            if notes[-1] in NOTE_INTERVALS:
                if NOTE_INTERVALS[notes[-1]] == interval:
                    notes.append(next_whole_note)
                elif NOTE_INTERVALS[notes[-1]] < interval:
                    notes.append(next_whole_note + '#')
                elif NOTE_INTERVALS[notes[-1]] > interval:
                    notes.append(next_whole_note + 'b')
            else:
                if NOTE_INTERVALS[notes[-1][0]] == interval:
                    notes.append(next_whole_note + notes[-1][1])
                else:
                    notes.append(next_whole_note)
        return notes


def parse_scale() -> Scale:
    root = sys.stdin.readline().strip()
    string_intervals = sys.stdin.readline().strip()
    intervals = [1 if si == 's' else 2 for si in string_intervals]
    return Scale(root, intervals)


def parse_graph() -> Dict[str, list]:
    n_nodes = int(sys.stdin.readline().strip())
    graph = defaultdict(list)
    for _ in range(n_nodes):
        (city_one, city_two) = sys.stdin.readline().strip().split(",")
        graph[city_one].append(city_two)
        graph[city_two].append(city_one)
    return graph


def spanning_tree(graph: Dict[str, list]) -> Optional[Set[str]]:
    keys = list(graph.keys())
    tree = []
    in_tree = set()
    in_tree.add(keys[0])
    pending = set(keys[1:])
    while len(pending) > 0:
        to_add = None
        for from_node in in_tree:
            for to_node in graph[from_node]:
                if to_node in pending:
                    tree.append([from_node, to_node])
                    to_add = to_node
                    break
            if to_add is not None:
                break
        if to_add is not None:
            in_tree.add(to_add)
            pending.remove(to_add)
        else:
            return None
    return set(["{},{}".format(f, t) for f, t in tree])


def can_remove_city(graph: Dict[str, list], city: str) -> bool:
    new_graph = graph.copy()
    del new_graph[city]
    spanning = spanning_tree(new_graph)
    return spanning is not None


def detect_the_ones_that_can_not_remove(graph: Dict[str, list]) -> [str]:
    can_not_remove = []
    for city in graph.keys():
        if not can_remove_city(graph, city):
            can_not_remove.append(city)
    return can_not_remove


def cities_to_list(cities: [str]) -> str:
    if len(cities) == 0:
        return '-'
    return ','.join(sorted(cities))


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        graph = parse_graph()
        can_remove = detect_the_ones_that_can_not_remove(graph)
        print("Case #{}: {}".format(test + 1, cities_to_list(can_remove)))


if __name__ == '__main__':
    solve()

