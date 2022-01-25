from __future__ import annotations

import math
import sys
from typing import List, Tuple, Optional, Set, Callable

import numpy as np

Vector = Tuple[int]

TileData = List[Vector]

TRANSFORMATIONS = [
    (1, 2, 3, 4),
    (-4, 1, -2, 3),
    (-3, -4, -1, -2),
    (2, -3, 4, -1),
    (3, -2, 1, -4),
    (-2, -1, -4, -3),
    (-1, 4, -3, 2),
    (4, 3, 2, 1),
]

flip_horizontally = lambda m: np.flip(m, axis=1)
flip_vertically = lambda m: np.flip(m, axis=0)
rotate_180 = lambda m: np.rot90(m, k=1, axes=(1, 0))
identity = lambda m: m

TRANSFORMATIONS_OPERATIONS = [
    [np.array],
    [rotate_180],
    [flip_horizontally, flip_vertically],
    [rotate_180, flip_vertically, flip_horizontally],
    [flip_vertically],
    [rotate_180, flip_vertically],
    [flip_horizontally],
    [flip_vertically, rotate_180]
]


MONSTER_DRAWING_SIZE = (20, 3)
MONSTER_RELATIVE_COORDINATES = {
    (0, 1),
    (1, 2),
    (4, 2),
    (5, 1),
    (6, 1),
    (7, 2),
    (10, 2),
    (11, 1),
    (12, 1),
    (13, 2),
    (16, 2),
    (17, 1),
    (18, 0),
    (18, 1),
    (19, 1),
}


def get_one_coordinates(drawing: List[List[int]]) -> List[Tuple[int, int]]:
    coordinates = []
    for (i, row) in enumerate(drawing):
        for (j, pixel) in enumerate(row):
            if pixel == 1:
                coordinates.append((j, i))
    return coordinates


def coordinates_to_drawing(coordinates: Set[Tuple[int, int]], size: Tuple[int, int]) -> List[List[int]]:
    return [
        [1 if (i, j) in coordinates else 0 for i in range(size[0])]
        for j in range(size[1])
    ]


def transform_matrix(matrix: List[Vector], ops: []) -> List[List[int]]:
    temporary = matrix[:]
    for op in ops:
        temporary = op(temporary)
    return temporary.tolist()


def transform_pattern(drawing: List[List[int]], ops: List[Callable[[List[List[int]]], 'np.ndarray[int]']]) -> List[Tuple[int, int]]:
    transposed_drawing = transform_matrix(drawing, ops)
    return get_one_coordinates(transposed_drawing)


MONSTER_DRAWINGS = [
    transform_pattern(coordinates_to_drawing(MONSTER_RELATIVE_COORDINATES, MONSTER_DRAWING_SIZE), ops)
    for ops in TRANSFORMATIONS_OPERATIONS
]


def transform_border(borders: [Vector, Vector, Vector, Vector], transformation: int) -> Tuple[int]:
    new_border = borders[abs(transformation) - 1]
    if np.sign(transformation) == -1:
        return tuple(reversed(new_border))
    else:
        return tuple(new_border)


def positional_transform(borders: Tuple[Vector, Vector, Vector, Vector], transformation: Tuple[int, int, int, int]) -> \
        List[Tuple[int]]:
    return [
        transform_border(borders, transformation[0]),
        transform_border(borders, transformation[1]),
        transform_border(borders, transformation[2]),
        transform_border(borders, transformation[3]),
    ]


def get_pattern_positions(i: int, j: int, pattern: List[Tuple[int, int]], size: int) -> Set[Tuple[int, int]]:
    return {(i + pi, j + pj) for (pi, pj) in pattern if 0 <= i + pi < size and 0 <= j + pj < size}


def find_patterns_in_bit_map(pattern: List[Tuple[int, int]], bit_map: List[List[int]]) -> int:
    positions = set()
    patterns = []
    for (j, row) in enumerate(bit_map):
        for (i, bit) in enumerate(row):
            pattern_positions = get_pattern_positions(i, j, pattern, len(bit_map))
            if len(pattern_positions) == len(pattern) and all(bit_map[pj][pi] == 1 for (pi, pj) in pattern_positions):
                patterns.append((i, j))
                positions = positions.union(pattern_positions)
    return len(positions)


