import sys
from collections import defaultdict
from typing import Dict
from typing import Set


def parse_graph(line: str, graph: Dict[str, Set[str]]):
    (from_node, to_node) = line.split("-")
    if from_node == 'end' or to_node == 'start':
        (from_node, to_node) = (to_node, from_node)
    if to_node not in ['start', 'end'] and from_node not in ['start', 'end']:
        graph[to_node].add(from_node)
    graph[from_node].add(to_node)


def bfs(node: str, graph: Dict[str, Set[str]], path: [str], small_caves: Set[str]) -> [[str]]:
    if len(path) > 1 and path[0] == 'end':
        return []
    if node != 'end' and node.islower() and node in small_caves:
        return []
    elif node != 'end' and node.islower():
        small_caves.add(node)
    path.append(node)
    if len(graph[node]) == 0:
        if node == 'end':
            return [path]
        return []
    paths = []
    for n in graph[node]:
        paths.extend(bfs(n, graph, path.copy(), small_caves.copy()))
    return paths


def solve():
    graph = defaultdict(set)
    for line in sys.stdin:
        parse_graph(line.strip(), graph)

    return len(bfs('start', graph, [], set()))


if __name__ == '__main__':
    print(solve())
