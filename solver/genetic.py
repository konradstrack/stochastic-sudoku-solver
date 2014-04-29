from mutation import MockMutation
from crossover import MockCrossover
from selection import MockSelection
from evaluation import MockEvaluation

class Genetic():
	def __init__(self, population, steps = 100):
		self.steps = steps
		self.population = population
		self.evaluation = MockEvaluation()
		self.selection = MockSelection()
		self.crossover = MockCrossover(len(population))
		self.mutation = MockMutation(probability = 0.4)

	def execute(self):
		for i in xrange(self.steps):
			self.execute_step(i)

	def execute_step(self, i):
		self.evaluation.process(self.population)
		self.selection.process(self.population)
		self.crossover.process(self.population)
		self.mutation.process(self.population)
