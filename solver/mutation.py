import random

import numpy

from registry import register


@register('mutation', 'mock')
class MockMutation():
    def __init__(self, probability):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            self.__mutate(genotype)

    def __mutate(self, genotype):
        pass


@register('mutation', 'single-swap')
class SingleSwapMutation():
    """
    Swaps values of two random fields. Omits invariants.
    """

    def __init__(self, probability=1.0):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.__mutate(genotype)

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()

        p1 = None
        p2 = None

        invariants = set(genotype.invariants.keys())
        fields = set((r, c) for r in range(rows) for c in range(cols))

        # If everything is invariant, there is nothing to swap.
        if len(fields) - len(invariants) < 2:
            return

        (p1, p2) = random.sample(fields - invariants, 2)
        (p1_r, p1_c) = p1
        (p2_r, p2_c) = p2

        tmp = genotype.board[p1_r, p1_c]
        genotype.board[p1_r, p1_c] = genotype.board[p2_r, p2_c]
        genotype.board[p2_r, p2_c] = tmp


@register('mutation', 'single-row-swap')
class SingleRowSwapMutation():
    """
    Swaps two random rows. Fixes invariants after mutating.
    """

    def __init__(self, probability=1.0):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.__mutate(genotype)
                genotype.board.fix_invariants()

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (r1, r2) = random.sample(range(rows), 2)

        tmp = numpy.copy(genotype.board.get_row(r1))
        genotype.board.set_row(r1, genotype.board.get_row(r2))
        genotype.board.set_row(r2, tmp)


@register('mutation', 'single-column-swap')
class SingleColumnSwapMutation():
    """
    Swaps two random squares. Fixes invariants after mutating.
    """

    def __init__(self, probability=1.0):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.__mutate(genotype)
                genotype.board.fix_invariants()

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (c1, c2) = random.sample(range(cols), 2)
        tmp = numpy.copy(genotype.board.get_column(c1))
        genotype.board.set_column(c1, genotype.board.get_column(c2))
        genotype.board.set_column(c2, tmp)


@register('mutation', 'single-square-swap')
class SingleSquareSwapMutation():
    """
    Swaps two random squares. Fixes invariants after mutating.
    """

    def __init__(self, probability=1.0):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.__mutate(genotype)
                genotype.board.fix_invariants()

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (s1, s2) = random.sample(range(rows // 3 * cols // 3), 2)
        (s1_r, s1_c) = genotype.board.get_square_indices(s1)
        (s2_r, s2_c) = genotype.board.get_square_indices(s2)

        tmp = numpy.copy(genotype.board.get_square(s1_r, s1_c))
        genotype.board.set_square(s1_r, s1_c, genotype.board.get_square(s2_r, s2_c))
        genotype.board.set_square(s2_r, s2_c, tmp)