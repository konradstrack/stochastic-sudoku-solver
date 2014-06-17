import argparse

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


def plot_by_fill_ratio(results, y_column):
    params = results[0].params
    figure_label = "Population: {0}, mutation probability: {1}".format(params['population_size'],
                                                                       params['mutation_probability'])
    figure = plt.figure()
    figure.suptitle(figure_label)

    fills = set(result.params['board_fill'] for result in results)

    for fill in sorted(fills):
        selected = next(result.iterations for result in results if result.params['board_fill'] == fill)
        x = [l[0] for l in selected]
        values = [l[y_column] for l in selected]

        label = "fill ratio {0:.2f}".format(fill / 81)
        plt.plot(x, values, '-', label=label)

    plt.ylabel("error value")
    plt.xlabel("iteration number")
    plt.legend()
    plt.show()


def plot_by_mutation_probability(results, y_column):
    params = results[0].params
    figure_label = "Population: {0}, fill ratio: {1}".format(params['population_size'],
                                                             params['board_fill'])
    figure = plt.figure()
    figure.suptitle(figure_label)

    probabilities = set(result.params['mutation_probability'] for result in results)

    for p in sorted(probabilities):
        selected = next(result.iterations for result in results if result.params['mutation_probability'] == p)
        x = [l[0] for l in selected]
        values = [l[y_column] for l in selected]

        label = "mutation prob. {0}".format(p)
        plt.plot(x, values, '-', label=label)

    plt.ylabel("error value")
    plt.xlabel("iteration number")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', required=True, help="type of the plot: mutation, fill")
    parser.add_argument('-v', '--value', help="values to print: min, mean", default="min")
    parser.add_argument('files', nargs='+', help="files with results")
    args = parser.parse_args()

    results = read_files(args.files)

    if args.value == "mean":
        y_column = 2
    else:
        y_column = 1

    if args.type == 'mutation':
        plot_by_mutation_probability(results, y_column)
    elif args.type == 'fill':
        plot_by_fill_ratio(results, y_column)

