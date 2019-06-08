#!/bin/bash

# $1 prefix of input gold and text files, to _number (excluding that
# $2 output directory
# $3 model_path
# $4 if defined, we expect combinations of plural and singular as number (plural_singular, etc)

ablation_script_path=~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py
#model_path=~/sentence-processing-MEG-LSTM/Code/models/hidden650-dropout0.4-lr20-batch_size128-emsize650.pt
model_path=$3
vocab_path$4
#=~/sentence-processing-MEG-LSTM/Code/data/vocab.txt

if [ "$5" != "" ]; then
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_singular_singular_sentences --vocabulary $vocab_path --output $2/singular_singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_singular_plural_sentences --vocabulary $vocab_path --output $2/singular_plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_plural_plural_sentences --vocabulary $vocab_path --output $2/plural_plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_plural_singular_sentences --vocabulary $vocab_path --output $2/plural_singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
else
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_singular_sentences --vocabulary $vocab_path --output $2/singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 $ablation_script_path $model_path --input $1_plural_sentences --vocabulary $vocab_path --output $2/plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
fi

