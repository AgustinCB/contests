import heapq
import sys
from typing import Tuple, List, Dict, Set


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def vertex_set(weight_map: [[int]]) -> Tuple[Set[str], Dict[str, List[str]]]:
    vertexes = set()
    neighbors = {}
    for y in range(len(weight_map)):
        for x in range(len(weight_map[0])):
            key = "{}x{}".format(x, y)
            vertexes.add(key)
            neighbors[key] = []
            for d in DIRECTIONS:
                if 0 <= x + d[0] < len(weight_map[0]) and 0 <= y + d[1] < len(weight_map):
                    neighbors[key].append("{}x{}".format(x + d[0], y + d[1]))
    return vertexes, neighbors


def min_distance(dist: Dict[str, int], vset: Set[str]) -> str:
    return min([p for p in dist.items() if p[0] in vset], key=lambda p: p[1])[0]


def a_star(weight_map: [[int]], goal: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    _, neighbors = vertex_set(weight_map)
    vset = [(0, "0x0")]
    heapq.heapify(vset)

    dist = {"0x0": 0}
    fscore = {"0x0": 0}
    prev = {}
    goal_x, goal_y = [int(p) for p in goal.split("x")]
    print("START A STAR GOAL {}".format(goal))
    i = 0
    while vset:
        min_vertex = heapq.heappop(vset)[1]
        if i % 1000 == 0:
            print("ITERATION {}: VSET SIZE {} DIST SIZE {} CURRENT {}".format(i, len(vset), len(dist), min_vertex))
        i += 1
        if min_vertex == goal:
            return dist, prev
        for neighbor in neighbors[min_vertex]:
            x, y = [int(p) for p in neighbor.split("x")]
            alt = dist[min_vertex] + weight_map[y][x]
            if neighbor not in dist or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = min_vertex
                fscore[neighbor] = alt + abs(goal_x - x) + abs(goal_y - y)
                if neighbor not in [v[1] for v in vset]:
                    heapq.heappush(vset, (fscore[neighbor], neighbor))
    return dist, prev


def dijkstra(weight_map: [[int]], goal: str) -> Tuple[Dict[str, int], Dict[str, str]]:
    vset, neighbors = vertex_set(weight_map)

    dist = {"0x0": 0}
    prev = {}
    while vset:
        min_vertex = min_distance(dist, vset)
        if min_vertex == goal:
            return dist, prev
        vset.remove(min_vertex)
        for neighbor in [n for n in neighbors[min_vertex] if n in vset]:
            x, y = [int(p) for p in neighbor.split("x")]
            alt = dist[min_vertex] + weight_map[y][x]
            if neighbor not in dist or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = min_vertex
    return dist, prev


def add_to_map(weight_map: [[int]], addendum: int) -> [[int]]:
    return [
        [cell + addendum if cell + addendum < 10 else (cell + addendum) - 9 for cell in row] for row in weight_map
    ]

def merge_maps(maps: [[[[int]]]]) -> [[int]]:
    final_map = []
    for map_row in maps:
        for i in range(len(map_row[0])):
            final_map.append(map_row[0][i] + map_row[1][i] + map_row[2][i] + map_row[3][i] + map_row[4][i])
    return final_map


def parse_map():
    weight_map = []
    for line in sys.stdin:
        weight_map.append([int(c) for c in line.strip()])
    map_plus_one = add_to_map(weight_map, 1)
    map_plus_two = add_to_map(weight_map, 2)
    map_plus_three = add_to_map(weight_map, 3)
    map_plus_four = add_to_map(weight_map, 4)
    map_plus_five = add_to_map(weight_map, 5)
    map_plus_six = add_to_map(weight_map, 6)
    map_plus_seven = add_to_map(weight_map, 7)
    map_plus_eight = add_to_map(weight_map, 8)
    maps = [
        [weight_map, map_plus_one, map_plus_two, map_plus_three, map_plus_four],
        [map_plus_one, map_plus_two, map_plus_three, map_plus_four, map_plus_five],
        [map_plus_two, map_plus_three, map_plus_four, map_plus_five, map_plus_six],
        [map_plus_three, map_plus_four, map_plus_five, map_plus_six, map_plus_seven],
        [map_plus_four, map_plus_five, map_plus_six, map_plus_seven, map_plus_eight],
    ]
    return merge_maps(maps)
    #return weight_map


def solve():
    weight_map = parse_map()
    goal = "{}x{}".format(len(weight_map) - 1, len(weight_map[0]) - 1)
    return a_star(weight_map, goal)[0][goal]


if __name__ == '__main__':
    print(solve())
