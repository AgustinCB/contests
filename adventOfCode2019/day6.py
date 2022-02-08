import sys
from collections import defaultdict
from typing import Dict, List


def parse_input() -> Dict[str, str]:
    orbit_info = {}
    for line in sys.stdin:
        orbited, orbitant = line.strip().split(")")
        orbit_info[orbitant] = orbited
    return orbit_info


def parse_graph_input() -> Dict[str, List[str]]:
    graph = defaultdict(list)
    for line in sys.stdin:
        orbited, orbitant = line.strip().split(")")
        graph[orbited].append(orbitant)
        graph[orbitant].append(orbited)
    return graph


def count_orbits(orbitant: str, orbit_info: Dict[str, str]) -> int:
    orbits = 0
    while orbitant in orbit_info:
        orbits += 1
        orbitant = orbit_info[orbitant]
    return orbits


def find_minimum_distance(graph: Dict[str, List[str]]) -> int:
    distances = {'YOU': 0}
    working_stack = [('YOU', 0)]
    while len(working_stack) > 0:
        (current_object, distance) = working_stack.pop()
        if current_object == 'SAN':
            return distance
        new_distance = distance + 1
        for neighbor in graph[current_object]:
            if neighbor not in distances or distances[neighbor] > new_distance:
                distances[neighbor] = new_distance
                working_stack.append((neighbor, new_distance))


def solve():
    if sys.argv[1] == 'part1':
        orbit_info = parse_input()
        return sum([count_orbits(o, orbit_info) for o in orbit_info.keys()])
    if sys.argv[1] == 'part2':
        orbit_graph = parse_graph_input()
        return find_minimum_distance(orbit_graph) - 2


if __name__ == '__main__':
    print(solve())
