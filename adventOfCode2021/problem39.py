import sys
from typing import Set, Tuple, List


def parse_light_pixels(padding=0) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    light_pixels = set()
    max_row = None
    max_column = None
    for (row, line) in enumerate(sys.stdin):
        for (column, pixel) in enumerate(line.strip()):
            if pixel == '#':
                light_pixels.add((row + padding, column + padding))
            if max_column is None or column > max_column:
                max_column = column
        if max_row is None or row > max_row:
            max_row = row
    return light_pixels, (max_row + 1 + padding, max_column + 1 + padding)


def get_pixel(
        algorithm: List[str], light_pixels: Set[Tuple[int, int]], row: int, column: int, input_boundaries: Tuple[Tuple[int, int], Tuple[int, int]], outside: str = '.'
) -> str:
    bits = []
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if (r, c) in light_pixels:
                bits.append(1)
            elif not (input_boundaries[0][0] <= r < input_boundaries[0][1]) or \
                    not (input_boundaries[1][0] <= c < input_boundaries[1][1]):
                bits.append(0 if outside == '.' else 1)
            else:
                bits.append(0)
    index = int(''.join([str(b) for b in bits]), 2)
    return algorithm[index]


def enhance(
        algorithm: List[str],
        light_pixels: Set[Tuple[int, int]],
        size: Tuple[int, int],
        outside: str = '.'
) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    new_points = set()
    new_size = size[0] + 2, size[1] + 2
    test_pixels = {(x + 1, y + 1) for x, y in light_pixels}
    input_boundaries = ((1, size[0] + 1), (1, size[1] + 1))
    for row in range(new_size[0]):
        for column in range(new_size[1]):
            if get_pixel(algorithm, test_pixels, row, column, input_boundaries, outside) == "#":
                new_points.add((row, column))
    return new_points, new_size


def print_map(light_pixels: Set[Tuple[int, int]], size: Tuple[int, int]):
    print(len(light_pixels))
    for row in range(size[0]):
        print(''.join(['#' if (row, c) in light_pixels else '.' for c in range(size[1])]))
    print()


def solve():
    algorithm = list(sys.stdin.readline().strip())
    sys.stdin.readline()
    current_pixels, size = parse_light_pixels(0)
    step = 0
    while step < 50:
        outside = '.' if algorithm[0] == '.' else (algorithm[-1] if step % 2 == 0 else algorithm[0])
        print_map(current_pixels, size)
        current_pixels, size = enhance(algorithm, current_pixels, size, outside)
        step += 1
    print_map(current_pixels, size)
    return len(current_pixels)


if __name__ == '__main__':
    print(solve())
