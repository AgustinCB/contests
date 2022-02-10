import sys
from typing import List

Layer = List[List[int]]
Image = List[Layer]


def parse_image(image_data: str, width: int, height: int) -> Image:
    layers = []
    data = [int(c) for c in image_data]
    current_row = []
    current_layer = []
    for d in data:
        if len(current_row) == width:
            current_layer.append(current_row)
            current_row = []
            if len(current_layer) == height:
                layers.append(current_layer)
                current_layer = []
        current_row.append(d)
    return layers


def find_pixel(image: Image, x: int, y: int) -> str:
    for layer in image:
        if layer[y][x] == 0:
            return ' '
        if layer[y][x] == 1:
            return '*'
    return ' '


def render_image(image: Image, width: int, height: int) -> List[List[str]]:
    layer = [[' ' for _ in range(width)] for _ in range(height)]
    positions = [(x, y) for x in range(width) for y in range(height)]
    for (x, y) in positions:
        layer[y][x] = find_pixel(image, x, y)
    return layer


def solve():
    image = parse_image(sys.stdin.readline().strip(), 25, 6)
    if sys.argv[1] == 'part1':
        min_layer = None
        zeros = None

        for layer in image:
            local_zeros = sum([len([i for i in row if i == 0]) for row in layer])
            if zeros is None or local_zeros < zeros:
                min_layer = layer
                zeros = local_zeros

        local_ones = sum([len([i for i in row if i == 1]) for row in min_layer])
        local_twos = sum([len([i for i in row if i == 2]) for row in min_layer])
        return local_ones * local_twos
    if sys.argv[1] == 'part2':
        layer = render_image(image, 25, 6)
        for row in layer:
            print(''.join([str(p) for p in row]))
        return None


if __name__ == '__main__':
    print(solve())
