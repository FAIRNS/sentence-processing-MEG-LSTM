        Presenting the Number Agreement data

Every file in this folder corresponds to one category of stimuli used in the Number Agreement (NA) task presented in the paper. 
They contains 4 columns, separated by tabulations:
- the first one contains the sentence
- the second one contains the plurality of the subject (singular or plural), 
  or, in the relative clause conditions, the plurality of the subject followed by that of the subject inside the relative clause (the distractor), 
  eg: singular_plural and plural_singular are the incongruent conditions described in the paper.
- the third column contains "correct" or "wrong", depending on whether this sentence has a correct number agreement or not.
  Each of the sentences is present twice, once with the correct agreement and once with the wrong one.
  The sentence is considered correct if the model assigns a higher probability to the correct verb than to the wrong one.
- the fourth column contains the sentence id (it is the same for both correct and wrong version of the same sentence).


If you want to use these sentences to reproduce the results of the paper, optionnaly with your own model, 
you can pass each file to the script ../convert_sentences_to_tal_format.pl, which will create a .text and a .gold file, 
that are directly read by the /sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py script. 

The full ablation pipeline can be found in sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/run_full_ablation_pipeline.sh and analyse_ablation_results.sh
