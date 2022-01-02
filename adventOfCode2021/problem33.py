import math
import sys
from typing import List


def get_maximum_y(y: int) -> int:
    return int(y * (y + 1) / 2)


def does_velocity_passes_through_square(square_limits: ((int, int), (int, int)), y_velocity: int, x_velocity: int) -> bool:
    current_x = 0
    current_y = 0
    current_x_velocity = x_velocity
    current_y_velocity = y_velocity
    while current_y >= square_limits[1][0]:
        if square_limits[0][0] <= current_x <= square_limits[0][1] and square_limits[1][0] <= current_y <= square_limits[1][1]:
            return True
        current_y += current_y_velocity
        current_x += current_x_velocity
        current_y_velocity -= 1
        if current_x_velocity > 0:
            current_x_velocity -= 1
    return False


def find_maximum_y(square_limits: ((int, int), (int, int)), possible_xs: List[int], possible_ys: List[int]) -> int:
    maximum_ys = []
    for possible_x in possible_xs:
        for possible_y in possible_ys:
            if does_velocity_passes_through_square(square_limits, possible_y, possible_x):
                maximum_ys.append(get_maximum_y(possible_y))
    return max(maximum_ys)


def get_square_limits(input_str: str) -> ((int, int), (int, int)):
    xs, ys = input_str.replace("target area: ", "").replace("x=", "").replace("y=", "").split(", ")
    from_x, to_x = [int(c) for c in xs.split("..")]
    from_y, to_y = [int(c) for c in ys.split("..")]
    return (abs(from_x), abs(to_x)), (from_y, to_y)


def does_positive_velocity_coord_passes_through_line(velocity_coord: int, from_velocity_coord: int, to_velocity_coord: int) -> bool:
    limit = velocity_coord * (velocity_coord + 1) / 2
    if limit < from_velocity_coord:
        return False
    if from_velocity_coord <= limit <= to_velocity_coord:
        return True
    current_velocity_coord = limit
    for i in range(1, velocity_coord + 1):
        current_velocity_coord -= i
        if from_velocity_coord <= current_velocity_coord <= to_velocity_coord:
            return True
        if from_velocity_coord > current_velocity_coord:
            return False
    return False


def find_xs_that_passes_through_area(from_x: int, to_x: int) -> List[int]:
    one_step_xs = list(range(from_x, to_x + 1))
    bellow_half_way = []
    for x in range(math.ceil(to_x / 2) + 1):
        if does_positive_velocity_coord_passes_through_line(x, from_x, to_x):
            bellow_half_way.append(x)
    return bellow_half_way + one_step_xs


def find_ys_that_passes_through_area(from_y: int, to_y: int) -> List[int]:
    if from_y >= 0:
        return find_xs_that_passes_through_area(from_y, to_y)
    possible_ys = []
    for y in range(1, abs(from_y) + 1):
        current_position = y + 1
        current_y = y + 1
        while current_position <= abs(from_y):
            if abs(to_y) <= current_position <= abs(from_y):
                possible_ys.append(y)
                break
            current_y += 1
            current_position += current_y
    return possible_ys


def solve():
    square_limits = get_square_limits(sys.stdin.readline().strip())
    possible_xs = find_xs_that_passes_through_area(square_limits[0][0], square_limits[0][1])
    possible_ys = find_ys_that_passes_through_area(square_limits[1][0], square_limits[1][1])
    return find_maximum_y(square_limits, possible_xs, possible_ys)


if __name__ == '__main__':
    print(solve())
