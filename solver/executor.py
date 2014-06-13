import sys
import random

from board import Board
from crossover import RowCrossover

from generator import BaseBoardGenerator
from genotype import BoardGenotype

from solver.mutation import SingleSwapMutation
from solver.selection import MockSelection
from solver.evaluation import SumEvaluation


class GeneticAlgorithm():
    def __init__(self, population, steps=100):
        self.steps = steps
        self.population = population
        self.evaluation = SumEvaluation()
        self.selection = MockSelection()
        self.crossover = RowCrossover(len(population))
        self.mutation = SingleSwapMutation(probability=0.4)

    def execute(self):
        solution = None
        self.evaluation.process(self.population)
        for i in range(self.steps):
            self.execute_step(i)
            solution = self.find_solution()
            if solution != None:
                break

        return (population, solution)

    def execute_step(self, i):
        self.selection.process(self.population)
        self.crossover.process(self.population)
        self.mutation.process(self.population)
        self.evaluation.process(self.population)

    def find_solution(self):
        """
        Check if we already found the solution.
        """
        for genotype in self.population:
            if genotype.fitness == self.evaluation.solution_fitness():
                return genotype
        return None

def random_fill(genotype):
    (rows, cols) = genotype.shape()
    for r in range(rows):
        for c in range(cols):
            if genotype[r, c] == 0:
                genotype[r, c] = random.randint(1, 9)
    return genotype


def read_board(board_path):
    with open(board_path, 'r') as f:
        lines = f.readlines()

    board = Board(lines)
    return board


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage:\n\t{0} [board_file]".format(sys.argv[0]))
        sys.exit(1)

    # read a board from the file
    board_path = sys.argv[1]
    board = read_board(board_path)

    print board

    # generate more boards
    base_boards = [board]
    board_generator = BaseBoardGenerator(base_boards)

    # create population
    board_list = board_generator.generate(10, 0.4)
    population = [BoardGenotype(board) for board in board_list]

    population = map(random_fill, population)

    algorithm = GeneticAlgorithm(population)
    (output_population, solution) = algorithm.execute()

    print solution
    for p in output_population:
        print()
        print(p.board)