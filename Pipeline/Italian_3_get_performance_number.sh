#!/bin/bash

#for NATASK in 'nounpp' 'subjrel_that' 'objrel_that';
for NATASK in 'embedding_mental_SR';
#for NATASK in 'nounpp' 'subjrel_that' 'subjrel_that_V1' 'objrel_that' 'objrel_that_V1' 'nounpp_copula_number';  
#for NATASK in  'objrel_that' 'objrel_that_V1' 'objrel_that_capitalized' 'objrel_that_V1_capitalized';  
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
            eval 'python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_'$NATASK'_4000.abl -info ../Data/Stimuli/Italian_'$NATASK'_4000.info -condition number_1='$NUMBER' number_2='$ATTRACTOR
        done
    done
done
