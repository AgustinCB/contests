use std::collections::HashMap;
use std::io::Stdin;
use std::io;


fn does_first_player_win(buckets: Vec<usize>, cache: &mut HashMap<Vec<usize>, bool>) -> bool {
    if buckets.contains(&0) {
        return does_first_player_win(buckets.into_iter().filter(|b| *b != 0).collect::<Vec<usize>>(), cache);
    }
    if buckets.len() == 0 {
        return false;
    }
    if buckets.len() == 1 {
        return buckets[0] % 3 != 0;
    }
    if buckets.len() == 2 {
        if buckets[0] % 3 == 0 && buckets[1] % 3 == 0 {
            return false;
        } else if buckets[0] % 3 == 0 || buckets[0] % 3 == 0 {
            return true;
        } else if (buckets[0] == 1 && buckets[1] == 2) || (buckets[1] == 1 && buckets[0] == 2) {
            return true;
        } else if buckets[0] == buckets[1] {
            return false;
        }
    }
    if cache.contains_key(&buckets) {
        return *cache.get(&buckets).unwrap();
    }
    if buckets.len() == 3 {
        // Do something here regarding powers of two
    }
    let mut counter = HashMap::new();
    for b in buckets.iter() {
        if !counter.contains_key(b) {
            counter.insert(*b, 1);
        }
        *counter.get_mut(b).unwrap() += 1;
    }
    for (bucket, quantity) in counter.into_iter() {
        let mut other_buckets = buckets.iter().cloned().filter(|b| *b != bucket).collect::<Vec<usize>>();
        for _ in 0..(quantity-1) {
            other_buckets.push(bucket);
        }
        let mut closest_power_of_two = bucket;
        while (closest_power_of_two & closest_power_of_two - 1) > 0 {
            closest_power_of_two = closest_power_of_two & closest_power_of_two - 1
        }
        for p in 0..(closest_power_of_two + 1) {
            other_buckets.push(bucket - 2usize.pow(p as _) as usize);
            if !does_first_player_win(other_buckets.clone(), cache) {
                cache.insert(other_buckets, true);
                return true;
            }
        }
    }
    cache.insert(buckets, false);
    false
}

fn read_line(stdin: &mut Stdin) -> io::Result<String> {
    let mut buffer = String::new();
    stdin.read_line(&mut buffer)?;
    Ok(buffer.trim_end().to_owned())
}

fn main() -> io::Result<()> {
    let mut stdin = io::stdin();
    let tests = read_line(&mut stdin)?.parse::<usize>().unwrap();
    let mut cache = HashMap::new();
    for test in 0..tests {
        read_line(&mut stdin)?;
        let buckets: Vec<usize> = read_line(&mut stdin)?.split(" ").map(|s| s.parse::<usize>().unwrap()).collect();
        println!("Case #{}: {}", test + 1, if does_first_player_win(buckets, &mut cache) {
            "Edu"
        } else {
            "Alberto"
        });
    }
    Ok(())
}
