import sys
from collections import defaultdict
from typing import Tuple, Dict, List


dies = [
    sum([1, 1, 1]),
    sum([1, 1, 2]),
    sum([1, 1, 3]),
    sum([1, 2, 1]),
    sum([1, 2, 2]),
    sum([1, 2, 3]),
    sum([1, 3, 1]),
    sum([1, 3, 2]),
    sum([1, 3, 3]),
    sum([2, 1, 1]),
    sum([2, 1, 2]),
    sum([2, 1, 3]),
    sum([2, 2, 1]),
    sum([2, 2, 2]),
    sum([2, 2, 3]),
    sum([2, 3, 1]),
    sum([2, 3, 2]),
    sum([2, 3, 3]),
    sum([3, 1, 1]),
    sum([3, 1, 2]),
    sum([3, 1, 3]),
    sum([3, 2, 1]),
    sum([3, 2, 2]),
    sum([3, 2, 3]),
    sum([3, 3, 1]),
    sum([3, 3, 2]),
    sum([3, 3, 3]),
]


def calculate_new_positions(
        games_statuses: Dict[Tuple[int, int, int, int], int], player1_turn: bool, limit: int
) -> Tuple[Dict[Tuple[int, int, int, int], int], int]:
    new_game_statuses = defaultdict(int)
    player1_victories = 0
    for roll in dies:
        for (x_position, x_points, y_position, y_points), quantity in games_statuses.items():
            if player1_turn:
                x_position += roll
                if x_position > 10:
                    x_position = x_position % 10
                x_points += x_position
                if x_points <= limit:
                    new_game_statuses[(x_position, x_points, y_position, y_points)] += quantity
                else:
                    player1_victories += quantity
            else:
                y_position += roll
                if y_position > 10:
                    y_position = y_position % 10
                y_points += y_position
                if y_points <= limit:
                    new_game_statuses[(x_position, x_points, y_position, y_points)] += quantity
    return new_game_statuses, player1_victories


def count_wins_per_timeline(player1_position: int, player2_position: int, limit: int) -> int:
    points = {(player1_position, 0, player2_position, 0): 1}
    player1_victories = 0
    player1_turn = True
    print(points, player1_victories, len(dies))
    while len(points) > 0:
        points, new_victories = calculate_new_positions(points, player1_turn, limit)
        player1_victories += new_victories
        player1_turn = not player1_turn
    print(points)
    return player1_victories


def solve():
    player1_position = int(sys.stdin.readline().strip().replace("Player 1 starting position: ", ""))
    player2_position = int(sys.stdin.readline().strip().replace("Player 2 starting position: ", ""))
    return count_wins_per_timeline(player1_position, player2_position, 20)


if __name__ == '__main__':
    print(solve())
