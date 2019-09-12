#!/bin/bash 

for NATASK in 'nounpp_copula_gender';
do
    #echo 'Number-agreement task: '$NATASK
    # Calculate accuracies (without ablation)
    # Calc accuracy for each condition (SS/SP/PS/PP)
    for NUMBER in 'masculine' 'feminine';
    do
        for ATTRACTOR in 'masculine' 'feminine';
        do
            echo
            eval 'python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_'$NATASK'_4000.abl -info ../Data/Stimuli/Italian_'$NATASK'_4000.info -condition gender_1='$NUMBER' gender_2='$ATTRACTOR
        done
    done
done
