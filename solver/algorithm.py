from random import Random

from genotype import BoardGenotype


class GeneticAlgorithm():
    population = None

    def __init__(self, evaluation, selection, crossover, mutation):
        self.evaluation = evaluation
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation

    def execute(self, population, steps):
        self.population = population
        solution = None
        self.evaluation.process(self.population)

        for i in range(steps):
            self.execute_step(i)
            solution = self.find_solution(self.population)
            if solution is not None:
                break

        return population, solution

    def execute_step(self, i):
        self.evaluation.process(self.population)

        best = self.find_best_fitness(self.population)
        print("Best fitness in iteration {0}: {1}".format(i, best.fitness))

        self.selection.process(self.population)
        self.crossover.process(self.population)
        self.mutation.process(self.population)

    def find_solution(self, population):
        """
        Check if we already found the solution.
        """
        for genotype in population:
            if genotype.fitness == self.evaluation.solution_fitness():
                return genotype
        return None

    @staticmethod
    def find_best_fitness(population):
        select_fitness = lambda p: p.fitness if p.fitness is not None else 1e5
        return min(population, key=select_fitness)


class HierarchicalAlgorithm():
    def __init__(self, genetic):
        self.genetic = genetic

    def execute(self, boards, genetic_steps):
        random = Random()

        def random_fill(genotype):
            (rows, cols) = genotype.shape()
            for r in range(rows):
                for c in range(cols):
                    if genotype[r, c] == 0:
                        genotype[r, c] = random.randint(1, 9)
            return genotype

        # self.boards = itertools.chain(*(map(logic.fill, self.boards)))
        boards = map(random_fill, boards)
        population = [BoardGenotype(board) for board in boards]
        return self.genetic.execute(population=population, steps=genetic_steps)