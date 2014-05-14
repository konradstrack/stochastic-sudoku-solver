import numpy as np
from math import sqrt	

class MockEvaluation():
    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__evaluate(genotype.board)

    def __evaluate(self, board):
        return 2

class SumEvaluation():
	def process(self, population):
		for genotype in population:
			genotype.fitness = self.__evaluate(genotype.board)

	def __evaluate(self, board):
		"""Evaluation based on differences between a perfect sum 
			(for a correct filling) and actual sum in columns and rows"""
		(rows, cols) = board.shape()
		perfect_sum = (1 + rows) * rows / 2
		error = 0

		for i in xrange(rows):
			row = board.get_row(i)
			row_sum = np.sum(row)
			error += (perfect_sum - row_sum) ** 2

		for i in xrange(cols):
			col = board.get_column(i)
			col_sum = np.sum(col)
			error += (perfect_sum - col_sum) ** 2

		error /= rows * 2
		error = sqrt(error)

		return error

#TODO: Add penalty for messing up invariants. OR just omit them while mutating 
class ErrorEvaluation():
	def process(self, population):
		for genotype in population:
			genotype.fitness = self.__evaluate(genotype.board)

	def __evaluate(self, board):
		"""Evaluation based on differences between a perfect sum 
			(for a correct filling) and actual sum in columns and rows"""
		(rows, cols) = board.shape()
		error = 0

		for i in xrange(rows):
			row = board.get_row(i)
			row_counts = np.bincount(row)
			for count in row_counts:
				if count > 1:
					error += count - 1

		for i in xrange(cols):
			col = board.get_column(i)
			col_counts = np.bincount(col)
			for count in col_counts:
				if count > 1:
					error += count - 1

		error /= (rows + cols)
		return error
			
