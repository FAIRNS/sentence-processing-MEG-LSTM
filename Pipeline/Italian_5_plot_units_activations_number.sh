#!/bin/bash -x
#for NATASK in 'nounpp' 'subjrel_that' 'objrel_that';
NUM_STIMULI=4000
for NATASK in 'objrel_that_V1' 'objrel_that_V2' 'subjrel_that_V1' 'subjrel_that_V2';
do
    for UNIT in '814' '1064';
#    for UNIT in '1220' '758' '1126' '719' '1184' '1225';
#    for UNIT in '836' '1064'; #'650' '0' '610' '623' '680' '1091';
#    for UNIT in '1220' '1126' '650' '0' '610' '623' '680' '1091' '814' '1118' '859' '1225';
    #for UNIT in '204' '238' '244' '650' '690' '708' '987' '1012' '1064' '1091' '1167' '1218';
    do
        eval 'python3 ../Code/LSTM/model-analysis/plot_units_activations.py -sentences ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.text -meta ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.info -activations ../Data/LSTM/activations/Italian/'$NATASK'.pkl -o ../Figures/Italian_'$NATASK'_'$UNIT'.png -c '$NATASK' -g 1 r \- 2 '$UNIT' gates.c_tilde number_1 singular number_2 singular  -g 1 r "\--" 2 '$UNIT' gates.c_tilde number_1 singular number_2 plural  -g 1 b "\--" 2 '$UNIT' gates.c_tilde number_1 plural number_2 singular  -g 1 b \- 2 '$UNIT' gates.c_tilde number_1 plural number_2 plural  -g 2 r \- 2 '$UNIT' gates.in number_1 singular number_2 singular  -g 2 r "\--" 2 '$UNIT' gates.in number_1 singular number_2 plural  -g 2 b "\--" 2 '$UNIT' gates.in number_1 plural number_2 singular  -g 2 b \- 2 '$UNIT' gates.in number_1 plural number_2 plural  -g 3 r \- 2 '$UNIT' gates.forget number_1 singular number_2 singular  -g 3 r "\--" 2 '$UNIT' gates.forget number_1 singular number_2 plural  -g 3 b "\--" 2 '$UNIT' gates.forget number_1 plural number_2 singular  -g 3 b \- 2 '$UNIT' gates.forget number_1 plural number_2 plural  -g 4 r "\--" 2 '$UNIT' cell number_1 singular number_2 plural  -g 4 b "\--" 2 '$UNIT' cell number_1 plural number_2 singular  -g 4 b \- 2 '$UNIT' cell number_1 plural number_2 plural -g 4 r \- 2 '$UNIT' cell number_1 singular number_2 singular -g 5 r "\--" 2 '$UNIT' hidden number_1 singular number_2 plural  -g 5 b "\--" 2 '$UNIT' hidden number_1 plural number_2 singular  -g 5 b \- 2 '$UNIT' hidden number_1 plural number_2 plural -g 5 r \- 2 '$UNIT' hidden number_1 singular number_2 singular -y "$\tilde{C_t}$" "\$i\_t\$" "\$f\_t\$" "\$C\_t\$" "\$h\_t\$"'
    done
done
