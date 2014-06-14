from crossover import RowCrossover
from evaluation import SumEvaluation
from mutation import SingleSwapMutation
from selection import MockSelection


class GeneticAlgorithm():
    def __init__(self, population, steps=100):
        self.steps = steps
        self.population = population
        self.evaluation = SumEvaluation()
        self.selection = MockSelection()
        self.crossover = RowCrossover(len(population))
        self.mutation = SingleSwapMutation(probability=0.4)

    def execute(self):
        for i in range(self.steps):
            self.execute_step(i)

        return self.population

    def execute_step(self, i):
        self.evaluation.process(self.population)
        self.selection.process(self.population)
        self.crossover.process(self.population)
        self.mutation.process(self.population)