#!/bin/bash
CUDA='' # ' --cuda' or '' (empty)
#CUDA=' --cuda'

#for NATASK in 'nounpp' 'subjrel_that' 'objrel_that' 'objrel_nounpp_V1' 'objrel_that_V1' 'subjrel_that_V1' 'objrel_nounpp' 'nounpp_copula_number' 'nounpp_copula_gender';'nounpp_objrel_capitalized' 'nounpp_objrel_V1_capitalized'
for NATASK in 'objrel_that_V1' 'objrel_that_V2' 'subjrel_that_V1' 'subjrel_that_V2';
do
    NUM_STIMULI=4000
    echo
    echo 'Number-agreement task: '$NATASK
    if [[ $NATASK == nounpp_objrel* ]]
    then
        NUM_STIMULI=4032
    fi
    echo $NUM_STIMULI
    # Calculate accuracies (without ablation)
    eval 'python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI' -v ../Data/LSTM/models/Italian_vocab.txt -o ../Output/Italian_'$NATASK'_'$NUM_STIMULI' --eos-separator "<eos>" --format pkl --lang it --uppercase-first-word'$CUDA
done
