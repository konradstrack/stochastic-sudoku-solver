class MockMutation():
    def __init__(self, probability):
        self.probability = probability

    def process(self, population):
        for genotype in population:
            self.__mutate(genotype)

    def __mutate(self, genotype):
        pass
