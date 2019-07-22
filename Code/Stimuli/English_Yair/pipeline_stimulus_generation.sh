#!/bin/bash -x

# Generate full stimulus set for each NA-task
python NA_tasks_generator.py --natask objrel -seed 1 -n 256 > ../../../Data/Stimuli/English_objrel.txt
python NA_tasks_generator.py --natask objrel_nounpp -seed 1 -n 64 > ../../../Data/Stimuli/English_objrel_nounpp.txt
python NA_tasks_generator.py --natask embedding_mental_SR -seed 1 -n 256 > ../../../Data/Stimuli/English_embedding_mental_SR.txt
python NA_tasks_generator.py --natask embedding_mental -seed 1 -n 64 > ../../../Data/Stimuli/English_embedding_mental.txt
python NA_tasks_generator.py --natask embedding_mental_2LRs -seed 1 -n 16 > ../../../Data/Stimuli/English_embedding_mental_2LRs.txt


# Verify that sub-sampled sets are counter-balanced with resepct to gender and other features
python verify_stimuli_file_is_balanced.py -f ../../../Data/Stimuli/English_objrel.txt
python verify_stimuli_file_is_balanced.py -f ../../../Data/Stimuli/English_objrel_nounpp.txt
python verify_stimuli_file_is_balanced.py -f ../../../Data/Stimuli/English_embedding_mental_SR.txt
python verify_stimuli_file_is_balanced.py -f ../../../Data/Stimuli/English_embedding_mental.txt
python verify_stimuli_file_is_balanced.py -f ../../../Data/Stimuli/English_embedding_mental_2LRs.txt
