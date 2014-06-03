from random import Random

__author__ = 'Konrad Strack'


def fill(board, uncertainty=1, repeat=4):
    result = board
    for _ in range(repeat):
        result = fill_intersections(result)

    return result


def fill_intersections(board, uncertainty=1):
    full = set(range(1, 10))
    random = Random()

    for r, row in enumerate(board):
        for c, value in enumerate(row):

            if value == 0:
                in_row = set(v for v in row)
                in_col = set(board[i, c] for i in range(board.shape()[0]))

                missing = full - (in_row | in_col)
                if len(missing) <= uncertainty:
                    board[r, c] = random.choice(list(missing))

    return board


def fill_squares(board, uncertainty=1):
    pass