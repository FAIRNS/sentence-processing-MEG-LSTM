#!/bin/bash
CUDA='' # ' --cuda' or '' (empty)
#CUDA=' --cuda'

for NATASK in 'objrel_V1' 'objrel_V2' 'objrel_nounpp_V1' 'objrel_nounpp_V2' 'embedding_mental_SR_V1' 'embedding_mental_SR_V2' 'embedding_mental_V1' 'embedding_mental_V2' 'embedding_mental_2LRs_V1' 'embedding_mental_2LRs_V2';
do
    echo
    echo 'Number-agreement task: '$NATASK
    # Calculate accuracies (without ablation)
    eval 'python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/hidden650_batch128_dropout0.2_lr20.0.pt -i ../Data/Stimuli/English_'$NATASK' -v ../Data/LSTM/models/english_vocab.txt -o ../Output/English_'$NATASK' --eos-separator "<eos>" --format pkl --lang en --uppercase-first-word'$CUDA
done
