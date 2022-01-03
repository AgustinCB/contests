import sys
from typing import List, Set, Tuple, Optional


class Booter(object):
    def __init__(self, program: List[str]):
        self.accumulator = 0
        self.instructions_ran = set()
        self.ip = 0
        self.program = program

    def run_until_infinite_loop(self) -> int:
        while self.ip < len(self.program):
            if self.ip in self.instructions_ran:
                return self.accumulator
            self.instructions_ran.add(self.ip)
            instruction, offset = self.program[self.ip].split(" ")
            self.__run_instruction(instruction, int(offset))
        return self.accumulator

    def fix_program(self) -> int:
        last_changed = None
        while True:
            self.instructions_ran = set()
            self.ip = 0
            self.accumulator = 0
            index, previous = self.__revert_first_jmp_nop(last_changed)
            last_changed = index + 1
            acc = self.run_until_infinite_loop()
            if self.ip == len(self.program):
                return acc
            self.program[index] = previous

    def __revert_first_jmp_nop(self, last_changed: Optional[int]) -> Tuple[int, str]:
        offset = 0 if last_changed is None else last_changed
        for (i, instruction) in enumerate(self.program[offset:]):
            if instruction.startswith("nop") or instruction.startswith("jmp"):
                prev = instruction
                if instruction.startswith("nop"):
                    self.program[i + offset] = self.program[i + offset].replace("nop", "jmp")
                elif instruction.startswith("jmp"):
                    self.program[i + offset] = self.program[i + offset].replace("jmp", "nop")
                return i + offset, prev

    def __run_instruction(self, instruction: str, offset: int):
        if instruction == "nop":
            self.ip += 1
        elif instruction == "acc":
            self.accumulator += offset
            self.ip += 1
        elif instruction == "jmp":
            self.ip += offset


def solve():
    program = [line.strip() for line in sys.stdin]

    if sys.argv[1] == 'part1':
        return Booter(program).run_until_infinite_loop()
    if sys.argv[1] == 'part2':
        return Booter(program).fix_program()


if __name__ == '__main__':
    print(solve())
