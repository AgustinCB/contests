import socket
from collections import defaultdict
from socket import SocketType
from typing import Optional

HOST = 'codechallenge-daemons.0x14.net'
PORT = 7162


def is_prime(n: int) -> bool:
    for i in range(2, n//2+1):
        if n % i == 0:
            return False
    return True


def get_number_of_non_prime(n: int) -> int:
    non_prime = 0
    for i in range(n+1):
        if not is_prime(i):
            non_prime += 1
    return non_prime


def send_message(s: socket.socket, message: str) -> str:
    print(message)
    s.sendall(bytes(message, "utf-8"))
    result = s.recv(4096).decode("utf-8").strip()
    print(result)
    return result


cache = defaultdict(int)
def dry_gcd(problem: [int], x: int, y: int) -> int:
    if x < y:
        return dry_gcd(problem, y, x)
    cache["{}x{}".format(x, y)] += 1
    if problem[x - 1] % problem[y - 1] == 0:
        return problem[y - 1]
    for i in reversed(list(range(1, min(problem[x - 1] // 2 + 1, problem[y - 1] // 2 + 1)))):
        if problem[x - 1] % i == 0 and problem[y - 1] % i == 0:
            return i
    return 1


def gcd(s: socket.socket, x: int, y: int) -> int:
    result = send_message(s, "? {} {}\n".format(x, y))
    return int(result)


def dry_won(problem: [int], indexes: [int]) -> bool:
    expected = [i + 1 for (i, n) in enumerate(problem) if is_prime(n)]
    print("PROBLEM  ", problem)
    print("EXPECTED ", expected, len(expected))
    print("BUT GOT  ", indexes, len(indexes))
    return expected == indexes


def won(s: socket.socket, indexes: [int]) -> bool:
    result = send_message(s, "! {}\n".format(" ".join([str(i) for i in indexes])))
    return result.startswith("Congratulations")


def solve_riddle(s: Optional[SocketType]) -> bool:
    problem = None
    if s is None:
        problem = [76, 69, 5, 39, 85, 73, 48, 65, 53, 3, 64, 28, 27, 54, 30, 68, 51, 80, 33, 42, 92, 89, 8, 57, 83, 14,
                   47, 84, 60, 12, 70, 61, 37, 13, 24, 77, 62, 72, 32, 98, 10, 22, 38, 36, 23, 93, 78, 81, 6, 7, 1, 95,
                   26, 90, 67, 91, 9, 25, 55, 45, 71, 63, 40, 31, 99, 100, 4, 44, 19, 59, 94, 29, 82, 66, 52, 15, 87,
                   79, 20, 11, 56, 35, 2, 41, 21, 50, 46, 88, 49, 43, 34, 86, 75, 74, 58, 17, 18, 16, 96, 97]
    if s is not None:
        n, q = [int(c) for c in s.recv(4096).decode("utf-8").strip().split(" ")]
    else:
        n, q = 100, 1500
    non_primes = get_number_of_non_prime(n)
    checking1 = 1
    checking2 = 2
    non_primes_found = set()
    divisors_of_index = [{1} for _ in range(n)]
    checked_with = [{i + 1} for i in range(n)]
    indexes = {i for i in range(1, n + 1)}
    asked = 0
    confirmed_primes = {}
    indexes_per_divisor = defaultdict(list)
    while len(non_primes_found) < non_primes and checking1 < n and checking2 <= n:
        if s is not None:
            result = gcd(s, checking1, checking2)
        else:
            result = dry_gcd(problem, checking1, checking2)
        asked += 1
        checked_with[checking1 - 1].add(checking2)
        checked_with[checking2 - 1].add(checking1)
        divisors_of_index[checking1 - 1].add(result)
        divisors_of_index[checking2 - 1].add(result)
        indexes_per_divisor[result].append(checking1)
        indexes_per_divisor[result].append(checking2)
        if not is_prime(result):
            non_primes_found.union({checking1, checking2})
            checking1 += 1
            checking2 = checking1
        else:
            if len(divisors_of_index[checking2 - 1]) > 2:
                non_primes_found.add(checking2)
            if len(divisors_of_index[checking1 - 1]) > 2:
                non_primes_found.add(checking1)
                checking1 += 1
                while checking1 < 101 and (checking1 in non_primes_found or checking1 in checked_with[checking2 - 1]):
                    checking1 += 1
        checking2 += 1
        while checking2 < 101 and (checking2 in non_primes_found or checking2 in checked_with[checking1 - 1]):
            checking2 += 1
        if checking2 == checking1:
            checking2 += 1
        if checking2 > n:
            checking1 += 1
            checking2 = checking1 + 1
            while checking1 < 101 and checking2 < 101 and (checking1 in non_primes_found or checking1 in checked_with[checking2 - 1]):
                checking1 += 1
                checking2 = checking1 + 1
    for i in indexes - non_primes_found:
        if len(divisors_of_index[i - 1]) > 2 or any([not is_prime(d) for d in divisors_of_index[i - 1]]):
            non_primes_found.add(i)
    if len(non_primes_found) < non_primes:
        for i in indexes - non_primes_found:
            if len(checked_with[i - 1]) == 100 and len(divisors_of_index[i - 1]) == 2:
                confirmed_primes[sorted(list(divisors_of_index[i - 1]))[-1]] = i
        def another_try(prime, asked):
            big_primes = set(
                [i + 1 for i in range(n) if len(checked_with[i]) == 100 and len(divisors_of_index[i]) == 1])
            unclear_indexes = sorted(list(indexes - non_primes_found - big_primes - set(confirmed_primes.values())),
                                      key=lambda i: len(checked_with[i-1]), reverse=True)
            prime_candidates = set([c for c in indexes_per_divisor[prime] if c not in non_primes_found])
            to_try = unclear_indexes if len(prime_candidates) == 0 else prime_candidates.intersection(unclear_indexes)
            print("BEFORE TRY FOR ", prime, prime_candidates, to_try, asked, non_primes_found, confirmed_primes,
                  len(non_primes_found), [(i, len(checked_with[i-1])) for i in to_try])
            for i in to_try:
                for j in indexes - checked_with[i - 1]:
                    if asked == q - 1:
                        break
                    if s is not None:
                        result = gcd(s, i, j)
                    else:
                        result = dry_gcd(problem, i, j)
                    asked += 1
                    checked_with[i - 1].add(j)
                    checked_with[j - 1].add(i)
                    if result > 1:
                        divisors_of_index[i - 1].add(result)
                        divisors_of_index[j - 1].add(result)
                        indexes_per_divisor[result].append(checking1)
                        indexes_per_divisor[result].append(checking2)
                        if not is_prime(result):
                            non_primes_found.add(i)
                            non_primes_found.add(j)
                            break
                        if len(divisors_of_index[j - 1]) > 2:
                            non_primes_found.add(j)
                        if len(divisors_of_index[i - 1]) > 2:
                            non_primes_found.add(i)
                            break
                if len(checked_with[i - 1]) == 100 and i not in non_primes_found:
                    confirmed_primes[sorted(list(divisors_of_index[i - 1]))[-1]] = i
                if len(non_primes_found) == non_primes:
                    break
                if asked == q:
                    break
            return asked
        asked = another_try(2, asked)
        asked = another_try(3, asked)
        asked = another_try(5, asked)
        asked = another_try(7, asked)
        asked = another_try(11, asked)
        big_primes = set([i+1 for i in range(n) if len(checked_with[i]) == 100 and len(divisors_of_index[i]) == 1])
        for i in indexes - non_primes_found:
            if len(checked_with[i - 1]) == 100 and len(divisors_of_index[i - 1]) == 2:
                confirmed_primes[sorted(list(divisors_of_index[i - 1]))[-1]] = i
        print("AFTER LAST TRY", asked, confirmed_primes, len(non_primes_found), non_primes_found, set(cache.values()))
        there_are_changes = True
        while there_are_changes:
            there_are_changes = False
            for i in [i for i in indexes - non_primes_found if len(checked_with[i - 1]) < 100]:
                if len(divisors_of_index[i - 1]) > 1:
                    divisor = sorted(list(divisors_of_index[i - 1]))[-1]
                    if divisor in confirmed_primes and i not in non_primes_found and confirmed_primes[divisor] != i:
                        non_primes_found.add(i)
                        there_are_changes = True
                    elif i not in confirmed_primes.values():
                        add = all([d in confirmed_primes for d in range(2, n // divisor + 1) if is_prime(d)])
                        if add:
                            confirmed_primes[divisor] = i
                            there_are_changes = True
            confirmed_prime_indexes = set(confirmed_primes.values())
            unclear_indexes = sorted(list(indexes - non_primes_found - confirmed_prime_indexes - big_primes),
                                     key=lambda i: len(checked_with[i - 1]))
            for unclear_index in unclear_indexes:
                if len(divisors_of_index[unclear_index - 1]) == 2:
                    divisor = sorted(list(divisors_of_index[unclear_index - 1]))[-1]
                    if is_prime(divisor) and divisor not in confirmed_primes and \
                            len(indexes_per_divisor[divisor]) == (n // divisor):
                        if all([rest not in unclear_indexes for rest in set(indexes_per_divisor[divisor]) - {unclear_index}]):
                            confirmed_primes[divisor] = unclear_index
                            there_are_changes = True
        print("NOT FOUND AFTER BEING SMART ", len(non_primes_found), non_primes_found, confirmed_primes)
        confirmed_prime_indexes = set(confirmed_primes.values())
        unclear_indexes = sorted(list(indexes - non_primes_found - confirmed_prime_indexes - big_primes),
                                  key=lambda i: len(checked_with[i - 1]))
        print([(snp, divisors_of_index[snp-1], len(checked_with[snp-1])) for snp in unclear_indexes])
        pending = non_primes - len(non_primes_found)
        for i in range(pending):
            non_primes_found.add(unclear_indexes[i])
    prime_indexes = indexes - non_primes_found
    if s is not None:
        return won(s, sorted(list(prime_indexes)))
    else:
        return dry_won(problem, sorted(list(prime_indexes)))


def get_password():
    end = False
    while not end:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            end = solve_riddle(s)


def solve():
    # get_password()
    solve_riddle(None)


if __name__ == '__main__':
    solve()

