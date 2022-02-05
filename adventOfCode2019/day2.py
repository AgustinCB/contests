import sys
from typing import List


def run_intcode(instructions: List[int]) -> int:
    i = 0
    while i < len(instructions) and instructions[i] != 99:
        if instructions[i] == 1:
            instructions[instructions[i + 3]] = instructions[instructions[i + 1]] + instructions[instructions[i + 2]]
        elif instructions[i] == 2:
            instructions[instructions[i + 3]] = instructions[instructions[i + 1]] * instructions[instructions[i + 2]]
        i += 4

    return instructions[0]


def solve():
    ins = [int(s) for s in sys.stdin.readline().strip().split(",")]
    if sys.argv[1] == 'part1':
        ins[1], ins[2] = 12, 2
        return run_intcode(ins)
    if sys.argv[1] == 'part2':
        for i in range(100):
            for j in range(100):
                this = ins[:]
                this[1], this[2] = i, j
                res = run_intcode(this)
                if res == 19690720:
                    return 100 * i + j
        pass


if __name__ == '__main__':
    print(solve())
