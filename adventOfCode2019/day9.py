import sys
from collections import defaultdict
from typing import List, Tuple


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
            self.program[self.relative_base + self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) + self.fetch_value(index + 2,
                                                                                                             modes[1])
        else:
            self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) + self.fetch_value(index + 2, modes[1])

    def multiplication(self, index: int, modes: Tuple[int, int], relative_output: bool):
        if relative_output:
            self.program[self.relative_base + self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) * self.fetch_value(index + 2,
                                                                                                             modes[1])
        else:
            self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) * self.fetch_value(index + 2, modes[1])

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
            if param1_mode == 1:
                self.program[self.program[self.ip + 1]] = self.inputs.pop()
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

    @staticmethod
    def parse_string(input_program: str) -> List[int]:
        return [int(c) for c in input_program.strip().split(",")]


def solve():
    machine = IntCodeMachine(IntCodeMachine.parse_string(sys.stdin.readline()), [2])
    if sys.argv[1] == 'part1':
        return machine.run()
    if sys.argv[1] == 'part2':
        pass


if __name__ == '__main__':
    print(solve())
