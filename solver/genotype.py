class BoardGenotype():
    def __init__(self, board):
        self.board = board
        self.fitness = None

    def __getattr__(self, name):
        """Forward methods to board. AttributeError will be raised fo unknown methods. """
        attr = getattr(self.board, name)
        return attr