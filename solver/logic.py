from copy import copy
from random import Random

import numpy as np


__author__ = 'Konrad Strack'


def fill(board, uncertainty=1, repeat=4):
    boards = [board]
    for _ in range(repeat):
        print(boards)
        result = []
        for b in boards:
            result.extend(fill_one(b, uncertainty))

        boards = result

    return boards


def fill_one(board, uncertainty=1):
    full = set(range(1, 10))
    random = Random()

    boards = []
    for r, row in enumerate(board):
        for c, value in enumerate(row):

            if value == 0:
                in_row = set(v for v in row)
                in_col = set(board[i, c] for i in range(board.shape()[0]))

                square = board.get_square(r // 3, c // 3)
                in_square = set(square[ind] for ind, n in np.ndenumerate(square))

                missing = full - (in_row | in_col | in_square)

                if 0 < len(missing) <= uncertainty:
                    take = len(missing)
                    for field_value in random.sample(list(missing), take):
                        new_board = copy(board)
                        new_board[r, c] = field_value

                        boards.append(new_board)

    if len(boards) == 0:
        boards = [board]
        
    return boards
