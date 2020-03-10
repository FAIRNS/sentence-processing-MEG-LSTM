#!/bin/bash
NUM_STIMULI=4000
for NATASK in 'nounpp_copula_gender';
do
    for UNIT in '1099' # '970' '859' '703' '814' '1123' ;
    do

        eval 'python3 ../Code/LSTM/model-analysis/plot_units_activations.py -sentences ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.text -meta ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.info -activations ../Data/LSTM/activations/Italian/'$NATASK'.pkl -o ../Figures/Italian_'$NATASK'_'$UNIT'.png -c nounpp_copula -g 1 m \- 6 '$UNIT' cell gender_1 masculine gender_2 masculine -g 1 m "\--" 6 '$UNIT' cell gender_1 masculine gender_2 feminine -g 1 c \- 6 '$UNIT' cell gender_1 feminine gender_2 feminine -g 1 c "\--" 6 '$UNIT' cell gender_1 feminine gender_2 masculine -y "\$C\_t\$" --no-legend --figheight 4 --figwidth 16'

    
    #echo 'python3 ../Code/LSTM/model-analysis/plot_units_activations.py -sentences ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.text -meta ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.info -activations ../Data/LSTM/activations/Italian/'$NATASK'.pkl -o ../Figures/Italian_'$NATASK'_'$UNIT'.png -c nounpp_copula -g 1 r \- 2 '$UNIT' gates.c_tilde gender_1 masculine gender_2 masculine  -g 1 r "\--" 2 '$UNIT' gates.c_tilde gender_1 masculine gender_2 feminine  -g 1 b "\--" 2 '$UNIT' gates.c_tilde gender_1 feminine gender_2 masculine  -g 1 b \- 2 '$UNIT' gates.c_tilde gender_1 feminine gender_2 feminine  -g 2 r \- 2 '$UNIT' gates.in gender_1 masculine gender_2 masculine  -g 2 r "\--" 2 '$UNIT' gates.in gender_1 masculine gender_2 feminine  -g 2 b "\--" 2 '$UNIT' gates.in gender_1 feminine gender_2 masculine  -g 2 b \- 2 '$UNIT' gates.in gender_1 feminine gender_2 feminine  -g 3 r \- 2 '$UNIT' gates.forget gender_1 masculine gender_2 masculine  -g 3 r "\--" 2 '$UNIT' gates.forget gender_1 masculine gender_2 feminine  -g 3 b "\--" 2 '$UNIT' gates.forget gender_1 feminine gender_2 masculine  -g 3 b \- 2 '$UNIT' gates.forget gender_1 feminine gender_2 feminine  -g 4 r "\--" 2 '$UNIT' cell gender_1 masculine gender_2 feminine  -g 4 b "\--" 2 '$UNIT' cell gender_1 feminine gender_2 masculine  -g 4 b \- 2 '$UNIT' cell gender_1 feminine gender_2 feminine -g 4 r \- 2 '$UNIT' cell gender_1 masculine gender_2 masculine -g 5 r "\--" 2 '$UNIT' hidden gender_1 masculine gender_2 feminine  -g 5 b "\--" 2 '$UNIT' hidden gender_1 feminine gender_2 masculine  -g 5 b \- 2 '$UNIT' hidden gender_1 feminine gender_2 feminine -g 5 r \- 2 '$UNIT' hidden gender_1 masculine gender_2 masculine -y "$\tilde{C_t}$" "\$i\_t\$" "\$f\_t\$" "\$C\_t\$" "\$h\_t\$" --no-legend'

    done
done
