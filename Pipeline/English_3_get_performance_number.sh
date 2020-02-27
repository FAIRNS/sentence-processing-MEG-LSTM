#!/bin/bash

#for NATASK in 'objrel_V1' 'objrel_V2' 'embedding_mental_SR_V1' 'embedding_mental_SR_V2';
#for NATASK in 'objrel_V1' 'objrel_V2' 'objrel_pronoun_V1' 'objrel_pronoun_V2';
for NATASK in 'objrel_V1' 'objrel_V2' 'objrel_pronoun_V1' 'objrel_pronoun_V2' 'subjrel_V1' 'subjrel_V2';
do
    echo '-------------------------------'
    echo 'Number-agreement task: '$NATASK
    echo '-------------------------------'
    # Calculate accuracies (without ablation)
    # Calc accuracy for each condition (SS/SP/PS/PP)
    for NUMBER in 'singular' 'plural';
    do
        for ATTRACTOR in 'singular' 'plural';
        do
            echo
            eval 'python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/English_'$NATASK'.abl -info ../Data/Stimuli/English_'$NATASK'.info -condition number_1='$NUMBER' number_2='$ATTRACTOR
        done
    done
done
