from math import sqrt

import numpy as np

from registry import register


@register('evaluation', 'mock')
class MockEvaluation():
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__evaluate(genotype.board)

    def __evaluate(self, board):
        return 2


@register('evaluation', 'sum')
class SumEvaluation():
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__evaluate(genotype.board)

    def __evaluate(self, board):
        """
        Evaluation based on differences between a perfect sum
        (for a correct filling) and actual sum in columns and rows.
        Assumes we are working on filled boards.
        """
        (rows, cols) = board.shape()
        perfect_sum = (1 + rows) * rows / 2
        error = 0

        for i in range(rows):
            row = board.get_row(i)
            row_sum = np.sum(row)
            error += (perfect_sum - row_sum) ** 2

        for i in range(cols):
            col = board.get_column(i)
            col_sum = np.sum(col)
            error += (perfect_sum - col_sum) ** 2

        for i in range(rows * cols // 9):
            (r, c) = board.get_square_indices(i)
            square = board.get_square(r, c)
            square_sum = np.sum(square)
            error += (perfect_sum - square_sum) ** 2

        error /= rows * 2
        error = sqrt(error)

        return error

    def solution_fitness(self):
        """
        Fitness for the correct solution. 
        We need average 0 difference for every row and column and square.
        """
        return 0


@register('evaluation', 'error')
class ErrorEvaluation():
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__evaluate(genotype.board)

    def __evaluate(self, board):
        """
        Evaluation based on number of errors (multiple values of same number)
        (for a correct filling) and actual sum in columns, rows and squares.
        Assumes we are working on filled boards.
        """
        (rows, cols) = board.shape()
        squares = rows * cols // 9
        errors = 0

        errors += self.__get_errors(board, board.get_row, rows)
        errors += self.__get_errors(board, board.get_column, cols)
        errors += self.__get_errors(board, lambda i: board.get_square(*board.get_square_indices(i)), squares)

        errors /= (rows + cols + squares) * 1.
        return errors

    def __get_errors(self, board, get_area, num_areas):
        area_errors = 0
        for i in range(num_areas):
            area = get_area(i).flat
            area_counts = np.bincount(area)
            for count in area_counts:
                if count > 1:
                    area_errors += count - 1

        return area_errors

    def solution_fitness(self):
        """
        Fitness for the correct solution. We need 0 errors.
        """
        return 0

			
