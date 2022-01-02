import sys


def parse_digits_sequence(sequence: str):
    return sequence.strip().split(" ")


def parse_input_line(input_line: str):
    (input_sequence, output_sequence) = input_line.split("|")
    return parse_digits_sequence(input_sequence), parse_digits_sequence(output_sequence)


def solve():
    io_pairs = []
    for line in sys.stdin:
        io_pairs.append(parse_input_line(line))

    counter = 0
    for (_, output_sequence) in io_pairs:
        for output_number in output_sequence:
            if len(output_number) in [2, 3, 4, 7]:
                counter += 1
    return counter


if __name__ == '__main__':
    print(solve())
