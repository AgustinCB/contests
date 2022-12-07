import sys
from typing import Iterable, List, Tuple


Movement = Tuple[int, int, int]
Stacks = List[List[str]]


def parse_map(input_stream: Iterable[str]) -> Stacks:
    length = -1
    stacks = []
    for line in input_stream:
        if not line.strip():
            break
        if length == -1:
            length = (len(line) + 1) // 4
            print(length, len(line), line)
            stacks = [[] for _ in range(length)]
        for i in range(length):
            c = line[i * 4 + 1]
            if c != ' ':
                stacks[i].append(c)
    return [list(reversed(s[:-1])) for s in stacks]


def parse_movement(input_string: str) -> Movement:
    input_string = input_string.replace("move ", "")
    quantity, stacks = input_string.split(" from ")
    from_stack, to_stack = stacks.split(" to ")
    return int(quantity), int(from_stack) - 1, int(to_stack) - 1


def parse_movements(input_stream: Iterable[str]) -> List[Movement]:
    return [parse_movement(line) for line in input_stream]


def parse(input_stream: Iterable[str]) -> Tuple[Stacks, List[Movement]]:
    return parse_map(input_stream), parse_movements(input_stream)


def perform_movement(stacks: Stacks, movement: Movement):
    to_move = list(reversed(stacks[movement[1]][-movement[0]:]))
    stacks[movement[2]] += to_move
    stacks[movement[1]] = stacks[movement[1]][:-movement[0]]


def perform_movement_for_model_9001(stacks: Stacks, movement: Movement):
    to_move = stacks[movement[1]][-movement[0]:]
    stacks[movement[2]] += to_move
    stacks[movement[1]] = stacks[movement[1]][:-movement[0]]


def solve():
    stacks, movements = parse(sys.stdin)
    if sys.argv[1] == 'part1':
        for movement in movements:
            perform_movement(stacks, movement)
        return ''.join([s[-1] for s in stacks])
    if sys.argv[1] == 'part2':
        for movement in movements:
            perform_movement_for_model_9001(stacks, movement)
        return ''.join([s[-1] for s in stacks])


if __name__ == '__main__':
    print(solve())
