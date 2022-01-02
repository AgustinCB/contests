import sys

from typing import Set


def parse_digits_sequence(sequence: str):
    return ["".join(sorted(s)) for s in sequence.strip().split(" ")]


def parse_input_line(input_line: str):
    (input_sequence, output_sequence) = input_line.split("|")
    return parse_digits_sequence(input_sequence), parse_digits_sequence(output_sequence)


def add_sequence_to_dictionary(dictionary: [set], sequence: str):
    if len(sequence) == 2:
        dictionary[1].add(sequence)
    if len(sequence) == 3:
        dictionary[7].add(sequence)
    if len(sequence) == 4:
        dictionary[4].add(sequence)
    if len(sequence) == 5:
        dictionary[2].add(sequence)
        dictionary[3].add(sequence)
        dictionary[5].add(sequence)
    if len(sequence) == 6:
        dictionary[0].add(sequence)
        dictionary[6].add(sequence)
        dictionary[9].add(sequence)
    if len(sequence) == 7:
        dictionary[8].add(sequence)


def build_candidates_dictionaries(input: [([str], [str])]):
    dictionaries = []
    for (input_sequence, output_sequence) in input:
        dictionary = [set() for _ in range(10)]
        for sequence in input_sequence + output_sequence:
            add_sequence_to_dictionary(dictionary, sequence)
        dictionaries.append(dictionary)
    return dictionaries


def detect_a(candidates: [Set[str]]):
    seven_one_diff = set(list(candidates[7])[0]) - set(list(candidates[1])[0])
    return list(seven_one_diff)[0]


def detect_d(candidates: [Set[str]]):
    final_set = set(list(candidates[4])[0])
    for s in candidates[2]:
        final_set = final_set.intersection(set(s))
    return list(final_set)[0]


def detect_b_and_e(candidates: [Set[str]], mapping: [str]):
    zero_pos = [set(c) for c in candidates[0]]
    common_in_zero = zero_pos[0]
    for z in zero_pos:
        common_in_zero = common_in_zero.intersection(z)
    one_pos = set(list(candidates[1])[0])
    left_arm = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    left_arm = left_arm - one_pos - {mapping[0], mapping[3], mapping[6]}
    e_set = left_arm - common_in_zero
    b_set = left_arm - e_set
    return list(b_set)[0], list(e_set)[0]


def detect_g(candidates: [Set[str]], mapping: [str]):
    final_set = set(list(candidates[2])[0])
    for s in candidates[2]:
        final_set = final_set.intersection(set(s))
    final_set.remove(mapping[0])
    final_set.remove(mapping[3])
    return list(final_set)[0]


def detect_c_and_f(candidates: [Set[str]], mapping: [str]):
    zero_pos = [set(c) for c in candidates[0]]
    common_in_zero = zero_pos[0]
    for z in zero_pos:
        common_in_zero = common_in_zero.intersection(z)
    right_arm = set(list(candidates[1])[0])
    c_set = right_arm - common_in_zero
    f_set = right_arm - c_set
    return list(c_set)[0], list(f_set)[0]


def candidates_to_mapping(candidates: [Set[str]]):
    mapping = [None for _ in range(7)]
    mapping[0] = detect_a(candidates)
    mapping[3] = detect_d(candidates)
    mapping[6] = detect_g(candidates, mapping)
    (b, e) = detect_b_and_e(candidates, mapping)
    mapping[2] = b
    mapping[4] = e
    (c, f) = detect_c_and_f(candidates, mapping)
    mapping[1] = c
    mapping[5] = f
    zero = "".join(sorted([mapping[0], mapping[1], mapping[2], mapping[4], mapping[5], mapping[6]]))
    one = "".join(sorted([mapping[1], mapping[5]]))
    two = "".join(sorted([mapping[0], mapping[1], mapping[3], mapping[4], mapping[6]]))
    three = "".join(sorted([mapping[0], mapping[1], mapping[3], mapping[5], mapping[6]]))
    four = "".join(sorted([mapping[1], mapping[2], mapping[3], mapping[5]]))
    five = "".join(sorted([mapping[0], mapping[2], mapping[3], mapping[5], mapping[6]]))
    six = "".join(sorted([mapping[0], mapping[2], mapping[3], mapping[4], mapping[5], mapping[6]]))
    seven = "".join(sorted([mapping[0], mapping[1], mapping[5]]))
    eight = "".join(sorted([mapping[0], mapping[1], mapping[2], mapping[3], mapping[4], mapping[5], mapping[6]]))
    nine = "".join(sorted([mapping[0], mapping[1], mapping[2], mapping[3], mapping[5], mapping[6]]))
    numbers = {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9
    }
    return numbers



def solve():
    io_pairs = []
    for line in sys.stdin:
        io_pairs.append(parse_input_line(line))

    candidates = build_candidates_dictionaries(io_pairs)
    total = 0
    for ((_, output_sequence), candidate) in zip(io_pairs, candidates):
        mapping = candidates_to_mapping(candidate)
        n = ""
        for sequence in output_sequence:
            n += str(mapping[sequence])
        total += int(n)
    return total


if __name__ == '__main__':
    print(solve())
