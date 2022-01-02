import sys
from typing import Tuple


def decode_seat(seat: str) -> Tuple[int, int]:
    row = seat[:7].replace('F', '0').replace('B', '1')
    col = seat[-3:].replace('L', '0').replace('R', '1')
    return int(row, 2), int(col, 2)


def solve():
    seats = []
    for line in sys.stdin:
        seats.append(line.strip())

    if sys.argv[1] == 'part1':
        return max([r * 8 + c for (r, c) in [decode_seat(seat) for seat in seats]])
    if sys.argv[1] == 'part2':
        seats = sorted(decode_seat(seat) for seat in seats)
        for i in range(1, len(seats)):
            prev_r, prev_c = seats[i - 1]
            r, c = seats[i]
            expected_column = (c - 1) % 8
            if prev_c != expected_column:
                return r * 8 + (c - 1)
        return seats


if __name__ == '__main__':
    print(solve())
