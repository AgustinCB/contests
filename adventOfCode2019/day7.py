import itertools
import sys
from typing import List, Tuple


class IntCodeMachine(object):
    def __init__(self, program: List[input], inputs: List[int]):
        self.program = program
        self.inputs = inputs
        self.outputs = []
        self.ip = 0

    def fetch_value(self, index: int, immediate: bool) -> int:
        if immediate:
            return self.program[index]
        else:
            return self.program[self.program[index]]

    def addition(self, index: int, modes: Tuple[bool, bool]):
        self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) + self.fetch_value(index + 2, modes[1])

    def multiplication(self, index: int, modes: Tuple[bool, bool]):
        self.program[self.program[index + 3]] = self.fetch_value(index + 1, modes[0]) * self.fetch_value(index + 2, modes[1])

    def peek_instruction(self):
        return self.program[self.ip] % 100

    def run_next(self) -> int:
        opcode = self.peek_instruction()
        param1_mode = self.program[self.ip] % 1000 >= 100
        param2_mode = self.program[self.ip] % 10000 >= 1000
        if opcode == 1:
            self.addition(self.ip, (param1_mode, param2_mode))
            self.ip += 4
        elif opcode == 2:
            self.multiplication(self.ip, (param1_mode, param2_mode))
            self.ip += 4
        elif opcode == 3:
            self.program[self.program[self.ip + 1]] = self.inputs.pop()
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
            if parameter1 < parameter2:
                self.program[self.program[self.ip + 3]] = 1
            else:
                self.program[self.program[self.ip + 3]] = 0
            self.ip += 4
        elif opcode == 8:
            parameter1 = self.fetch_value(self.ip + 1, param1_mode)
            parameter2 = self.fetch_value(self.ip + 2, param2_mode)
            if parameter1 == parameter2:
                self.program[self.program[self.ip + 3]] = 1
            else:
                self.program[self.program[self.ip + 3]] = 0
            self.ip += 4
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


def calculate_signal(program: List[int], configuration: Tuple[int, int, int, int, int]) -> int:
    current_input = 0
    for setting in configuration:
        current_program = program.copy()
        machine = IntCodeMachine(current_program, [current_input, setting])
        outputs = machine.run()
        current_input = outputs[0]
    return current_input


def calculate_signal_with_feedback_loop(program: List[int], configuration: Tuple[int, int, int, int, int]) -> int:
    programs = {
        'A': IntCodeMachine(program.copy(), [0, configuration[0]]),
        'B': IntCodeMachine(program.copy(), [configuration[1]]),
        'C': IntCodeMachine(program.copy(), [configuration[2]]),
        'D': IntCodeMachine(program.copy(), [configuration[3]]),
        'E': IntCodeMachine(program.copy(), [configuration[4]]),
    }
    links = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'A'}
    current_machine = programs['A']
    current_machine_id = 'A'
    while any(p.can_continue() for p in programs.values()):
        while current_machine.peek_instruction() == 3 and len(current_machine.inputs) == 0:
            current_machine_id = links[current_machine_id]
            current_machine = programs[current_machine_id]
        opcode = current_machine.run_next()
        if opcode == 4:
            programs[links[current_machine_id]].inputs.insert(0, current_machine.outputs.pop())
        elif opcode == 99:
            current_machine_id = links[current_machine_id]
            current_machine = programs[current_machine_id]
    return programs['A'].inputs[0]


def solve():
    program = [int(code) for code in sys.stdin.readline().strip().split(",")]
    if sys.argv[1] == 'part1':
        return max([
            calculate_signal(program, configuration)
            for configuration in itertools.permutations(range(5))
        ])
    if sys.argv[1] == 'part2':
        return max([
            calculate_signal_with_feedback_loop(program, configuration)
            for configuration in itertools.permutations(range(5, 10))
        ])


if __name__ == '__main__':
    print(solve())
