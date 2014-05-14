from solver.board import Board
from solver.genotype import BoardGenotype
import random

class MockCrossover():
    def __init__(self, final_size):
        self.final_size = final_size

    def process(self, population):
        for i in xrange(self.final_size - len(population)):
            population.append(BoardGenotype(Board()))

class RowCrossover():
	'''Splits boards by rows'''
	def __init__(self, final_size):
		self.final_size = final_size

	def process(self, population):
		parents = list(population)
		for i in xrange(self.final_size - len(population)):
			p1, p2 = random.sample(parents, 2)
			genotype = self.cross(p1, p2)
			population.append(genotype)

  	def cross(self, p1, p2):
  		board = Board()
  		board.invariants = p1.board.invariants
  		split = random.randint(0, p1.board.shape()[0]) 

  		for i in xrange(split):
  			board.set_row(i, p1.board.get_row(i))
  		for i in xrange(split, p1.board.shape()[0]):
  			board.set_row(i, p2.board.get_row(i))
  		
  		genotype = BoardGenotype(board)
  		return genotype

class ColumnCrossover():
	'''Splits boards by columns'''
	def __init__(self, final_size):
		self.final_size = final_size

	def process(self, population):
		parents = list(population)
		for i in xrange(self.final_size - len(population)):
			p1, p2 = random.sample(parents, 2)
			genotype = self.cross(p1, p2)
			population.append(genotype)

  	def cross(self, p1, p2):
  		board = Board()
  		board.invariants = p1.board.invariants
  		split = random.randint(0, p1.board.shape()[1]) 

  		for i in xrange(split):
  			board.set_column(i, p1.board.get_column(i))
  		for i in xrange(split, p1.board.shape()[1]):
  			board.set_column(i, p2.board.get_column(i))
  		
  		genotype = BoardGenotype(board)
  		return genotype

class SquareCrossover():
	'''Splits boards by squares'''
	def __init__(self, final_size):
		self.final_size = final_size

	def process(self, population):
		parents = list(population)
		for i in xrange(self.final_size - len(population)):
			p1, p2 = random.sample(parents, 2)
			genotype = self.cross(p1, p2)
			population.append(genotype)

  	def cross(self, p1, p2):
  		board = Board()
  		board.invariants = p1.board.invariants
  		squares_num = p1.board.shape()[0] / 3 * p2.board.shape()[1] / 3 
  		split = random.randint(0, squares_num) 

  		for i in xrange(split):
  			row_num, col_num = board.get_square_indices(i)
  			board.set_square(row_num, col_num, p1.board.get_square(row_num, col_num))
  		for i in xrange(split, p1.board.shape()[1]):
  			row_num, col_num = board.get_square_indices(i)
  			board.set_square(row_num, col_num, p1.board.get_square(row_num, col_num))
  		
  		genotype = BoardGenotype(board)
  		return genotype