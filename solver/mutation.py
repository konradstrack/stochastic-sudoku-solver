import random

class MockMutation():
    def __init__(self, probability):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            self.__mutate(genotype)

    def __mutate(self, genotype):
        pass

class SingleSwapMutation():
	def __init__(self, probability):
		self.probability = probability

	def process(self, population):
		for genotype in population:
			self.__mutate(genotype)
	
	def __mutate(self, genotype):
		(rows, cols) = genotype.board.shape()
		(p1, p2) = random.sample(xrange(rows * cols), 2)
		(p1_r, p1_c) = genotype.board.get_indices(p1)
		(p2_r, p2_c) = genotype.board.get_indices(p2)
		tmp = genotype.board[p1_r, p1_c]
		genotype.board[p1_r, p1_c] = genotype.board[p2_r, p2_c]
		genotype.board[p2_r, p2_c] = tmp

# TODO: Switching rows, cols, squares