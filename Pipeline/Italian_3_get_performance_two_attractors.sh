#!/bin/bash
#NATASK=objrel_nounpp_V1

#for NATASK in 'objrel_nounpp' 'objrel_nounpp_V1' 'objrel_nounpp_capitalized' 'objrel_nounpp_V1_capitalized';  
#for NATASK in 'objrel_nounpp_capitalized' 'objrel_nounpp_V1_capitalized';  
for NATASK in 'embedding_mental';
do
    echo '---------------------------------------------------------'
    echo $NATASK
    echo '---------------------------------------------------------'
    for NUMBER in 'singular' 'plural';
    do
        for ATTRACTOR1 in 'singular' 'plural';
        do
            for ATTRACTOR2 in 'singular' 'plural';
            do

                echo $NUMBER $ATTRACTOR1 $ATTRACTOR2
                eval 'python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/Italian_'$NATASK'_4032.abl -info ../Data/Stimuli/Italian_'$NATASK'_4032.info -condition number_1='$NUMBER' number_2='$ATTRACTOR1' number_3='$ATTRACTOR2
            done
        done
    done
done
