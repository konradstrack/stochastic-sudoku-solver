from solver.board import Board
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
		pass

	def rows_of_squares(self, board):
		pass

	def columns_of_cells(self, board):
		pass

	def rows_of_cells(self, board):
		pass