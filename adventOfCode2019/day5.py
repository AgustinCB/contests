import sys
from typing import List, Tuple


def run_intcode(instructions: List[int], inputs: List[int]) -> List[int]:
    def fetch_value(index: int, immediate: bool) -> int:
        if immediate:
            return instructions[index]
        else:
            return instructions[instructions[index]]

    def addition(index: int, modes: Tuple[bool, bool]):
        instructions[instructions[index + 3]] = fetch_value(index + 1, modes[0]) + fetch_value(index + 2, modes[1])

    def multiplication(index: int, modes: Tuple[bool, bool]):
        instructions[instructions[index + 3]] = fetch_value(index + 1, modes[0]) * fetch_value(index + 2, modes[1])

    outputs = []
    i = 0
    while i < len(instructions) and instructions[i] != 99:
        print(instructions[i:i+4])
        opcode = instructions[i] % 100
        param1_mode = instructions[i] % 1000 >= 100
        param2_mode = instructions[i] % 10000 >= 1000
        if opcode == 1:
            addition(i, (param1_mode, param2_mode))
            i += 4
        elif opcode == 2:
            multiplication(i, (param1_mode, param2_mode))
            i += 4
        elif opcode == 3:
            instructions[instructions[i + 1]] = inputs.pop()
            i += 2
        elif opcode == 4:
            value = fetch_value(i + 1, param1_mode)
            outputs.append(value)
            i += 2
        elif opcode == 5:
            parameter = fetch_value(i + 1, param1_mode)
            if parameter != 0:
                i = fetch_value(i + 2, param2_mode)
            else:
                i += 3
        elif opcode == 6:
            parameter = fetch_value(i + 1, param1_mode)
            if parameter == 0:
                i = fetch_value(i + 2, param2_mode)
            else:
                i += 3
        elif opcode == 7:
            parameter1 = fetch_value(i + 1, param1_mode)
            parameter2 = fetch_value(i + 2, param2_mode)
            if parameter1 < parameter2:
                instructions[instructions[i + 3]] = 1
            else:
                instructions[instructions[i + 3]] = 0
            i += 4
        elif opcode == 8:
            parameter1 = fetch_value(i + 1, param1_mode)
            parameter2 = fetch_value(i + 2, param2_mode)
            if parameter1 == parameter2:
                instructions[instructions[i + 3]] = 1
            else:
                instructions[instructions[i + 3]] = 0
            i += 4
        else:
            raise RuntimeError("Invalid instruction code {}: {} {} {}".format(instructions[i], opcode, param1_mode, param2_mode))

    return outputs


def solve():
    byte_code = [int(c) for c in sys.stdin.readline().strip().split(",")]
    if sys.argv[1] == 'part1':
        return run_intcode(byte_code, [1])
    if sys.argv[1] == 'part2':
        return run_intcode(byte_code, [5])


if __name__ == '__main__':
    print(solve())
