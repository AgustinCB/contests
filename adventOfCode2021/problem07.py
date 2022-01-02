import sys


def solve():
    draws = None
    current_board = None
    boards = []
    board_columns = []
    board_rows = []
    for line in sys.stdin:
        if line.strip() != "":
            if draws is None:
                draws = [int(l) for l in line.split(',')]
            else:
                current_board.append([int(l) for l in ' '.join(line.split()).split(' ')])
        else:
            if current_board is not None:
                boards.append(current_board)
            current_board = []

    boards.append(current_board)

    for board in boards:
        transposed_board = list(map(list, zip(*board)))
        current_board = [set(row) for row in transposed_board]
        board_columns.append(current_board)


    for board in boards:
        current_board = [set(row) for row in board]
        board_rows.append(current_board)

    unmarked = None
    won = None
    for draw in draws:
        for board in board_rows:
            for row in board:
                if draw in row:
                    row.remove(draw)
                if len(row) == 0:
                    won = draw
                    unmarked = board
                    break
            if won is not None:
                break
        for board in board_columns:
            for row in board:
                if draw in row:
                    row.remove(draw)
                if len(row) == 0:
                    won = draw
                    unmarked = board
                    break
            if won is not None:
                break
        if won is not None:
            break

    print(boards)
    print(won)
    print(unmarked)
    sum_unmarked = sum([sum(row) for row in unmarked])

    return sum_unmarked * won


if __name__ == '__main__':
    print(solve())
