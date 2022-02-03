import copy
import sys
from collections import defaultdict
from typing import Tuple, List

TileCoordinate = Tuple[int, int]


DIRECTIONS = [
    (-1, 1),  # North-west
    (-1, 0),  # West
    (0, -1),  # South-west
    (1, -1),  # South-east
    (1, 0),   # East
    (0, 1),   # North-east
]


def parse_line(line: str) -> List[TileCoordinate]:
    result = []
    i = 0
    while i < len(line):
        if line[i] == 'e':
            result.append(DIRECTIONS[4])
        elif line[i] == 'w':
            result.append(DIRECTIONS[1])
        elif line[i] == 's':
            i += 1
            if line[i] == 'w':
                result.append(DIRECTIONS[2])
            elif line[i] == 'e':
                result.append(DIRECTIONS[3])
        else:
            i += 1
            if line[i] == 'w':
                result.append(DIRECTIONS[0])
            elif line[i] == 'e':
                result.append(DIRECTIONS[5])
        i += 1
    return result


def parse_instructions() -> List[List[TileCoordinate]]:
    return [parse_line(line.strip()) for line in sys.stdin]


def tile_coordinate(steps: List[TileCoordinate]) -> TileCoordinate:
    coordinate = (0, 0)
    for step in steps:
        coordinate = (coordinate[0] + step[0], coordinate[1] + step[1])
    return coordinate


def adjacent_tiles(tile: TileCoordinate) -> List[TileCoordinate]:
    return [(tile[0] + d[0], tile[1] + d[1]) for d in DIRECTIONS]


def solve():
    tiles = parse_instructions()
    tile_colors = defaultdict(bool)
    for tile in tiles:
        tile_colors[tile_coordinate(tile)] = not tile_colors[tile_coordinate(tile)]
    if sys.argv[1] == 'part1':
        return sum(1 for is_black in tile_colors.values() if is_black)
    if sys.argv[1] == 'part2':
        for i in range(100):
            new_tile_colors = copy.deepcopy(tile_colors)
            interesting_whites = set()
            for coord, is_black in list(tile_colors.items()):
                if not is_black:
                    continue
                neighbors = adjacent_tiles(coord)
                blacks = sum(1 for n in neighbors if tile_colors[n])
                if blacks > 2 or blacks == 0:
                    new_tile_colors[coord] = False
                interesting_whites = interesting_whites.union({n for n in neighbors if not tile_colors[n]})
            for coord in interesting_whites:
                neighbors = adjacent_tiles(coord)
                blacks = sum(1 for n in neighbors if tile_colors[n])
                if blacks == 2:
                    new_tile_colors[coord] = True
            tile_colors = new_tile_colors
        return sum(1 for is_black in tile_colors.values() if is_black)


if __name__ == '__main__':
    print(solve())
