__author__ = 'Konrad Strack'

import numpy as np


class Board():
    def __init__(self, initial_board=None):
        self._board = np.zeros(shape=(9, 9), dtype='i')
        self.invariants = []

        if initial_board is not None:
            for r, row in enumerate(initial_board[:9]):
                for c, col in enumerate(row[:9]):
                    if col != 0:
                        self.invariants.append((r, c))
                        self._board[r, c] = col

    def __getitem__(self, position):
        x, y = position
        return self._board[x, y]

    def __setitem__(self, position, value):
        x, y = position
        self._board[x, y] = value

    def shape(self):
        return self._board.shape