#!/bin/bash

# $1 prefix of input gold and text files, to _number (excluding that
# $2 output directory
# $3 if defined, we expect combinations of plural and singular as number (plural_singular, etc)

if [ "$3" != "" ]; then
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_singular_singular_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/singular_singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_singular_plural_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/singular_plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_plural_plural_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/plural_plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_plural_singular_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/plural_singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
else
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_singular_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/singular --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
    for unit in {1..1300}
    do
	echo python3 /private/home/mbaroni/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py /private/home/mbaroni/relative_clauses/hidden650_batch128_dropout0.2_lr20.0.pt --input $1_plural_sentences --vocabulary /private/home/mbaroni/relative_clauses/vocab.txt --output $2/plural --eos-separator \"\<eos\>\" --format pkl -u $unit -g 1 --use-unk --s 111 --cuda --do-ablation
    done
fi

