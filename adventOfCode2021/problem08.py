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

    wons = []
    for draw in draws:
        for (index, board) in enumerate(board_rows):
            for row in board:
                if draw in row:
                    row.remove(draw)
                if len(row) == 0:
                    wons.append(index)
                    break
        if len(wons) > 0:
            if len(board_columns) == 1:
                break
            wons = sorted(wons)
            wons.reverse()
            for won_index in wons:
                del board_columns[won_index]
                del board_rows[won_index]
            wons = []
        for (index, board) in enumerate(board_columns):
            for row in board:
                if draw in row:
                    row.remove(draw)
                if len(row) == 0:
                    wons.append(index)
                    break
        if len(wons) > 0:
            if len(board_columns) == 1:
                break
            wons = sorted(wons)
            wons.reverse()
            for won_index in wons:
                print(won_index, len(board_columns))
                del board_columns[won_index]
                del board_rows[won_index]
            wons = []

    print(board_columns)
    print(board_rows)
    print(draw)
    sum_unmarked_rows = sum([sum(row) for row in board_rows[0]])
    sum_unmarked_cols = sum([sum(row) for row in board_columns[0]])
    sum_unmarked = sum_unmarked_rows if sum_unmarked_rows < sum_unmarked_cols else sum_unmarked_cols

    return sum_unmarked * draw


if __name__ == '__main__':
    print(solve())
