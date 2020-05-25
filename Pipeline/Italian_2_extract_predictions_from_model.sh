#!/bin/bash
CUDA='' # ' --cuda' or '' (empty)
#CUDA=' --cuda'

#for NATASK in 'objrel_that_V1' 'objrel_that_V2' 'objrel_nounpp_V1' 'objrel_nounpp_V2' 'sc_short_V1' 'sc_long_V1'
for NATASK in 'simple_non'
do
    NUM_STIMULI=4000
    echo
    echo 'Number-agreement task: '$NATASK
    if [[ $NATASK == objrel_nounpp* ]]
    then
        NUM_STIMULI=4032
    fi
    if [[ $NATASK == sc_long* ]]
    then
        NUM_STIMULI=4032
    fi
    if [[ $NATASK == simple_non* ]]
    then
        NUM_STIMULI=512
    fi
    echo $NUM_STIMULI
    # Calculate accuracies (without ablation)
    eval 'python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI' -v ../Data/LSTM/models/Italian_vocab.txt -o ../Output/Italian_'$NATASK'_'$NUM_STIMULI' --eos-separator "<eos>" --format pkl --lang it --uppercase-first-word'$CUDA
done

# python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_double_subjrel_V1 -v ../Data/LSTM/models/Italian_vocab.txt -o ../Output/Italian_double_subjrel_V1 --eos-separator "<eos>" --format pkl --lang it --uppercase-first-word --cuda
