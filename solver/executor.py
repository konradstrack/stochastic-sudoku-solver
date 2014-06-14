import argparse

from algorithm import GeneticAlgorithm

from board import Board
from generator import BaseBoardGenerator
from genotype import BoardGenotype


def read_board(board_path):
    with open(board_path, 'r') as f:
        lines = f.readlines()

    board = Board(lines)
    return board


def parse_arguments():
    parser = argparse.ArgumentParser(description='Genetic algorithm for solving Sudoku.')
    parser.add_argument('-f', '--configFile', required=True, help='the algorithm configuration file')
    parser.add_argument('-b', '--boardFile', required=True, help='path to a single Sudoku board')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # read a board from the file
    board_path = args.boardFile
    board = read_board(board_path)

    # generate more boards
    base_boards = [board]
    board_generator = BaseBoardGenerator(base_boards)
    board_list = board_generator.generate(10, 0.4)

    # create population
    population = [BoardGenotype(board) for board in board_list]

    algorithm = GeneticAlgorithm(population)
    output_population = algorithm.execute()

    for p in output_population:
        print()
        print(p.board)