class Tile(object):
    def __init__(self, tile_id: int, data: TileData):
        self.tile_id = tile_id
        self.data = data
        transposed_data = np.transpose(data)
        self.borders = (data[0], tuple(transposed_data[-1]), data[-1], tuple(transposed_data[0]))
        self.free_borders = None
        self.neighbors = []
        self.all_borders = set()
        for border in self.borders:
            self.all_borders.add(border)
            self.all_borders.add(tuple(reversed(border)))
        self.transformation = 0

    def check_if_its_corner_tile(self, others: List[Tile]) -> bool:
        return len(self.get_free_borders(others)) == 2

    def check_if_its_side_tile(self, others: List[Tile]) -> bool:
        return len(self.get_free_borders(others)) == 1

    def get_free_borders(self, others: List[Tile]) -> Set[Vector]:
        all_borders = set()
        for other in others:
            if other.tile_id == self.tile_id:
                continue
            all_borders = all_borders.union(other.all_borders)
        self.free_borders = set(self.borders) - all_borders
        return set(self.borders) - all_borders

    def transpose_to(self, border: Vector, position: int) -> bool:
        for (i, t) in enumerate(TRANSFORMATIONS):
            transformed = positional_transform(self.borders, t)
            if transformed[position] == border:
                self.transformation = i
                self.borders = tuple(transformed)
                return True
        return False

    def transpose_to_two(self, first_pair: Tuple[Vector, int], second_pair: Tuple[Vector, int]):
        for (i, t) in enumerate(TRANSFORMATIONS):
            transformed = positional_transform(self.borders, t)
            if (transformed[first_pair[1]] == first_pair[0] or transformed[first_pair[1]] == tuple(
                    reversed(first_pair[0]))) and \
                    (transformed[second_pair[1]] == second_pair[0] or transformed[second_pair[1]] == tuple(
                        reversed(second_pair[0]))):
                self.transformation = i
                self.borders = tuple(transformed)
                self.free_borders = {
                    transformed[first_pair[1]],
                    transformed[second_pair[1]],
                }
                return
        raise RuntimeError(
            "Couldn't find transformation for {} and {} for {}".format(first_pair, second_pair, self.tile_id))

    def inner_tile(self) -> List[List[int]]:
        self.transform()
        content = [
            row[1:-1][:]
            for row in self.data[1:-1]
        ]
        return content

    def transform(self):
        self.data = transform_matrix(
            self.data,
            TRANSFORMATIONS_OPERATIONS[self.transformation],
        )
        self.transformation = 0

    def __hash__(self):
        return self.data.__hash__()


def find_borders(tiles: List[Tile], debug: bool = False) -> (List[Tile], List[List[Tile]]):
    borders = []
    inside = []
    for tile in tiles:
        n_free_borders = len(tile.get_free_borders(tiles))
        if debug:
            print(n_free_borders)
        if n_free_borders in [1, 2]:
            borders.append(tile)
        elif n_free_borders > 0:
            raise RuntimeError("More free borders than expected: {}".format(n_free_borders))
        else:
            inside.append(tile)
    map_size = int(math.sqrt(len(inside)))
    inside = [
        [
            inside[i * map_size + j]
            for j in range(map_size)
        ]
        for i in range(map_size)
    ]
    return borders, inside


def arrange_four_tiles(tiles: Tuple[Tile, Tile, Tile, Tile]) -> List[List[Tile]]:
    tile_map = [[None, None], [None, None]]
    first_borders = list(tiles[0].free_borders)
    tiles[0].transpose_to_two((first_borders[0], 0), (first_borders[1], 3))
    tile_map[0][0] = tiles[0]
    working_tiles = list(tiles[1:])
    for (x, y, target, from_x, from_y, source) in [
        (0, 1, 0, 0, 0, 2),
        (1, 0, 3, 0, 0, 1),
        (1, 1, 0, 1, 0, 2)]:
        for i in range(len(working_tiles)):
            tile = working_tiles[i]
            if tile.transpose_to(tile_map[from_y][from_x].borders[source], target):
                tile_map[y][x] = tile
                working_tiles.remove(tile)
                break
    return tile_map


