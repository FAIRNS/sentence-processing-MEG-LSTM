#!/bin/bash -x

#for NATASK in 'nounpp' 'subjrel' 'objrel';
#for NATASK in 'objrel_that_V1' 'objrel_that_V2' 'objrel_nounpp_V1' 'objrel_nounpp_V2';
#for NATASK in 'objrel_nounpp_V1' 'objrel_nounpp';
#for NATASK in 'embedding_mental_SR'
for NATASK in 'simple_non'
    #'objrel_nounpp';
do
   eval 'python3 ../Code/LSTM/model-analysis/extract-activations.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_512.text -v ../Data/LSTM/models/Italian_vocab.txt -o ../Data/LSTM/activations/Italian/'$NATASK' --eos-separator "<eos>" --cuda --lang it --use-unk --uppercase-first-word'
   #eval 'python3 ../Code/LSTM/model-analysis/extract-activations.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_'$NATASK'_4032.text -v ../Data/LSTM/models/Italian_vocab.txt -o ../Data/LSTM/activations/Italian/'$NATASK' --eos-separator "<eos>" --cuda --lang it --use-unk --uppercase-first-word'
done

# python3 ../Code/LSTM/model-analysis/extract-activations.py ../Data/LSTM/models/Italian_hidden650_batch64_dropout0.2_lr20.0.pt -i ../Data/Stimuli/Italian_double_subjrel_V1.text -v ../Data/LSTM/models/Italian_vocab.txt -o ../Data/LSTM/activations/Italian/Italian_double_subjrel_V1 --eos-separator "<eos>" --cuda --lang it --use-unk --uppercase-first-word
