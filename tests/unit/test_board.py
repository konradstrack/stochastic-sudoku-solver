from solver.board import Board

__author__ = 'Konrad Strack'


class TestBoard(object):
    def test_if_board_has_the_correct_size(self):
        board = Board()

        assert board.shape() == (9, 9)

    def test_setting_and_getting_fields(self):
        board = Board()

        value = 14
        board[1, 3] = value

        assert board[1, 3] == value