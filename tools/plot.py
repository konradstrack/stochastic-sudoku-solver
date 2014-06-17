import sys

from matplotlib import pyplot as plt


class Result():
    params = {}
    iterations = []

    def __init__(self, lines):
        info = lines[0].split()

        self.params = {
            'population_size': int(info[0]),
            'number_of_tournaments': int(info[1]),
            'tournament_size': int(info[2]),
            'mutation_probability': float(info[3]),
            'board_fill': int(info[4])
        }

        self.iterations = [line.split() for line in lines[1:]]


def read_files(file_list):
    results = []
    for filename in file_list:
        with open(filename) as f:
            lines = f.readlines()

        results.append(Result(lines))

    return results


def plot_by_fill(results):
    params = results[0].params
    figure_label = "Population: {0}, mutation probability: {1}".format(params['population_size'],
                                                               params['mutation_probability'])
    figure = plt.figure()
    figure.suptitle(figure_label)

    fills = set(result.params['board_fill'] for result in results)

    for fill in sorted(fills):
        selected = next(result.iterations for result in results if result.params['board_fill'] == fill)
        x = [l[0] for l in selected]
        mins = [l[1] for l in selected]

        label = "fill ratio {0:.2f}".format(fill / 81)
        plt.plot(x, mins, '-', label=label)

    plt.legend()
    plt.show()

if __name__ == "__main__":
    results = read_files(sys.argv[1:])

    plot_by_fill(results)

