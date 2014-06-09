from solver.board import Board
import numpy
import copy
import random

class BaseBoardGenerator(object):
	"""
	Generates boards based on given filled base boards.
	Uses available permutations:
	- permuting columns of squares
	- permuting rows of squares
	- permuting columns of cells within a single column of squares and
	- permuting rows of cells within a single row of squares
	"""
	PERMUTATIONS = ["cols_of_squares", "rows_of_squares", "columns_of_cells", "rows_of_cells"]

	def __init__(self, base_boards):
		self.boards = base_boards

	def generate(self, size, fill_portion):
		"""Generates size boards, with fill_portion of fields filled."""
		generated_boards = []
		for i in xrange(size):
			board = self.__generate_board()
			self.__remove_percentage(board, 1 - fill_portion)
			board.set_invariants()
			generated_boards.append(board)
		return generated_boards

	def __generate_board(self):
		board = copy.deepcopy(random.choice(self.boards))
		permutation = getattr(self, self.PERMUTATIONS[random.randrange(len(self.PERMUTATIONS))])
		permutation(board)
		return board

	def __remove_percentage(self, board, to_remove_percentage):
		(rows, cols) = board.shape()
		num_fields = rows * cols
		to_remove = int(num_fields * to_remove_percentage)

		for i in random.sample(range(num_fields), to_remove):
			(r, c) = board.get_indices(i)
			board[r, c] = 0


	def cols_of_squares(self, board):
		"""
		Permutes columns of squares.
		"""
		permute = [0,1,2]
		random.shuffle(permute)

		as_cols_of_squares = [[numpy.copy(board.get_column(i)) for i in xrange(begin, begin+3)] for begin in [0,3,6]]


		for (i, col_of_squares) in enumerate(permute):
			for j in xrange(3):
				board.set_column(3 * i + j, as_cols_of_squares[col_of_squares][j])



	def rows_of_squares(self, board):
		"""
		Permutes rows of squares.
		"""
		permute = [0,1,2]
		random.shuffle(permute)

		as_rows_of_squares = [[numpy.copy(board.get_row(i)) for i in xrange(begin, begin+3)] for begin in [0,3,6]]


		for (i, row_of_squares) in enumerate(permute):
			for j in xrange(3):
				board.set_row(3 * i + j, as_rows_of_squares[row_of_squares][j])

	def columns_of_cells(self, board):
		"""
		Permutes columns of cells within single column of squares.
		"""

		col_of_squares = random.randrange(3)
		permute = [0,1,2]
		random.shuffle(permute)
		begin = col_of_squares * 3
		cols = [numpy.copy(board.get_column(i)) for i in xrange(begin, begin+3)]

		for i, col in enumerate(permute):
			board.set_column(begin + i, cols[col])



	def rows_of_cells(self, board):
		"""
		Permutes rows of cells within single row of squares.
		"""
		row_of_squares = random.randrange(3)
		permute = [0,1,2]
		random.shuffle(permute)
		begin = row_of_squares * 3
		rows = [numpy.copy(board.get_row(i)) for i in xrange(begin, begin+3)]

		for i, row in enumerate(permute):
			board.set_row(begin + i, rows[row])
