#![feature(iter_intersperse)]
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::io::Stdin;
use std::io;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

pub fn solve_problem(input: &String, thread_count: usize) -> Option<Vec<HashMap<char, u8>>> {
    let equation = Arc::new(Equation::new(input));
    let answers = Arc::new(Mutex::new(Vec::new()));

    let perms: Vec<Vec<u8>> = PermGenerator::new(equation.vars.len())
        .filter(|perm| valid_perm(perm, &equation.first_vars_index))
        .collect();
    let mut perms_peekable_iter = perms.into_iter().peekable();
    let size = perms_peekable_iter.len() / thread_count;

    let mut handles = Vec::new();

    while perms_peekable_iter.peek().is_some() {
        let perms_chunk: Vec<_> = perms_peekable_iter.by_ref().take(size).collect();
        let equation = Arc::clone(&equation);
        let answers = Arc::clone(&answers);
        let handle = thread::spawn(move || {
            let mut var_value: HashMap<char, u8> = HashMap::new();
            for perm in perms_chunk {
                for (var, value) in equation.vars.iter().zip(perm.iter()) {
                    var_value.insert(*var, *value);
                }

                if !equation.starts_with_zero(&var_value) {
                    if let 1 = equation.eval(&var_value) {
                        answers.lock().unwrap().push(var_value.clone());
                    }
                }
            }
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let x: Vec<HashMap<char, u8>> = answers.lock().unwrap().to_vec();

    if x.len() == 0 {
        None
    }
    else {
        Some(x)
    }
}

fn valid_perm(perm: &Vec<u8>, first_vars: &Vec<usize>) -> bool {
    for var in first_vars {
        if perm[*var] == 0 {
            return false;
        }
    }
    true
}

struct PermGenerator {
    pool: [u8; 10],
    indicies: [u8; 10],
    cycles: Vec<usize>,
    letter_count: usize,
}

impl PermGenerator {
    fn new(letter_count: usize) -> PermGenerator {
        let mut cycles: Vec<usize> = Vec::new();
        for i in (10 - letter_count + 1..11).rev() {
            cycles.push(i)
        }
        PermGenerator {
            pool: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            indicies: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            cycles: cycles,
            letter_count: letter_count,
        }
    }
}

impl Iterator for PermGenerator {
    type Item = Vec<u8>;

    fn next(&mut self) -> Option<Self::Item> {
        for i in (0..self.letter_count).rev() {
            self.cycles[i] -= 1;
            if self.cycles[i] == 0 {
                let x = self.indicies;
                let mut j = i;
                for h in i + 1..10 {
                    self.indicies[j] = x[h];
                    j += 1;
                }
                for h in i..i + 1 {
                    self.indicies[j] = x[h];
                    j += 1;
                }

                self.cycles[i] = 10 - i;
            } else {
                let j = self.cycles[i];
                self.indicies.swap(i, 10 - j);
                let v: Vec<u8> = (0..self.letter_count)
                    .map(|i| self.pool[self.indicies[i] as usize])
                    .collect();
                return Some(v);
            }
        }
        None
    }
}

struct Equation {
    postfix: VecDeque<String>,
    vars: Vec<char>,
    first_vars_index: Vec<usize>,
}

impl Equation {
    fn new(infix: &String) -> Equation {
        let mut operator_precedence = HashMap::new();
        operator_precedence.insert('+', 2);
        operator_precedence.insert('-', 2);
        operator_precedence.insert('/', 3);
        operator_precedence.insert('*', 3);
        operator_precedence.insert('=', 1);

        let letters = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        ];
        let mut variables = HashSet::new();
        let mut first_vars = HashSet::new();
        let mut output_queue = VecDeque::new();

        let mut operator_stack = Vec::new();
        let mut current_word = String::new(); //Placeholder var to combine chars that form a single "number"

        for token in infix.chars() {
            if letters.contains(&token) || token.is_ascii_digit() {
                if !token.is_ascii_digit() {
                    variables.insert(token);
                }
                current_word.push(token);
                continue;
            } else {
                if current_word.len() != 0 {
                    first_vars.insert(current_word.chars().nth(0).unwrap());
                    output_queue.push_back(current_word);
                    current_word = String::new();
                }
            }

            if operator_precedence.contains_key(&token) {
                let precedence = operator_precedence[&token];
                while operator_stack.len() != 0
                    && operator_precedence.contains_key(operator_stack.last().unwrap())
                    && operator_precedence[operator_stack.last().unwrap()] > precedence
                {
                    output_queue.push_back(operator_stack.pop().unwrap().to_string());
                }
                operator_stack.push(token);
            } else if token == '(' {
                operator_stack.push(token);
            } else if token == ')' {
                while *operator_stack.last().unwrap() != '(' {
                    output_queue.push_back(operator_stack.pop().unwrap().to_string());
                }
                operator_stack.pop();
            }
        }

        if current_word.len() != 0 {
            output_queue.push_back(current_word);
        }

        for _i in 0..operator_stack.len() {
            output_queue.push_back(operator_stack.pop().unwrap().to_string());
        }

        let vars: Vec<char> = variables.into_iter().collect();
        let mut first_vars_index: Vec<usize> = vec![];
        for (index, var) in vars.iter().enumerate() {
            if first_vars.contains(var) {
                first_vars_index.push(index);
            }
        }

        // eprintln!("{:?} {:?}", output_queue, vars);
        Equation {
            postfix: output_queue,
            vars: vars,
            first_vars_index: first_vars_index,
        }
    }

    fn eval(&self, var_value: &HashMap<char, u8>) -> u64 {
        let mut postfix_copy = self.postfix.clone();

        let mut calc_stack: Vec<f64> = vec![];
        loop {
            let token = match postfix_copy.pop_front() {
                Some(n) => n,
                None => break,
            };
            let new_stack_value = match token.as_str() {
                "+" => {
                    let b = calc_stack.pop().unwrap();
                    let a = calc_stack.pop().unwrap();
                    (a + b) as f64
                }
                "-" => {
                    let b = calc_stack.pop().unwrap();
                    let a = calc_stack.pop().unwrap();
                    (a - b) as f64
                }
                "*" => {
                    let b = calc_stack.pop().unwrap();
                    let a = calc_stack.pop().unwrap();
                    (a * b) as f64
                }
                "/" => {
                    let b = calc_stack.pop().unwrap() as f64;
                    let a = calc_stack.pop().unwrap() as f64;
                    a / b
                }
                "=" => {
                    let b = calc_stack.pop().unwrap();
                    let a = calc_stack.pop().unwrap();
                    (if a == b && b.ceil() == b.floor() && a.ceil() == a.floor() {
                        1
                    } else {
                        0
                    }) as f64
                }
                _ => {
                    let mut value = 0;
                    for (idx, var) in token.chars().rev().enumerate() {
                        let next_char = var_value.get(&var).cloned().unwrap_or_else(|| var.to_digit(10).unwrap() as u8);
                        value += 10_u64.pow(idx as u32) * next_char as u64;
                    }
                    value as f64
                }
            };
            calc_stack.push(new_stack_value);
        }
        calc_stack[0] as u64
    }

    fn starts_with_zero(&self, var_value: &HashMap<char, u8>) -> bool {
        for i in self.postfix.iter() {
            let first_digit = i.chars().next().unwrap();
            if first_digit.is_alphabetic() && *var_value.get(&first_digit).unwrap() == 0 {
                return true
            }
        }
        false
    }
}

fn read_line(stdin: &mut Stdin) -> io::Result<String> {
    let mut buffer = String::new();
    stdin.read_line(&mut buffer)?;
    Ok(buffer.trim_end().to_owned())
}

fn solution_to_string(problem: &str, solution: Option<Vec<HashMap<char, u8>>>) -> String {
    match solution {
        Some(answers) => {
            let mut answer_strings: Vec<String> = answers.into_iter().map(|answer| {
                let mut answer_string = String::new();
                for input_char in problem.chars() {
                    answer_string.push_str(&answer.get(&input_char).map(|c| c.to_string()).unwrap_or(input_char.to_string()));
                }
                answer_string
            }).collect();
            answer_strings.sort();
            answer_strings.into_iter()
                .intersperse(";".to_string())
                .collect()
        },
        None => "IMPOSSIBLE".to_owned(),
    }
}

fn main() -> io::Result<()> {
    let mut stdin = io::stdin();
    let tests = read_line(&mut stdin)?.parse::<usize>().unwrap();
    for i in 1..tests+1 {
        let line = read_line(&mut stdin)?;
        let solution = solve_problem(&line, 4);
        println!("Case #{}: {}", i, solution_to_string(&line, solution));
    }
    Ok(())
}
