import numpy

from solver.board import Board


__author__ = 'Konrad Strack'


class TestBoard():
    def test_if_board_has_the_correct_size(self):
        board = Board()

        assert board.shape() == (9, 9)

    def test_setting_and_getting_fields(self):
        board = Board()

        value = 14
        board[1, 3] = value

        assert board[1, 3] == value

    def test_setting_invariants(self):
        invariants = [(0, 4), (2, 3), (7, 1)]

        initial_board = numpy.zeros(shape=(9, 9), dtype='i')

        for r, c in invariants:
            initial_board[r, c] = 7

        board = Board(initial_board)
        assert set(board.invariants) == set(invariants)

    def test_setting_invariants_on_the_board(self):
        invariants = [(0, 4), (2, 3), (7, 1)]

        initial_board = numpy.zeros(shape=(9, 9), dtype='i')

        for r, c in invariants:
            initial_board[r, c] = 7

        board = Board(initial_board)

        for r in range(9):
            for c in range(9):
                assert board[r, c] == 0 or (board[r, c] == 7 and (r, c) in invariants)
