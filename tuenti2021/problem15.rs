use std::collections::HashMap;
use std::io::Stdin;
use std::io;
use std::thread;

const MOD: usize = 1e8 as usize + 7;
const THREADS: usize = 8;

fn read_line(stdin: &mut Stdin) -> io::Result<String> {
    let mut buffer = String::new();
    stdin.read_line(&mut buffer)?;
    Ok(buffer.trim_end().to_owned())
}

fn is_a_tuenti(n: usize) -> bool {
    let mut current = n;
    while current >= 20 {
        let tuenti_position = current % 100;
        if 20 <= tuenti_position && tuenti_position < 30 {
            return true;
        }
        current = (current - current % 1000) / 1000;
    }
    false
}

fn processes_factorial_minus_tuentis_subgroup(from_n: usize, subgroup: usize, n: usize) -> usize {
    ((from_n + 1 + subgroup * (n - (from_n - 1))  / THREADS)..std::cmp::min(n + 1, from_n + 1 + (subgroup + 1) * (n - (from_n - 1)) / THREADS))
        .filter(|n| !is_a_tuenti(*n))
        .fold(1, |acc, n| (acc * n) % MOD)
}

fn factorial_minus_tuentis(n: usize, last: Option<(usize, usize)>) -> usize {
    let mut handles = Vec::new();
    let (from_n, prev_result) = last.unwrap_or((0, 1));
    if prev_result == 0 {
        return 0;
    }
    for i in 0..THREADS {
        handles.push(thread::spawn(move || processes_factorial_minus_tuentis_subgroup(from_n, i, n)));
    }
    let mut res = prev_result;
    for handle in handles {
        res = (res * handle.join().unwrap()) % MOD;
    }
    res
}

fn main() -> io::Result<()> {
    let mut stdin = io::stdin();
    let tests = read_line(&mut stdin)?.parse::<usize>().unwrap();
    let mut last_n = None;
    for i in 1..tests+1 {
        let n = read_line(&mut stdin)?.parse::<usize>().unwrap();
        let result = factorial_minus_tuentis(n, last_n);
        match last_n {
            None => {
                last_n = Some((n, result));
            },
            Some((prev, _)) if prev < n => {
                last_n = Some((n, result));
            },
            _ => {},
        }
        println!("Case #{}: {}", i, result);
    }
    Ok(())
}
