class MockEvaluation():
	def process(self, population):
		for genotype in population:
			genotype.fitness = self.__evaluate(genotype.board)

	def __evaluate(self,board):
		return 2