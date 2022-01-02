use std::collections::HashMap;
use std::io;
use std::io::Stdin;

fn combinations_from(from_bit: usize, so_far: usize, unavailable: usize, max_bits: usize) -> Vec<Vec<usize>> {
    if from_bit == max_bits {
        return vec![vec![aim - so_far]];
    }
    let mut result = vec![];
    for i in 0..(2usize.pow(from_bit as _ + 1) + unavailable + 2
    result
}

/*
def all_possible_codes_per_bit_count(max_bits: int, aim: int) -> [[int]]:
    def combinations_from(from_bit: int, so_far: 0, unavailable: int) -> [[int]]:
        for i in range(2 ** from_bit + 1 - unavailable):
            future_unavailable = i * 2 + unavailable * 2
            if 2 ** max_bits - future_unavailable < aim - so_far - i:
                break
            for permutation in combinations_from(from_bit + 1, so_far + i, i * 2 + unavailable * 2):
                result.append([i] + permutation)

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
            bits = get_bits_for_codes_per_bit_count(codes_per_bit_count, ops_distribution)
            possibilities[bits].append(max_bits - min_bits)

    min_possibility = min(possibilities.keys())
    min_diff = min(possibilities[min_possibility])
    return min_possibility + 2 * total_ops, min_diff
*/

fn get_optimal_compression(ops: Vec<usize>) -> (usize, usize) {
    (0, 0)
}

fn read_line(stdin: &mut Stdin) -> io::Result<String> {
    let mut buffer = String::new();
    stdin.read_line(&mut buffer)?;
    Ok(buffer.trim_end().to_owned())
}

fn main() -> io::Result<()> {
    let mut stdin = io::stdin();
    let tests = read_line(&mut stdin)?.parse::<usize>().unwrap();
    for test in 0..tests {
        let n_ops = read_line(&mut stdin)?.parse::<usize>().unwrap();
        let mut ops_distribution: HashMap<String, usize> = HashMap::new();
        for _ in 0..n_ops {
            let op = read_line(&mut stdin)?.split(" ").next().unwrap().to_string();
            if !ops_distribution.contains_key(&op) {
                ops_distribution.insert(op.clone(), 0usize);
            }
            *ops_distribution.get_mut(&op).unwrap() += 1;
        }
        let mut ops = ops_distribution.values().cloned().collect::<Vec<usize>>();
        ops.sort();
        ops.reverse();
        let (bits, diff) = get_optimal_compression(ops);
        println!("Case #{}: {}, {}", test + 1, bits, diff);
    }
    Ok(())
}