def expand_inside(borders: List[Tile], inside: List[List[Tile]]) -> List[List[Tile]]:
    def get_adjacent_border_to(border: Vector, transpose_to: int) -> Tile:
        adjacent_borders = [
            b for b in borders
            if border in b.all_borders
        ]
        if len(adjacent_borders) != 1:
            raise RuntimeError(
                "EXPECTED 1 BORDER ADJACENT TO {}, got {}, tile ids {}, borders {}".format(
                    border,
                    len(adjacent_borders),
                    [t.tile_id for t in adjacent_borders],
                    [b.tile_id for b in borders]
                )
            )
        tile_border = adjacent_borders[0]
        tile_border.transpose_to(border, transpose_to)
        borders.remove(tile_border)
        return tile_border

    if len(inside) > 1:
        next_borders, next_inside = find_borders([tile for row in inside for tile in row])
        inside = expand_inside(next_borders, next_inside)
    if len(inside) == 0:
        return arrange_four_tiles(tuple(borders))
    new_size = len(inside) + 2
    tile_map = [
        [
            None if i == 0 or i == new_size - 1 or j == 0 or j == new_size - 1
            else inside[j - 1][i - 1]
            for i in range(new_size)
        ]
        for j in range(new_size)
    ]
    for (j, row) in enumerate(inside):
        for (i, tile) in enumerate(row):
            if 0 < j < len(inside) - 1 and 0 < i < len(inside) - 1:
                continue
            if j == 0:
                tile_map[0][i + 1] = get_adjacent_border_to(tile.borders[0], 2)
            if i == len(inside) - 1:
                tile_map[j + 1][-1] = get_adjacent_border_to(tile.borders[1], 3)
            if j == len(inside) - 1:
                tile_map[-1][i + 1] = get_adjacent_border_to(tile.borders[2], 0)
            if i == 0:
                tile_map[j + 1][0] = get_adjacent_border_to(tile.borders[3], 1)
    for (i, j, neighbor, source, target) in [
        (0, 0, tile_map[1][0], 0, 2),
        (0, -1, tile_map[1][-1], 0, 2),
        (-1, 0, tile_map[-2][0], 2, 0),
        (-1, -1, tile_map[-2][-1], 2, 0),
    ]:
        tile_map[i][j] = get_adjacent_border_to(neighbor.borders[source], target)
    return tile_map


def tile_map_to_bit_map(tile_map: List[List[Tile]]) -> List[List[int]]:
    tile_size = (len(tile_map[0][0].data) - 2)
    bit_map = [[] for _ in range(len(tile_map) * tile_size)]

    for (j, row) in enumerate(tile_map):
        for tile in row:
            for (ij, inner_row) in enumerate(tile.inner_tile()):
                bit_map[j * tile_size + ij] += inner_row
    return bit_map


def parse_tile() -> Optional[Tile]:
    tile_id_string = sys.stdin.readline()
    if tile_id_string.strip() == "":
        return None
    tile_id = int(tile_id_string.strip().replace("Tile ", "").replace(":", ""))
    tile_data = []
    for line in sys.stdin:
        if line.strip() == "":
            break
        line_data = [1 if c == '#' else 0 for c in line.strip()]
        tile_data.append(tuple(line_data))
    return Tile(tile_id, tile_data)


def solve():
    tiles = []
    finished = False
    while not finished:
        finished = True
        tile = parse_tile()
        if tile is not None:
            tiles.append(tile)
            finished = False
    if sys.argv[1] == 'part1':
        corners = 1
        for tile1 in tiles:
            if tile1.check_if_its_corner_tile(tiles):
                corners *= tile1.tile_id
        return corners
    if sys.argv[1] == 'part2':
        borders, inside = find_borders(tiles)
        tile_map = expand_inside(borders, inside)
        bit_map = tile_map_to_bit_map(tile_map)
        ones = sum(sum(row) for row in bit_map)
        for pattern in MONSTER_DRAWINGS:
            taken_ones = find_patterns_in_bit_map(pattern, bit_map)
            if taken_ones > 0:
                return ones - taken_ones
        return 0


if __name__ == '__main__':
    print(solve())
