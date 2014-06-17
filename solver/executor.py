import argparse
import configparser
import sys

from algorithm import GeneticAlgorithm, HierarchicalAlgorithm, generate_population
from board import Board
from registry import registry



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
            __import__(group)
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

    configuration = {
        'use_genetic_only': alg_config.getboolean('use_genetic_only', False),

        'mutation': mutation_cls,
        'selection': selection_cls,
        'evaluation': evaluation_cls,
        'crossover': crossover_cls,

        'population_size': alg_config.getint('population_size', 100),
        'genetic_steps': alg_config.getint('genetic_steps', 100),
        'tournament_size': alg_config.getint('tournament_size', 20),
        'number_of_tournaments': alg_config.getint('number_of_tournaments', 40),

        'generator_fill_portion': alg_config.getfloat('generator_fill_portion', 0.4),

        'mutation_probability': alg_config.getfloat('mutation_probability', 0.8)
    }

    return configuration


if __name__ == "__main__":
    args = parse_arguments()
    configuration = build_configuration(args.configFile)

    # read a board from the file
    board_path = args.boardFile
    board = read_board(board_path)

    population_size = configuration['population_size']

    evaluation_cls = configuration['evaluation']
    selection_cls = configuration['selection']
    crossover_cls = configuration['crossover']
    mutation_cls = configuration['mutation']

    genetic_algorithm = GeneticAlgorithm(evaluation=evaluation_cls(),
                                         selection=selection_cls(configuration['number_of_tournaments'],
                                                                 configuration['tournament_size']),
                                         crossover=crossover_cls(population_size),
                                         mutation=mutation_cls(configuration['mutation_probability']))

    # print configuration for the current invocation
    print(population_size,
          configuration['number_of_tournaments'],
          configuration['tournament_size'],
          configuration['mutation_probability'])

    genetic_steps = configuration['genetic_steps']
    if configuration['use_genetic_only']:
        population = generate_population(board, population_size)
        output_population, solution = genetic_algorithm.execute(population, genetic_steps)
    else:
        hierarchical_algorithm = HierarchicalAlgorithm(genetic_algorithm)
        output_population, solution = hierarchical_algorithm.execute(board, genetic_steps=genetic_steps)

    print("=" * 100, file=sys.stderr)
    print("5 best boards:", file=sys.stderr)
    sort_by_fitness = lambda p: p.fitness if p.fitness is not None else 100
    for p in sorted(output_population, key=sort_by_fitness, reverse=True)[-5:]:
        print(p.board, p.fitness, file=sys.stderr)
        print(file=sys.stderr)

    print("=" * 100, file=sys.stderr)
    print("Initial board:\n{0}\n".format(board), file=sys.stderr)

    if solution is not None:
        print("Found solution:\n{0} {1}".format(solution.board, solution.fitness), file=sys.stderr)
    else:
        print("No solution.", file=sys.stderr)

