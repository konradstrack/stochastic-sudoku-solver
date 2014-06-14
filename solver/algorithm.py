from crossover import RowCrossover
from evaluation import SumEvaluation
from mutation import SingleSwapMutation
from selection import MockSelection


class GeneticAlgorithm():
    def __init__(self, population, evaluation, selection, crossover, mutation, steps=100):
        self.steps = steps
        self.population = population
        self.evaluation = evaluation
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation

    def execute(self):
        for i in range(self.steps):
            self.execute_step(i)

            print("=" * 100, i)
            print("=" * 100)
            for p in self.population[:3]:
                print(p.board)
                print()

        return self.population

    def execute_step(self, i):
        self.evaluation.process(self.population)
        self.selection.process(self.population)
        self.crossover.process(self.population)
        self.mutation.process(self.population)