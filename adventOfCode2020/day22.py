import queue
from collections import deque
import sys
from itertools import islice
from typing import Tuple, Deque


def get_decks() -> Tuple[Deque[int], Deque[int]]:
    player1 = deque()
    player2 = deque()
    current_player = player1
    sys.stdin.readline()
    for line in sys.stdin:
        if line.strip() == "":
            sys.stdin.readline()
            current_player = player2
            continue
        current_player.append(int(line.strip()))
    return player1, player2


def play_game(player1: Deque[int], player2: Deque[int]) -> Deque[int]:
    while len(player1) > 0 and len(player2) > 0:
        player1_hand = player1.popleft()
        player2_hand = player2.popleft()
        if player1_hand > player2_hand:
            player1.append(player1_hand)
            player1.append(player2_hand)
        else:
            player2.append(player2_hand)
            player2.append(player1_hand)
    return player1 if len(player1) > 0 else player2


def play_recursive_game(player1: Deque[int], player2: Deque[int]) -> (bool, Deque[int]):
    plays_seen = set()
    while len(player1) > 0 and len(player2) > 0:
        game_configuration = (tuple(player1), tuple(player2))
        if game_configuration in plays_seen:
            return True, queue.Queue()
        plays_seen.add(game_configuration)
        player1_hand = player1.popleft()
        player2_hand = player2.popleft()
        player1_won = player1_hand > player2_hand
        if player1_hand <= len(player1) and player2_hand <= len(player2):
            player1_won, _ = play_recursive_game(deque(islice(player1, 0, player1_hand)), deque(islice(player2, 0, player2_hand)))
        if player1_won:
            player1.append(player1_hand)
            player1.append(player2_hand)
        else:
            player2.append(player2_hand)
            player2.append(player1_hand)
    player1_won = len(player1) > 0
    return player1_won, player1 if player1_won else player2


def calculate_score(winner: Deque[int]) -> int:
    index = len(winner)
    points = 0
    while not len(winner) == 0:
        points += index * winner.popleft()
        index -= 1
    return points


def solve():
    player1, player2 = get_decks()
    if sys.argv[1] == 'part1':
        return calculate_score(play_game(player1, player2))
    if sys.argv[1] == 'part2':
        _, winner = play_recursive_game(player1, player2)
        return calculate_score(winner)


if __name__ == '__main__':
    print(solve())
