# Example for running the pipeline for generating NA-taks
1. Generate a full NA-task based on ALL tokens in the lexicon
python NA_tasks_generator.py --natask nounPP > nounPP_Italian.txt

2. Filter the resulting file to have only, e.g., 250 samples from each value (singluar/plural or masculine/feminine) of each feature (grammatical number or gender)
python subsample_dataset.py -f nounPP_Italian.txt -n 250 --max-iter 10 > nounpp_Italian_4000.txt

3. Verify that the resutling sub-sampled file is indeed counter-balanced with respect to all features:
python verify_stimuli_file_is_balanced.py -f nounpp_Italian_4000.txt
