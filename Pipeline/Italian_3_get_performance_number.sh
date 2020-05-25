#!/bin/bash

for NATASK in  'nounpp' 'objrel_that_V2' 'objrel_that_V1' 'sc_short_V1'
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

# python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_double_subjrel_V1.abl -info ../Data/Stimuli/Italian_double_subjrel_V1.info -condition number_1=singular number_2=singular
# python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_double_subjrel_V1.abl -info ../Data/Stimuli/Italian_double_subjrel_V1.info -condition number_1=singular number_2=plural
# python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_double_subjrel_V1.abl -info ../Data/Stimuli/Italian_double_subjrel_V1.info -condition number_1=plural number_2=singular
# python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_double_subjrel_V1.abl -info ../Data/Stimuli/Italian_double_subjrel_V1.info -condition number_1=plural number_2=plural
