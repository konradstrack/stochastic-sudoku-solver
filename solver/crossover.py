import random

from registry import register
from solver.board import Board
from solver.genotype import BoardGenotype


@register('crossover', 'mock')
class MockCrossover():
    def __init__(self, final_size):
        self.final_size = final_size

    def process(self, population):
        for i in range(self.final_size - len(population)):
            population.append(BoardGenotype(Board()))


@register('crossover', 'row')
class RowCrossover():
    """Splits boards by rows"""

    def __init__(self, final_size):
        self.final_size = final_size

    def process(self, population):
        parents = list(population)
        for i in range(self.final_size - len(population)):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

    def cross(self, p1, p2):
        board = Board()
        split = random.randint(0, p1.board.shape()[0])

        for i in range(split):
            board.set_row(i, p1.board.get_row(i))
        for i in range(split, p1.board.shape()[0]):
            board.set_row(i, p2.board.get_row(i))

        board.invariants = InvariantsMerger.merge_invariants(p1, p2, self.__area_function(split))

        genotype = BoardGenotype(board)
        return genotype

    def __area_function(self, split):
        return lambda r_c: r_c[0] < split


@register('crossover', 'column')
class ColumnCrossover():
    """Splits boards by columns"""

    def __init__(self, final_size):
        self.final_size = final_size

    def process(self, population):
        parents = list(population)
        for i in range(self.final_size - len(population)):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

    def cross(self, p1, p2):
        board = Board()
        split = random.randint(0, p1.board.shape()[1])

        for i in range(split):
            board.set_column(i, p1.board.get_column(i))
        for i in range(split, p1.board.shape()[1]):
            board.set_column(i, p2.board.get_column(i))

        board.invariants = InvariantsMerger.merge_invariants(p1, p2, self.__area_function(split))

        genotype = BoardGenotype(board)
        return genotype

    def __area_function(self, split):
        return lambda r_c: r_c[1] < split


@register('crossover', 'square')
class SquareCrossover():
    """Splits boards by squares"""

    def __init__(self, final_size):
        self.final_size = final_size

    def process(self, population):
        parents = list(population)
        for i in range(self.final_size - len(population)):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

    def cross(self, p1, p2):
        board = Board()
        squares_num = p1.board.shape()[0] / 3 * p2.board.shape()[1] / 3
        split = random.randint(0, squares_num)

        for i in range(split):
            row_num, col_num = board.get_square_indices(i)
            board.set_square(row_num, col_num, p1.board.get_square(row_num, col_num))

        for i in range(split, p1.board.shape()[1]):
            row_num, col_num = board.get_square_indices(i)
            board.set_square(row_num, col_num, p1.board.get_square(row_num, col_num))

        board.invariants = InvariantsMerger.merge_invariants(p1, p2,
                                                             self.__area_function(board.get_square_indices(split)))

        genotype = BoardGenotype(board)
        return genotype

    def __area_function(self, square_split):
        split_r, split_c = square_split
        split_r = split_r * 3
        split_c = split_c * 3
        return lambda r_c: r_c[0] < split_r or r_c[0] < split_r + 3 and r_c[1] < split_c


class InvariantsMerger(object):
    @classmethod
    def merge_invariants(cls, board1, board2, area_function):
        """
        Merges the invariants of board 1 and board2 using area_function.
        The resulting invariants contain invariants of board1 that are in first area 
        and invariants of board2 that are in the second area. 
        Area_function returns true if given point p = (r,c) is in the first area and false otherwise.
        """
        invariants = {}
        invariants.update({p: v for p, v in board1.invariants.items() if area_function(p)})
        invariants.update({p: v for p, v in board2.invariants.items() if not area_function(p)})

        return invariants