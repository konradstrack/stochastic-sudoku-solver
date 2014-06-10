from random import Random

import numpy as np


__author__ = 'Konrad Strack'


def fill(board, uncertainty=1, repeat=4):
    result = board
    for _ in range(repeat):
        result = fill_one(result, uncertainty)

    return result


def fill_one(board, uncertainty=1):
    full = set(range(1, 10))
    random = Random()

    for r, row in enumerate(board):
        for c, value in enumerate(row):

            if value == 0:
                in_row = set(v for v in row)
                in_col = set(board[i, c] for i in range(board.shape()[0]))
                in_square = set(board[ind[0], ind[1]] for ind, n in np.ndenumerate(board.get_square(r // 3, c // 3)))

                missing = full - (in_row | in_col | in_square)
                if 0 < len(missing) <= uncertainty:
                    board[r, c] = random.choice(list(missing))

    return board
