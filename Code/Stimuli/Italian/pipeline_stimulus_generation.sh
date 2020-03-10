#!/bin/bash -x

# Generate full stimulus set for each NA-task
python NA_tasks_generator.py --natask nounpp -seed 1 > Italian_nounpp.txt
python NA_tasks_generator.py --natask subjrel -seed 1 > Italian_subjrel.txt
python NA_tasks_generator.py --natask objrel -seed 1 > Italian_objrel.txt
python NA_tasks_generator.py --natask nounpp_copula -seed 1 > Italian_nounpp_copula.txt
python NA_tasks_generator.py --natask objrel_nounpp -seed 1 > Italian_objrel_nounpp.txt

# Subsample 4000 stimuli
python subsample_dataset.py -f Italian_nounpp.txt -n 250 --IX-last -1 -seed 1 > Italian_nounpp_4000.txt
python subsample_dataset.py -f Italian_subjrel.txt -n 250 --IX-last -2 -seed 1 > Italian_subjrel_4000.txt
python subsample_dataset.py -f Italian_objrel.txt -n 250 --IX-last -2 -seed 1 > Italian_objrel_4000.txt
python subsample_dataset.py -f Italian_nounpp_copula.txt -n 250 --IX-last -2 -seed 1 > Italian_nounpp_copula_4000.txt
python subsample_dataset_two_attractors.py -f Italian_objrel_nounpp.txt -n 63 --IX-last -2 -seed 1 > Italian_objrel_nounpp_4032.txt

# Verify that sub-sampled sets are counter-balanced with resepct to gender and other features
echo 'nounpp'
python verify_stimuli_file_is_balanced.py -f Italian_nounpp_4000.txt
echo 'subjrel'
python verify_stimuli_file_is_balanced.py -f Italian_subjrel_4000.txt
echo 'objrel'
python verify_stimuli_file_is_balanced.py -f Italian_objrel_4000.txt
echo 'nounpp_copula'
python verify_stimuli_file_is_balanced.py -f Italian_nounpp_copula_4000.txt
echo 'objrel_nounpp'
python verify_stimuli_file_is_balanced.py -f Italian_objrel_nounpp_4000.txt
