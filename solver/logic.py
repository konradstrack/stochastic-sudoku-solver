__author__ = 'Konrad Strack'


def fill(board, uncertainty=1, repeat=4):
    result = board
    for _ in range(repeat):
        result = fill_intersections(result)

    return result


def fill_intersections(board, uncertainty=1):
    for r, row in enumerate(board):
        for c, value in enumerate(row):

            if value == 0:
                in_row = set(v for v in row)
                in_col = set(board[i, c] for i in range(board.shape[0]))

                print(in_row | in_col)


def fill_squares(board, uncertaint=1):
    pass