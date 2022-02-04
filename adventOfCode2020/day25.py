import sys


def find_loop_size(public_key: int, subject: int = 7, magic_number: int = 20201227) -> int:
    value = 1
    iterations = 0
    while value != public_key:
        value *= subject
        value %= magic_number
        iterations += 1
    return iterations


def transform_subject(subject: int, loop_size: int, magic_number: int = 20201227) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= magic_number
    return value


def solve():
    card_public_key = int(sys.stdin.readline().strip())
    door_public_key = int(sys.stdin.readline().strip())
    if sys.argv[1] == 'part1':
        loops = find_loop_size(card_public_key)
        return transform_subject(door_public_key, loops)
    if sys.argv[1] == 'part2':
        pass


if __name__ == '__main__':
    print(solve())
