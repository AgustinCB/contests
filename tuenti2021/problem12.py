from collections import defaultdict
import heapq
import sys
from typing import Dict, List


def a_start(transactions: Dict[str, Dict[str, int]]) -> Dict[str, str]:
    goal = "END_BTC"
    starting_point = "START_BTC"
    vset = [(0, starting_point)]
    heapq.heapify(vset)
    dist = {starting_point: 0}
    fscore = {starting_point: 0}
    prev = {}
    print("START A STAR GOAL {}".format(goal))
    i = 0
    while vset:
        min_vertex = heapq.heappop(vset)[1]
        if min_vertex == goal:
            return prev
        if i % 1000 == 0:
            print("ITERATION {}: VSET SIZE {} DIST SIZE {} CURRENT {}".format(i, len(vset), len(dist), min_vertex))
        i += 1
        for next_coin in transactions[min_vertex].keys():
            alt = dist[min_vertex] + 1
            if next_coin not in dist or alt < dist[next_coin]:
                dist[next_coin] = alt
                prev[next_coin] = min_vertex
                fscore[next_coin] = alt - transactions[min_vertex][next_coin]
                if next_coin not in [v[1] for v in vset]:
                    heapq.heappush(vset, (fscore[next_coin], next_coin))
    return {}


def parse_transactions():
    sites = int(sys.stdin.readline().strip())
    transactions = defaultdict(lambda: defaultdict(int))
    for _ in range(sites):
        site_transactions = int(sys.stdin.readline().strip().split(" ")[1])
        for _ in range(site_transactions):
            from_coin, amount, to_coin = sys.stdin.readline().strip().split("-")
            if from_coin == "BTC":
                from_coin = "START_BTC"
            if to_coin == "BTC":
                to_coin = "END_BTC"
            amount = int(amount)
            if transactions[from_coin][to_coin] < amount:
                transactions[from_coin][to_coin] = amount
    return transactions


def get_btcs(transactions: Dict[str, Dict[str, int]], prev: Dict[str, str]):
    if "END_BTC" not in prev:
        return 1
    current = "END_BTC"
    coins = 1
    path = []
    while current != "START_BTC":
        path.append(current)
        current = prev[current]

    for p in reversed(path):
        coins *= transactions[current][p]
        current = p
    return coins if coins > 1 else 1


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        transactions = parse_transactions()
        print("Case #{}: {}".format(test + 1, get_btcs(transactions, a_start(transactions))))


if __name__ == '__main__':
    solve()

