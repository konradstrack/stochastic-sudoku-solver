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

    def get_row(self, row_number):
        return self._board[row_number, :]

    def get_column(self, col_number):
        return self._board[:, col_number]

    def get_square(self, row, col):
        r1 = row * 3
        c1 = col * 3
        return self._board[r1:r1 + 3, c1:c1 + 3]

    def set_row(self, row_number, row):
        self._board[row_number, :] = row

    def set_column(self, col_number, col):
        self._board[:, col_number] = col

    def set_square(self, row, col, square):
        r1 = row * 3
        c1 = col * 3
        self._board[r1:r1 + 3, c1:c1 + 3] = square