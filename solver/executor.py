import argparse
import configparser
import sys

from algorithm import GeneticAlgorithm, HierarchicalAlgorithm
from board import Board
from registry import registry
from generator import BaseBoardGenerator

import mutation, selection, evaluation, crossover

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


def build_configuration(config_path):
    config = configparser.ConfigParser()
    config.read_file(open(config_path))

    alg_config = config['algorithm']

    def get_class(group, default):
        name = alg_config.get(group, default)
        try:
            cls = registry[group][name]
            return cls
        except KeyError as e:
            print("Error in the config file:\nThere's no {0} for '{1}'.\nUse one of: {2}".format(e, group, ", ".join(
                registry[group])))
            sys.exit(1)

    mutation_cls = get_class('mutation', 'mock')
    selection_cls = get_class('selection', 'mock')
    evaluation_cls = get_class('evaluation', 'mock')
    crossover_cls = get_class('crossover', 'mock')

    # noinspection PyDictCreation
    configuration = {
        'mutation': mutation_cls,
        'selection': selection_cls,
        'evaluation': evaluation_cls,
        'crossover': crossover_cls
    }

    # get other parameters
    configuration['genetic_steps'] = int(alg_config.get('genetic_steps', 100))

    return configuration


if __name__ == "__main__":
    args = parse_arguments()
    configuration = build_configuration(args.configFile)

    # read a board from the file
    board_path = args.boardFile
    board = read_board(board_path)


    # generate more boards
    base_boards = [board]
    board_generator = BaseBoardGenerator(base_boards)
    board_list = board_generator.generate(100, 0.4)

    evaluation_cls = configuration['evaluation']
    selection_cls = configuration['selection']
    crossover_cls = configuration['crossover']
    mutation_cls = configuration['mutation']

    population_size = len(board_list)
    genetic_algorithm = GeneticAlgorithm(evaluation=evaluation_cls(),
                                         selection=selection_cls(population_size // 2, 20),
                                         crossover=crossover_cls(population_size),
                                         mutation=mutation_cls())

    hierarchical_algorithm = HierarchicalAlgorithm(genetic_algorithm)

    genetic_steps = configuration['genetic_steps']
    output_population, solution = hierarchical_algorithm.execute(board_list, genetic_steps=genetic_steps)

    print("=" * 100)
    print("5 best boards:")
    sort_by_fitness = lambda p: p.fitness if p.fitness is not None else 100
    for p in sorted(output_population, key=sort_by_fitness, reverse=True)[-5:]:
        print(p.board, p.fitness)
        print()

    print("=" * 100)
    print("Initial board used to generate the population:\n{0}\n".format(board))

    if solution is not None:
        print("Found solution:\n{0} {1}".format(solution.board, solution.fitness))
    else:
        print("No solution.")

