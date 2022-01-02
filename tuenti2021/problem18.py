from collections import Counter, defaultdict
import math
import sys
from typing import Dict, Tuple, List


def all_possible_codes_per_bit_count(max_bits: int, aim: int) -> [[int]]:
    def combinations_from(from_bit: int, so_far: 0, unavailable: int) -> [[int]]:
        if from_bit == max_bits:
            return [[aim - so_far]]
        result = []
        for i in range(2 ** from_bit + 1 - unavailable):
            future_unavailable = i * 2 + unavailable * 2
            if 2 ** max_bits - future_unavailable < aim - so_far - i:
                break
            for permutation in combinations_from(from_bit + 1, so_far + i, i * 2 + unavailable * 2):
                result.append([i] + permutation)
        return result

    return combinations_from(1, 0, 0)


def get_bits_for_codes_per_bit_count(codes_per_bit_count: [int], ops_distribution: Dict[str, int]) -> int:
    bits = 0
    current_step = 0
    for v in sorted(ops_distribution.values(), reverse=True):
        while codes_per_bit_count[current_step] == 0:
            current_step += 1
        bits += v * (current_step + 1)
        codes_per_bit_count[current_step] -= 1
    return bits


def get_optimal_compression_alternative(ops_distribution: Dict[str, int]) -> Tuple[int, int]:
    total_ops = sum(ops_distribution.values())
    if len(ops_distribution) < 3:
        min_possibility = sum(ops_distribution.values()) + 2 * total_ops
        return min_possibility, 0

    total_codes = len(ops_distribution)
    max_bits_necessary = math.ceil(math.log(total_codes, 2)) + 1
    possibilities = defaultdict(list)
    for codes_per_bit_count in all_possible_codes_per_bit_count(max_bits_necessary, total_codes):
        if sum(codes_per_bit_count) >= total_codes:
            non_zero_indexes = [i + 1 for (i, c) in enumerate(codes_per_bit_count) if c != 0]
            min_bits = non_zero_indexes[0]
            max_bits = non_zero_indexes[-1]
            bits = get_bits_for_codes_per_bit_count(codes_per_bit_count.copy(), ops_distribution)
            if bits == 363 - 2 * total_ops:
                print(codes_per_bit_count)
            possibilities[bits].append(max_bits - min_bits)

    min_possibility = min(possibilities.keys())
    min_diff = min(possibilities[min_possibility])
    return min_possibility + 2 * total_ops, min_diff


def calculate_bits(ops_distribution: List[int], ops_per_bits: List[int]) -> int:
    return sum([b * c for (b, c) in zip(ops_per_bits, ops_distribution)])


def get_optimal_bit_distribution(ops_distribution: List[int]) -> List[int]:
    if len(ops_distribution) == 0:
        return []
    if len(ops_distribution) == 1:
        return [1]
    if len(ops_distribution) == 2:
        return [1, 1]
    if len(ops_distribution) == 3:
        return [1, 2, 2]
    if len(ops_distribution) == 4:
        with_all_equals = [2, 2, 2, 2]
        without_all_equals = [1, 2, 3, 3]
        points_with_all_equals = calculate_bits(ops_distribution, with_all_equals)
        points_without_all_equals = calculate_bits(ops_distribution, without_all_equals)
        return with_all_equals if points_without_all_equals >= points_with_all_equals else without_all_equals

    prev_optimal_bit_distribution = get_optimal_bit_distribution(ops_distribution[:-1])
    changing_points = []
    current_bits = calculate_bits(ops_distribution[:-1], prev_optimal_bit_distribution)
    for i in range(len(prev_optimal_bit_distribution) - 1):
        if prev_optimal_bit_distribution[i] < prev_optimal_bit_distribution[i + 1]:
            new_bits = prev_optimal_bit_distribution.copy()
            new_bits[i] += 1
            new_bits.insert(i + 1, new_bits[i])
            new_number_of_bits = calculate_bits(ops_distribution, new_bits)
            adding_through_last_changing_point = new_number_of_bits - current_bits
            changing_points.append((adding_through_last_changing_point, i, new_bits))
    adding_through_last_index = ops_distribution[-2] + ops_distribution[-1] * (prev_optimal_bit_distribution[-1] + 1)
    last_index_bits = prev_optimal_bit_distribution.copy()
    last_index_bits[-1] += 1
    last_index_bits.append(last_index_bits[-1])
    changing_points.append((adding_through_last_index, len(prev_optimal_bit_distribution), last_index_bits))

    new_bits = sorted(changing_points)[0][2]

    return new_bits


def flatten_bit_distribution(ops_distribution: List[int], bits_distribution: List[int]) -> List[int]:
    buckets = sorted(dict(Counter(bits_distribution)).items())
    lingering = []
    taken_buckets = buckets[0][1]
    for (i, (k, q)) in enumerate(buckets[1:]):
        buckets_used = math.ceil(q / (2 ** (i + 1)))
        taken_buckets += buckets_used
        lingering.append(q % (2 ** (i + 1)))
    total_lingering = sum(lingering)
    if total_lingering == 0:
        return bits_distribution
    bucket_index = math.log(total_lingering, 2)
    new_bits = bits_distribution.copy()
    if bucket_index == math.floor(bucket_index):
        last_indexes = []
        for i in range(len(bits_distribution) - 1):
            if bits_distribution[i] < bits_distribution[i + 1]:
                last_indexes.append(i)
        last_indexes.append(len(bits_distribution) - 1)
        for (i, l) in enumerate(lingering):
            if l > 0:
                if i + 1 == bucket_index:
                    for offset in range(total_lingering):
                        new_bits.insert(last_indexes[i + 1], bits_distribution[last_indexes[i + 1]])
                else:
                    for _ in range(l):
                        new_bits.remove(bits_distribution[last_indexes[i + 1]])
        if calculate_bits(ops_distribution, new_bits) == calculate_bits(ops_distribution, bits_distribution):
            return new_bits
    return bits_distribution


def get_optimal_compression(ops_distribution: List[int]) -> Tuple[int, int]:
    optimal_bit_distribution = get_optimal_bit_distribution(ops_distribution)
    total_ops = sum(ops_distribution)
    optimal_bit_distribution = flatten_bit_distribution(ops_distribution, optimal_bit_distribution)
    return calculate_bits(ops_distribution, optimal_bit_distribution) + total_ops * 2,\
           optimal_bit_distribution[-1] - optimal_bit_distribution[0]


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        n_ops = int(sys.stdin.readline().strip())
        ops = [sys.stdin.readline().strip().split(" ")[0] for _ in range(n_ops)]
        ops_distribution = Counter(ops)
        bits, diff = get_optimal_compression(list(reversed(sorted(ops_distribution.values()))))
        # bits, diff = get_optimal_compression_alternative(ops_distribution)
        print("Case #{}: {}, {}".format(test + 1, bits, diff))


if __name__ == '__main__':
    solve()
