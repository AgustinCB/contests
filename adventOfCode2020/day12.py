import sys
from typing import Tuple, List


def move(command: str, argument: int, current_position: Tuple[int, int]) -> Tuple[int, int]:
    if command == "E":
        return current_position[0] + argument, current_position[1]
    elif command == "W":
        return current_position[0] - argument, current_position[1]
    elif command == "N":
        return current_position[0], current_position[1] + argument
    elif command == "S":
        return current_position[0], current_position[1] - argument


def run_instructions(starting_position: Tuple[int, int], starting_direction: int, instructions: List[str]) -> Tuple[int, int, int]:
    current_position = starting_position[:]
    current_direction = starting_direction
    directions = ["E", "N", "W", "S"]
    r_to_l = [0, 3, 2, 1]
    for instruction in instructions:
        command = instruction[0]
        argument = int(instruction[1:])
        if command == "F":
            current_position = move(directions[current_direction], argument, current_position)
        elif command == "L" or command == "R":
            argument = argument // 90
            if command == "R":
                argument = r_to_l[argument]
            current_direction = (current_direction + argument) % 4
        else:
            current_position = move(command, argument, current_position)
    return current_position[0], current_position[1], current_direction


def run_instructions_with_waypoint(
        starting_position: Tuple[int, int],
        starting_waypoint_position: Tuple[int, int],
        instructions: List[str]
) -> Tuple[int, int]:
    current_position = starting_position[:]
    current_waypoint_position = starting_waypoint_position
    r_to_l = [0, 3, 2, 1]
    for instruction in instructions:
        command = instruction[0]
        argument = int(instruction[1:])
        if command == "F":
            current_position = (
                current_position[0] + current_waypoint_position[0] * argument,
                current_position[1] + current_waypoint_position[1] * argument
            )
        elif command == "L" or command == "R":
            argument = argument // 90
            if command == "R":
                argument = r_to_l[argument]
            if argument == 1:
                current_waypoint_position = (-current_waypoint_position[1], current_waypoint_position[0])
            elif argument == 2:
                current_waypoint_position = (-current_waypoint_position[0], -current_waypoint_position[1])
            elif argument == 3:
                current_waypoint_position = (current_waypoint_position[1], -current_waypoint_position[0])
        else:
            current_waypoint_position = move(command, argument, current_waypoint_position)
    return current_position[0], current_position[1]


def solve():
    instructions = [l.strip() for l in sys.stdin]

    if sys.argv[1] == 'part1':
        x, y, _ = run_instructions((0, 0), 0, instructions)
        return abs(x) + abs(y)
    if sys.argv[1] == 'part2':
        x, y = run_instructions_with_waypoint((0, 0), (10, 1), instructions)
        return abs(x) + abs(y)


if __name__ == '__main__':
    print(solve())
