#!/bin/bash

# path to self
MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# input corpus (for example, path to frwiki.txt)
INPUT=$1
# directory where to leave a post-processed train/val/test split
OUTPUT_DIR=$2

echo tokenize and separate in sentences
java -cp ${MYPATH}/../src/CoreNLP/stanford-corenlp.jar edu.stanford.nlp.international.french.process.FrenchTokenizer < $INPUT | \
    sed 's/ \(\.\) / \1\n/g' | \
    grep -v '^\s*$' > ${INPUT}.tok
echo compute word frequencies
<${INPUT}.tok awk '{a[$1]++}END{for(k in a)print a[k]"\t"k}' RS=" |\n"  | sort -nr > ${INPUT}.wfreq
echo extract a reduced set of the vocabulary
mkdir -p ${OUTPUT_DIR}
cat $MYPATH/stimuli-vocab.txt <(head -100000 ${INPUT}.wfreq | cut -f2) | sort -u > ${OUTPUT_DIR}/reduced-vocab.txt
sed -i '1i_UNK_' ${OUTPUT_DIR}/reduced-vocab.txt
sed -i '1i</s>' ${OUTPUT_DIR}/reduced-vocab.txt

echo shuffle and remove OOV words
shuf ${INPUT}.tok  | python mask_with_unk.py ${OUTPUT_DIR}/reduced-vocab.txt > ${OUTPUT_DIR}/full.txt
echo splitting data
./split-data.sh ${OUTPUT_DIR}/full.txt

