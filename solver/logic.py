from copy import copy
from random import Random

import numpy as np


__author__ = 'Konrad Strack'


def fill(boards, uncertainty=1, repeat=4, limit=10):
    """Creates a list of partially filled boards out of one board. The boards are filled in a human-like way,
    but with guessing.

    @param uncertainty specifies the limit of missing values for one field
    @param repeat specifies how many times the procedure should be repeated
    """
    # boards = [board]
    for _ in range(repeat):
        result = []

        # first fill the fields that can be filled non-randomly
        if uncertainty > 1:
            for b in boards:
                result.extend(fill_one(b, 1))
            boards = result

        # now fill the rest
        for b in boards:
            result.extend(fill_one(b, uncertainty))

        l = min(len(result), limit)
        boards = result[:l]

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
                        new_board = board.copy()
                        new_board[r, c] = field_value

                        boards.append(new_board)

    if len(boards) == 0:
        boards = [board]

    return boards
