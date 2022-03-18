import sys
from collections import defaultdict, Counter
from typing import Optional, List, Tuple, Dict


class IntCodeMachine(object):
    def __init__(self, program: List[input], inputs: List[int]):
        self.program = defaultdict(int)
        for (i, byte) in enumerate(program):
            self.program[i] = byte
        self.inputs = inputs
        self.outputs = []
        self.ip = 0
        self.relative_base = 0

    def fetch_index(self, index: int, mode: int) -> int:
        if mode == 1:
            return index
        elif mode == 0:
            return self.program[index]
        elif mode == 2:
            return self.relative_base + self.program[index]
        else:
            raise RuntimeError("Invalid fetch mode {}", mode)

    def fetch_output_index(self, relative_output: bool, index: int) -> int:
        if relative_output:
            return self.relative_base + self.program[index]
        else:
            return self.program[index]

    def fetch_value(self, index: int, mode: int) -> int:
        index = self.fetch_index(index, mode)
        return self.program[index]

    def addition(self, index: int, modes: Tuple[int, int], relative_output: bool):
        output_index = self.fetch_output_index(relative_output, index + 3)
        self.program[output_index] = self.fetch_value(index + 1, modes[0]) + self.fetch_value(index + 2, modes[1])

    def multiplication(self, index: int, modes: Tuple[int, int], relative_output: bool):
        output_index = self.fetch_output_index(relative_output, index + 3)
        self.program[output_index] = self.fetch_value(index + 1, modes[0]) * self.fetch_value(index + 2, modes[1])

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
            index = self.fetch_index(self.ip + 1, param1_mode)
            self.program[index] = self.inputs.pop()
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

    def run_until_input(self) -> Optional[int]:
        code = self.run_next()
        while code != 3 and self.can_continue():
            code = self.run_next()
        return self.program[self.ip]

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


def print_map(output: List[int], screen_map: Dict[Tuple[int, int], int]) -> Tuple[int, Tuple[int, int], Tuple[int, int]]:
    screen = []
    in_seventh = []
    ball = None
    paddle = None
    for i in range(len(output) // 3):
        x, y, tile_id = output[i * 3], output[i * 3 + 1], output[i * 3 + 2]
        screen.append((x, y, tile_id))
    height = 24
    width = 44
    for (x, y, t) in screen:
        screen_map[(x, y)] = t
    for ((x, y), tile_id) in screen_map.items():
        if (y == 17 or y == 16) and tile_id == 2:
            in_seventh.append((y, x))
    for y in range(height):
        screen_line = ""
        for x in range(width):
            tile = None
            if screen_map[(x, y)] == 0:
                tile = " "
            elif screen_map[(x, y)] == 1:
                tile = "x"
            elif screen_map[(x, y)] == 2:
                tile = "@"
            elif screen_map[(x, y)] == 3:
                tile = "-"
                paddle = (x, y)
            elif screen_map[(x, y)] == 4:
                tile = "o"
                ball = (x, y)
            screen_line += tile
        print(screen_line)
    print()
    print("SCORE", screen_map[(-1, 0)], "BALL", ball, "PADDLE", paddle)
    print()
    return screen_map[(-1, 0)], ball, paddle


def destroy_all_balls(code: List[int]) -> int:
    machine = IntCodeMachine(code, [0])
    screen = {}
    machine.run_until_input()
    print_map(machine.outputs, screen)
    for ((x, y), i) in screen.items():
        if i != 2:
            continue
        machine.program[388] = x
        machine.program[389] = y + 1
        machine.program[390] = 0
        machine.program[391] = -1
        machine.program[2753] = x
        machine.program[2754] = y
        machine.inputs = [0]
        machine.run_until_input()
        print_map(machine.outputs, screen)
    return machine.program[386]


def solve():
    if sys.argv[1] == 'part1':
        machine = IntCodeMachine(IntCodeMachine.parse_string(sys.stdin.readline()), [])
        machine.run()
        return len([tile_id for (i, tile_id) in enumerate(machine.outputs) if i % 3 == 2 and tile_id == 2])
    if sys.argv[1] == 'part2':
        with open("inputs/day13input.txt", "r") as f:
            p = IntCodeMachine.parse_string(f.readline())
        p[0] = 2
        return destroy_all_balls(p)


if __name__ == '__main__':
    print(solve())
