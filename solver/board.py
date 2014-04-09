__author__ = 'Konrad Strack'

import numpy as np


class Board():
    def __init__(self):
        self._board = np.zeros(shape=(9, 9), dtype='i')

    def __getitem__(self, position):
        x, y = position
        return self._board[x, y]

    def __setitem__(self, position, value):
        x, y = position
        self._board[x, y] = value

    def shape(self):
        return self._board.shape