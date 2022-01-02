import sys

def solve():
    bits_info = [[set(), set()] for _ in range(13)]
    tree = [[] for _ in range(2**13 + 1)]
    numbers = []
    number_index = 0

    for line in sys.stdin:
        tree_index = 0
        for (index, bit) in enumerate(line):
            if bit == "\n":
                continue
            bit = int(bit)
            bits_info[index][bit].add(number_index)
            tree_index = tree_index * 2 + 1 + bit
            tree[tree_index].append(number_index)
        numbers.append(int(line, 2))
        number_index += 1
    oxygen = numbers[find_best_match(tree, lambda a, b: a >= b, len(numbers))]
    co2 = numbers[find_best_match(tree, lambda a, b: a < b, len(numbers))]
    return oxygen * co2


def find_best_match(tree, matcher, max_indexes):
    candidates = set(range(max_indexes))
    tree_position = 0
    while len(candidates) != 1:
        print(len(tree), tree_position, candidates)
        zeros_candidates = tree[tree_position * 2 + 1]
        ones_candidates = tree[tree_position * 2 + 2]
        ones_new_candidates = candidates.intersection(ones_candidates)
        zeros_new_candidates = candidates.intersection(zeros_candidates)
        if matcher(len(ones_new_candidates), len(zeros_new_candidates)):
            candidates = candidates.intersection(ones_new_candidates)
            tree_position = tree_position * 2 + 2
        else:
            candidates = candidates.intersection(zeros_new_candidates)
            tree_position = tree_position * 2 + 1
    return candidates.pop()


if __name__ == '__main__':
    print(solve())
