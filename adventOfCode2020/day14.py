import sys
from typing import Tuple, Dict


def build_mask(mask: str) -> Tuple[int, int]:
    and_mask = int(''.join([m if m == "0" else "1" for m in mask]), 2)
    or_mask = int(''.join([m if m == "1" else "0" for m in mask]), 2)
    return and_mask, or_mask


def part1_memory() -> Dict[int, int]:
    and_mask, or_mask = build_mask(sys.stdin.readline().strip().split("mask = ")[1])
    memory = {}
    for line in sys.stdin:
        if "mask" not in line:
            address, value = line.strip().split("] = ")
            pre_mask_value = int(value)
            memory[int(address.replace("mem[", ""))] = pre_mask_value & and_mask | or_mask
        else:
            and_mask, or_mask = build_mask(line.strip().split("mask = ")[1])
    return memory


def part2_memory() -> Dict[int, int]:
    mask_line = sys.stdin.readline().strip().split("mask = ")[1]
    _, or_mask = build_mask(mask_line)
    xs = len([c for c in mask_line if c == "X"])
    xindexes = {i for (i, c) in enumerate(list(mask_line)) if c == 'X'}
    memory = {}
    for line in sys.stdin:
        if "mask" not in line:
            address, value = line.strip().split("] = ")
            pre_mask_address = int(address.replace("mem[", "")) | or_mask
            for i in range(2**xs):
                address = pre_mask_address
                mask = ['X' for _ in range(len(mask_line))]
                for (b, xindex) in enumerate(xindexes):
                    mask[xindex] = str(i >> b & 1)
                address_and_mask, address_or_mask = build_mask(''.join(mask))
                memory[address & address_and_mask | address_or_mask] = int(value)
        else:
            mask_line = line.strip().split("mask = ")[1]
            _, or_mask = build_mask(mask_line)
            xs = len([c for c in mask_line if c == "X"])
            xindexes = {i for (i, c) in enumerate(list(mask_line)) if c == 'X'}
    return memory


def solve():
    if sys.argv[1] == 'part1':
        memory = part1_memory()
        return sum([p[1] for p in memory.items()])
    if sys.argv[1] == 'part2':
        memory = part2_memory()
        return sum([p[1] for p in memory.items()])


if __name__ == '__main__':
    print(solve())
