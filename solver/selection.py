import random

class MockSelection():
    def process(self, population):
        population = population[:20]

#TODO: Dodac prawdopodobienstwo p, za opisem na wikipedii 
#http://en.wikipedia.org/wiki/Tournament_selection 
class TournamentSelection():
    def __init__(self, tournaments_number=20, tournament_size=20):
    	'''tournaments_number is the number of tournaments that take place
    	tournament_size is the size of each tournament
    	the population after selection has tournaments_number genotypes'''
        self.tournaments_number = tournaments_number
        self.tournament_size = tournament_size

    def process(self, population):
        p = list(population)
        population[:] = []
        for i in range(self.tournaments_number):
            sample = random.sample(p, self.tournament_size)
            winner = max(sample, key=lambda genotype: genotype.fitness)
            population.append(winner)
            p.remove(winner)

