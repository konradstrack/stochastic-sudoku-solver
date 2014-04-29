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

    def test_getting_columns(self):
        initial_board = numpy.arange(81)
        initial_board.shape = (9, 9)
        board = Board(initial_board)

        assert (board.get_column(1) == range(1, 81, 9)).all()
        assert (board.get_column(3) == range(3, 81, 9)).all()

    def test_getting_rows(self):
        initial_board = numpy.arange(81)
        initial_board.shape = (9, 9)
        board = Board(initial_board)

        assert (board.get_row(1) == range(9, 18)).all()
        assert (board.get_row(3) == range(27, 36)).all()

    def test_getting_squares(self):
        initial_board = numpy.arange(81)
        initial_board.shape = (9, 9)
        board = Board(initial_board)

        print(initial_board)

        square00 = [[0, 1, 2],
                    [9, 10, 11],
                    [18, 19, 20]]

        square12 = [[33, 34, 35],
                    [42, 43, 44],
                    [51, 52, 53]]

        assert (board.get_square(0, 0) == square00).all()
        assert (board.get_square(1, 2) == square12).all()
