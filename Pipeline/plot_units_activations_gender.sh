#!/bin/bash

echo "choose task (e.g., nounpp, subjrel_that)"
read NATASK

echo "what is the number of stimuli (should appear in file names of Linzen-like files)"
read NUM_STIMULI

echo "For which unit to plot (counting from ZERO!)"
read UNIT

eval 'python3 ../Code/LSTM/model-analysis/plot_units_activations.py -sentences ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.text -meta ../Data/Stimuli/Italian_'$NATASK'_'$NUM_STIMULI'.info -activations ../Data/LSTM/activations/Italian/'$NATASK'.pkl -o ../Figures/Italian_'$NATASK'_'$UNIT'.png -c nounpp_copula -g 1 r \- 2 '$UNIT' gates.c_tilde gender_1 masculine gender_2 masculine  -g 1 r "\--" 2 '$UNIT' gates.c_tilde gender_1 masculine gender_2 feminine  -g 1 b "\--" 2 '$UNIT' gates.c_tilde gender_1 feminine gender_2 masculine  -g 1 b \- 2 '$UNIT' gates.c_tilde gender_1 feminine gender_2 feminine  -g 2 r \- 2 '$UNIT' gates.in gender_1 masculine gender_2 masculine  -g 2 r "\--" 2 '$UNIT' gates.in gender_1 masculine gender_2 feminine  -g 2 b "\--" 2 '$UNIT' gates.in gender_1 feminine gender_2 masculine  -g 2 b \- 2 '$UNIT' gates.in gender_1 feminine gender_2 feminine  -g 3 r \- 2 '$UNIT' gates.forget gender_1 masculine gender_2 masculine  -g 3 r "\--" 2 '$UNIT' gates.forget gender_1 masculine gender_2 feminine  -g 3 b "\--" 2 '$UNIT' gates.forget gender_1 feminine gender_2 masculine  -g 3 b \- 2 '$UNIT' gates.forget gender_1 feminine gender_2 feminine  -g 4 r "\--" 2 '$UNIT' cell gender_1 masculine gender_2 feminine  -g 4 b "\--" 2 '$UNIT' cell gender_1 feminine gender_2 masculine  -g 4 b \- 2 '$UNIT' cell gender_1 feminine gender_2 feminine -g 4 r \- 2 '$UNIT' cell gender_1 masculine gender_2 masculine -g 5 r "\--" 2 '$UNIT' hidden gender_1 masculine gender_2 feminine  -g 5 b "\--" 2 '$UNIT' hidden gender_1 feminine gender_2 masculine  -g 5 b \- 2 '$UNIT' hidden gender_1 feminine gender_2 feminine -g 5 r \- 2 '$UNIT' hidden gender_1 masculine gender_2 masculine -y "$\tilde{C_t}$" "\$i\_t\$" "\$f\_t\$" "\$C\_t\$" "\$h\_t\$" --no-legend'

