import random

import numpy

from board import InvariantsFixer


class MockMutation():
    def __init__(self, probability):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            self.__mutate(genotype)

    def __mutate(self, genotype):
        pass


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

        while not p1 and not p2 or (p1_r, p1_c) in genotype.invariants or (p2_r, p2_c) in genotype.invariants:
            (p1, p2) = random.sample(range(rows * cols), 2)
            (p1_r, p1_c) = genotype.board.get_indices(p1)
            (p2_r, p2_c) = genotype.board.get_indices(p2)
            if (p1_r, p1_c) in genotype.invariants or (p2_r, p2_c) in genotype.invariants:
                print
                "inv"

        tmp = genotype.board[p1_r, p1_c]
        genotype.board[p1_r, p1_c] = genotype.board[p2_r, p2_c]
        genotype.board[p2_r, p2_c] = tmp


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
                InvariantsFixer.fix_invariants(genotype)

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (r1, r2) = random.sample(range(rows), 2)

        tmp = numpy.copy(genotype.board.get_row(r1))
        genotype.board.set_row(r1, genotype.board.get_row(r2))
        genotype.board.set_row(r2, tmp)


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
                InvariantsFixer.fix_invariants(genotype)

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (c1, c2) = random.sample(range(cols), 2)
        tmp = numpy.copy(genotype.board.get_column(c1))
        genotype.board.set_column(c1, genotype.board.get_column(c2))
        genotype.board.set_column(c2, tmp)


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
                InvariantsFixer.fix_invariants(genotype)

    def __mutate(self, genotype):
        (rows, cols) = genotype.board.shape()
        (s1, s2) = random.sample(range(rows / 3 * cols / 3), 2)
        (s1_r, s1_c) = genotype.board.get_square_indices(s1)
        (s2_r, s2_c) = genotype.board.get_square_indices(s2)

        tmp = numpy.copy(genotype.board.get_square(s1_r, s1_c))
        genotype.board.set_square(s1_r, s1_c, genotype.board.get_square(s2_r, s2_c))
        genotype.board.set_square(s2_r, s2_c, tmp)