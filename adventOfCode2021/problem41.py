import sys
from typing import Tuple


def who_wins(player1_position: int, player2_position: int) -> Tuple[int, int]:
    player1_score = 0
    player2_score = 0
    player1_turn = True
    rolls = 0
    current_increase_score = 6
    while player1_score < 1000 and player2_score < 1000:
        if player1_turn:
            player1_position += current_increase_score
            if player1_position > 10:
                player1_position = player1_position % 10
            player1_score += player1_position
        else:
            player2_position += current_increase_score
            if player2_position > 10:
                player2_position = player2_position % 10
            player2_score += player2_position
        current_increase_score -= 1
        if current_increase_score == -1:
            current_increase_score = 9
        player1_turn = not player1_turn
        rolls += 3
    return player2_score if player1_score > player2_score else player1_score, rolls


def solve():
    player1_position = int(sys.stdin.readline().strip().replace("Player 1 starting position: ", ""))
    player2_position = int(sys.stdin.readline().strip().replace("Player 2 starting position: ", ""))
    looser_score, rolls = who_wins(player1_position, player2_position)
    return looser_score * rolls


if __name__ == '__main__':
    print(solve())
