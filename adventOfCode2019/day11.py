import sys
from collections import defaultdict
from collections.abc import Set
from typing import List, Optional, Tuple, Dict


class IntCodeMachine(object):
    def __init__(self, program: List[input], inputs: List[int]):
        self.program = defaultdict(int)
        for (i, byte) in enumerate(program):
            self.program[i] = byte
        self.inputs = inputs
        self.outputs = []
        self.ip = 0
        self.relative_base = 0

    def fetch_value(self, index: int, mode: int) -> int:
        if mode == 1:
            return self.program[index]
        elif mode == 0:
            return self.program[self.program[index]]
        elif mode == 2:
            return self.program[self.relative_base + self.program[index]]
        else:
            raise RuntimeError("Invalid fetch mode {}", mode)

    def addition(self, index: int, modes: Tuple[int, int], relative_output: bool):
        if relative_output:
            self.program[self.relative_base + self.program[index + 3]] = self.fetch_value(index + 1,
                                                                                          modes[0]) + self.fetch_value(
                index + 2,
                modes[1])
        else:
            self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) + self.fetch_value(index + 2,
                                                                                                             modes[1])

    def multiplication(self, index: int, modes: Tuple[int, int], relative_output: bool):
        if relative_output:
            self.program[self.relative_base + self.program[index + 3]] = self.fetch_value(index + 1,
                                                                                          modes[0]) * self.fetch_value(
                index + 2,
                modes[1])
        else:
            self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) * self.fetch_value(index + 2,
                                                                                                             modes[1])

    def peek_instruction(self):
        return self.program[self.ip] % 100

    def run_next(self) -> int:
        opcode = self.peek_instruction()
        param1_mode = (self.program[self.ip] % 1000) // 100
        param2_mode = (self.program[self.ip] % 10000) // 1000
        relative_output = (self.program[self.ip] % 100000) // 10000 == 2
        if opcode == 1:
            self.addition(self.ip, (param1_mode, param2_mode), relative_output)
            self.ip += 4
        elif opcode == 2:
            self.multiplication(self.ip, (param1_mode, param2_mode), relative_output)
            self.ip += 4
        elif opcode == 3:
            if param1_mode == 0:
                self.program[self.program[self.ip + 1]] = self.inputs.pop()
            elif param1_mode == 1:
                self.program[self.ip + 1] = self.inputs.pop()
            elif param1_mode == 2:
                self.program[self.relative_base + self.program[self.ip + 1]] = self.inputs.pop()
            self.ip += 2
        elif opcode == 4:
            value = self.fetch_value(self.ip + 1, param1_mode)
            self.outputs.append(value)
            self.ip += 2
        elif opcode == 5:
            parameter = self.fetch_value(self.ip + 1, param1_mode)
            if parameter != 0:
                self.ip = self.fetch_value(self.ip + 2, param2_mode)
            else:
                self.ip += 3
        elif opcode == 6:
            parameter = self.fetch_value(self.ip + 1, param1_mode)
            if parameter == 0:
                self.ip = self.fetch_value(self.ip + 2, param2_mode)
            else:
                self.ip += 3
        elif opcode == 7:
            parameter1 = self.fetch_value(self.ip + 1, param1_mode)
            parameter2 = self.fetch_value(self.ip + 2, param2_mode)
            index = self.relative_base + self.program[self.ip + 3] if relative_output else self.program[self.ip + 3]
            if parameter1 < parameter2:
                self.program[index] = 1
            else:
                self.program[index] = 0
            self.ip += 4
        elif opcode == 8:
            parameter1 = self.fetch_value(self.ip + 1, param1_mode)
            parameter2 = self.fetch_value(self.ip + 2, param2_mode)
            index = self.relative_base + self.program[self.ip + 3] if relative_output else self.program[self.ip + 3]
            if parameter1 == parameter2:
                self.program[index] = 1
            else:
                self.program[index] = 0
            self.ip += 4
        elif opcode == 9:
            self.relative_base += self.fetch_value(self.ip + 1, param1_mode)
            self.ip += 2
        elif opcode == 99:
            return opcode
        else:
            raise RuntimeError("Invalid instruction code {}: {} {} {}".format(
                self.program[self.ip], opcode, param1_mode, param2_mode
            ))
        return opcode

    def can_continue(self) -> bool:
        return self.ip < len(self.program) and self.program[self.ip] != 99

    def run(self) -> List[int]:
        while self.can_continue():
            self.run_next()
        return self.outputs

    def run_until_output(self) -> Optional[int]:
        code = self.run_next()
        while code != 4 and self.can_continue():
            code = self.run_next()
        if self.program[self.ip] == 99:
            return None
        return self.outputs.pop()

    @staticmethod
    def parse_string(input_program: str) -> List[int]:
        return [int(c) for c in input_program.strip().split(",")]


DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def robot(brain: IntCodeMachine, starting_color: int) -> Dict[Tuple[int, int], int]:
    painted = set()
    colors = defaultdict(int)
    current_position = (0, 0)
    colors[current_position] = starting_color
    direction = 1
    iterations = 0
    while brain.can_continue():
        brain.inputs = [colors[current_position]]
        color = brain.run_until_output()
        if color is None:
            break
        if color not in [1, 0]:
            raise RuntimeError("Unexpected color: {}".format(color))
        colors[current_position] = color
        painted.add(current_position)
        turn = brain.run_until_output()
        if turn == 0:
            direction = (direction - 1) % len(DIRECTIONS)
        elif turn == 1:
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            raise RuntimeError("Unexpected direction: {}".format(direction))
        current_position = (
            current_position[0] + DIRECTIONS[direction][0], current_position[1] + DIRECTIONS[direction][1])
        iterations += 1
    return colors


def solve():
    machine = IntCodeMachine(IntCodeMachine.parse_string(sys.stdin.readline()), [])
    if sys.argv[1] == 'part1':
        return len(robot(machine, 0))
    if sys.argv[1] == 'part2':
        colors = robot(machine, 1)
        message_positions = sorted(list(colors))
        width = max(i[0] for i in message_positions) + 1
        height = max(abs(i[1]) for i in message_positions) + 1
        message = ''
        for y in range(height):
            row = ''
            for x in range(width):
                row += '#' if (x, -y) in colors and colors[(x, -y)] == 1 else '.'
            message += row + '\n'
        return message


if __name__ == '__main__':
    print(solve())
