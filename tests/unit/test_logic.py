from solver.board import Board
from solver.logic import fill

__author__ = 'Konrad Strack'

import numpy as np


class TestLogic():
    def test_if_fills_certain_intersections(self):
        init_board = np.zeros(shape=(9, 9))
        filled = {
            (2, 0): 1,
            (2, 1): 2,
            (2, 2): 3,
            (2, 3): 4,
            (5, 5): 5,
            (6, 5): 6,
            (7, 5): 8,
            (8, 5): 9
        }

        for k, v in filled.items():
            init_board[k] = v

        board = Board(init_board)

        filled_board = fill(board)[0]
        assert 7 == filled_board[2, 5]