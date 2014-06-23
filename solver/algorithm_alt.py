from copy import copy
from random import Random
import sys
import numpy

from genotype import BoardGenotype
from logic import fill_steps
from algorithm import generate_population

class HierarchicalAlgorithm():
    def __init__(self, genetic, population_size):
        self.genetic = genetic
        self.population_size = population_size

    def execute(self, board, genetic_steps):

        boards = fill_steps(board, steps = 4)

        boards = boards[:self.population_size]

        population = []
        for b in boards:
            population.extend(generate_population(b, self.population_size // len(boards)))

        population.extend(generate_population(boards[-1], self.population_size % len(boards)))
        
        (output_population, solution) = self.genetic.execute(population=population, steps=genetic_steps)

        return (output_population, solution)

    def execute_iterated(self, board, genetic_steps, hierarchical_steps = 10):

        first_boards = fill_steps(board, steps = 3)

        top_solution_boards = first_boards

        for i in range(hierarchical_steps):

            boards = top_solution_boards[:self.population_size]

            population = []
            for b in boards:
                population.extend(generate_population(b, self.population_size // len(boards)))

            population.extend(generate_population(boards[-1], self.population_size % len(boards)))

            (output_population, solution) = self.genetic.execute(population=population, steps=genetic_steps)

            if solution != None:
                return (output_population, solution)
            sort_by_fitness = lambda p: p.fitness if p.fitness is not None else 100
            top_solutions = sorted(output_population, key=sort_by_fitness, reverse = True)[:50]

            top_solutions_boards = [g.board.copy() for g in top_solutions]
            # Leave just the invariants
            for b in top_solutions_boards:
                for (r, row) in enumerate(b):
                    for (c, col) in enumerate(row):
                        b[r,c] = 0
                b.fix_invariants()
            top_solution_boards.extend(boards)

        return (output_population, solution)

    def execute_iterated_another(self, board, genetic_steps, hierarchical_steps = 10):

        first_boards = fill_steps(board, steps = 1)

        top_solution_boards = first_boards

        for i in range(hierarchical_steps):
            boards = []
            for board in top_solution_boards:
                boards.extend(fill_steps(board, steps = 2))

            if len(top_solution_boards) > self.population_size:
                top_solution_boards = random.sample(boards, self.population_size)

            population = []
            for b in boards:
                population.extend(generate_population(b, self.population_size // len(boards)))

            population.extend(generate_population(boards[-1], self.population_size % len(boards)))

            (output_population, solution) = self.genetic.execute(population=population, steps=genetic_steps)

            if solution != None:
                return (output_population, solution)
            
            sort_by_fitness = lambda p: p.fitness if p.fitness is not None else 100
            top_solutions = sorted(output_population, key=sort_by_fitness, reverse = True)[:20]

            top_solutions_boards = [g.board.copy() for g in top_solutions]
            # Leave just the invariants
            for b in top_solutions_boards:
                for (r, row) in enumerate(b):
                    for (c, col) in enumerate(row):
                        b[r,c] = 0
                b.fix_invariants()

            top_solution_boards.append(board)

            boards = top_solution_boards

        return (output_population, solution)

random = Random()