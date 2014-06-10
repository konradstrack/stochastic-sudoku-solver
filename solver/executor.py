import sys

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
        for i in range(self.steps):
            self.execute_step(i)

        return population

    def execute_step(self, i):
        self.evaluation.process(self.population)
        self.selection.process(self.population)
        self.crossover.process(self.population)
        self.mutation.process(self.population)


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

    # generate more boards
    base_boards = [board]
    board_generator = BaseBoardGenerator(base_boards)

    # create population
    board_list = board_generator.generate(10, 0.4)
    population = [BoardGenotype(board) for board in board_list]

    algorithm = GeneticAlgorithm(population)
    output_population = algorithm.execute()

    for p in output_population:
        print()
        print(p.board)