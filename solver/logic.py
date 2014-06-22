from copy import copy
from random import Random

import numpy as np
import itertools

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

def fill_just_one(board, uncertainty=1):
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

                    return boards

    return []

def fill_all_sure(board):
    full = set(range(1, 10))
    random = Random()
    new_board = board.copy()
    changed = True
    while changed:
        changed = False
        for r, row in enumerate(new_board):
            for c, value in enumerate(row):
                if value == 0:
                    in_row = set(v for v in row)
                    in_col = set(new_board[i, c] for i in range(new_board.shape()[0]))

                    square = new_board.get_square(r // 3, c // 3)
                    in_square = set(square[ind] for ind, n in np.ndenumerate(square))

                    missing = full - (in_row | in_col | in_square)

                    if len(missing) == 1:
                        field_value, = missing 
                        new_board[r, c] = field_value
                        changed = True

    return new_board

def fill_min_max(board, minimum = 5, maximum = 10):
    boards = []
    for uncertainty in range(1, 8):
        boards = fill([board], uncertainty, 6, maximum)
        if len(boards) >= minimum:
            return boards

def fill_steps(board, steps = 3):
    boards = [fill_all_sure(board)]
    uncertainty = 2
    new_boards = boards
    i = steps
    while i > 0 and uncertainty < 9:
        new_boards = \
            list(itertools.chain.from_iterable(
                [fill_just_one(b, uncertainty) for b in new_boards]))
        
        if len(new_boards) == 0:
            uncertainty += 1
        else:
            i -= 1
            boards.extend(new_boards)

    for b in boards:
        b.set_invariants()

    return boards



