#!/bin/bash

for mut in {00..90..10}
do
	FILENAME=filled_40_1
	echo "[algorithm]

use_genetic_only = False

evaluation = error-new
selection = tournament
crossover = row
mutation = single-swap

population_size = 200
genetic_steps = 400

tournament_size = 100
number_of_tournaments = 50

generator_fill_portion = 0.4

mutation_probability = 0.${mut}" > hierarchical_config_mut.ini
	python3 solver/executor_alt.py -b data/input_boards/${FILENAME}.txt -f hierarchical_config_mut.ini > data/results/hierarchical_iterated/based_on_mutation_probability/mut_${mut}.out
done


	FILENAME=filled_40_1
	echo "[algorithm]

use_genetic_only = False

evaluation = error-new
selection = tournament
crossover = row
mutation = single-swap

population_size = 200
genetic_steps = 400

tournament_size = 100
number_of_tournaments = 50

generator_fill_portion = 0.4

mutation_probability = 1.0" > hierarchical_config_mut.ini
	python3 solver/executor_alt.py -b data/input_boards/${FILENAME}.txt -f hierarchical_config_mut.ini > data/results/hierarchical_iterated/based_on_mutation_probability/mut_100.out

#!/bin/bash

for mut in {00..90..10}
do
	FILENAME=filled_40_1
	echo "[algorithm]

use_genetic_only = False

evaluation = error-new
selection = tournament
crossover = row
mutation = single-swap

population_size = 200
genetic_steps = 400

tournament_size = 100
number_of_tournaments = 50

generator_fill_portion = 0.4

mutation_probability = 0.${mut}" > hierarchical_config_mut.ini
	python3 solver/executor_alt_steps.py -b data/input_boards/${FILENAME}.txt -f hierarchical_config_mut.ini > data/results/hierarchical_iterated_with_steps/based_on_mutation_probability/mut_${mut}.out
done


	FILENAME=filled_40_1
	echo "[algorithm]

use_genetic_only = False

evaluation = error-new
selection = tournament
crossover = row
mutation = single-swap

population_size = 200
genetic_steps = 400

tournament_size = 100
number_of_tournaments = 50

generator_fill_portion = 0.4

mutation_probability = 1.0" > hierarchical_config_mut.ini
	python3 solver/executor_alt_steps.py -b data/input_boards/${FILENAME}.txt -f hierarchical_config_mut.ini > data/results/hierarchical_iterated_with_steps/based_on_mutation_probability/mut_100.out