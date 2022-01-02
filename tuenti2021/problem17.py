from collections import Counter
import math
import sys


cache = {}


def does_first_player_win_with_modulo(buckets: [int]) -> bool:
    buckets = [b % 3 for b in buckets if b % 3 != 0]
    if len(buckets) == 0:
        return False
    if len(buckets) == 1:
        return True
    if len(buckets) == 2:
        buckets = sorted(buckets)
        if buckets == [1, 2]:
            return True
        if buckets == [2, 2]:
            return False
        if buckets == [1, 1]:
            return False
    cache_key = ",".join([str(c) for c in sorted(buckets)])
    if cache_key in cache:
        return cache[cache_key]
    n_buckets = Counter(buckets)
    for (bucket, quantity) in n_buckets.items():
        other_buckets = [b for b in buckets if b != bucket]
        for _ in range(quantity - 1):
            other_buckets.append(bucket)
        for p in range(math.floor(math.log(bucket, 2)) + 1):
            new_buckets = [bucket - 2 ** p]
            if not does_first_player_win_with_modulo(new_buckets + other_buckets):
                cache[cache_key] = True
                return True
    cache[cache_key] = False
    return False


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        int(sys.stdin.readline().strip())
        buckets = [int(c) for c in sys.stdin.readline().strip().split(' ')]
        if does_first_player_win_with_modulo(buckets):
            won = "Edu"
        else:
            won = "Alberto"
        print("Case #{}: {}".format(test + 1, won))


if __name__ == '__main__':
    solve()

