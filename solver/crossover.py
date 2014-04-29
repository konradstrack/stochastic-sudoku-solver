class MockCrossover():
	def __init__(self, final_size):
		self.final_size = final_size

	def process(self, population):
		for i in xrange(self.final_size - len(population)):
			population.append(Board())