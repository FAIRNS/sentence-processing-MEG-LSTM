#!/bin/bash -x

#for NATASK in 'nounpp' 'subjrel' 'objrel';
for NATASK in 'objrel_that_V1' 'objrel_that_V2' 'subjrel_that_V1' 'subjrel_that_V2';
do
   eval 'python3 ../Code/LSTM/model-analysis/extract-activations.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_4000.text -v ../Data/LSTM/models/Italian_vocab.txt -o ../Data/LSTM/activations/Italian/'$NATASK' --eos-separator "<eos>" --cuda --lang it --use-unk --uppercase-first-word'
   #eval 'python3 ../Code/LSTM/model-analysis/extract-activations.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_4032.text -v ../Data/LSTM/models/Italian_vocab.txt -o ../Data/LSTM/activations/Italian/'$NATASK' --eos-separator "<eos>" --cuda --lang it --use-unk'
done

