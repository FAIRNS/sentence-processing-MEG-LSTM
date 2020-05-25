#!/bin/bash

#for NATASK in 'objrel_nounpp_V1' 'objrel_nounpp_V2' 'embedding_mental_V1' 'embedding_mental_V2'; # 'embedding_mental_2LRs_V1' 'embedding_mental_2LRs_V2';
echo 'sentence_type,keys,condition,accuracy'
for NATASK in 'SC_OR_V1' 'SC_OR_V2' 'SC_OR_V3' 'OR_OR_V1' 'OR_OR_V2' 'OR_OR_V3'
do
    #echo '-------------------------------'
    #echo 'Number-agreement task: '$NATASK
    #echo '-------------------------------'
    # Calculate accuracies (without ablation)
    # Calc accuracy for each condition (SS/SP/PS/PP)
    for NUMBER in 'singular' 'plural';
    do
		for ATTRACTOR1 in 'singular' 'plural';
		do
			for ATTRACTOR2 in 'singular' 'plural';
			do

			#echo
			eval 'python3 ../Code/LSTM/model-analysis/get_agreement_accuracy_for_contrast.py -ablation-results ../Output/English_'$NATASK'.abl -info ../Data/Stimuli/English_'$NATASK'.info -condition number_1='$NUMBER' number_2='$ATTRACTOR1' number_3='$ATTRACTOR2
			done
        done
    done
done
