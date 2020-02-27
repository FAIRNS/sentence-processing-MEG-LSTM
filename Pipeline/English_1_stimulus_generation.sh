#!/bin/bash 
# ----------------------------
# Prepare in Linzen's format and generate an info pkl file
# ----------------------------
# All counts are from zero (python like)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!
# ---------
# In subjrel*:
# V1 is the main (last) verb
# V2 is the embedded (first) verb
# In objrel*:
# V1 is the main (outer) verb
# V2 is the embedded (inner) verb
# In embedding_mental*:
# V1 is the main (first) verb
# V2 is the embedded (second) verb

#for NATASK in 'objrel' 'objrel_nounpp' 'embedding_mental' 'embedding_mental_SR' 'embedding_mental_2LRs'
#for NATASK in 'objrel_pronoun'
for NATASK in 'subjrel'
do
    if [ "$NATASK" == "subjrel" ] ;then
        V1_NUM_FIELD=3
        V2_NUM_FIELD=3
        V1_POSITION=3
        V2_POSITION=6
        NUMBER_3=''
        NUMBER_4=''
    fi
    if [ "$NATASK" == "objrel" ] ;then
        V1_NUM_FIELD=8
        V2_NUM_FIELD=9
        V1_POSITION=6
        V2_POSITION=5
        NUMBER_3=''
        NUMBER_4=''
    fi
    if [ "$NATASK" == "objrel_pronoun" ] ;then
        V1_NUM_FIELD=8
        V2_NUM_FIELD=9
        V1_POSITION=5
        V2_POSITION=4
        NUMBER_3=''
        NUMBER_4=''
    fi
    if [ "$NATASK" == "objrel_nounpp" ] ;then
        V1_NUM_FIELD=8
        V2_NUM_FIELD=9
        V1_POSITION=9
        V2_POSITION=8
        NUMBER_3=' -p number_3 7'
        NUMBER_4=''
    fi
    if [ "$NATASK" == "embedding_mental_SR" ] ;then
        V1_NUM_FIELD=8
        V2_NUM_FIELD=9
        V1_POSITION=2
        V2_POSITION=6
        NUMBER_3=''
        NUMBER_4=''
    fi
    if [ "$NATASK" == "embedding_mental" ] ;then
        V1_NUM_FIELD=8
        V2_NUM_FIELD=9
        V1_POSITION=2
        V2_POSITION=9
        NUMBER_3=' -p number_3 7'
        NUMBER_4=''
    fi
    if [ "$NATASK" == "embedding_mental_2LRs" ] ;then
        V1_NUM_FIELD=10
        V2_NUM_FIELD=11
        V1_POSITION=5
        V2_POSITION=12
        NUMBER_3=' -p number_3 7'
        NUMBER_4=' -p number_4 9'
    fi

    echo
    echo 'Transform to Linzen format'
    
    eval 'python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/English_'$NATASK'.txt -o ../Data/Stimuli/English_'$NATASK'_V1 -p number_1 3 -p number_2 5'$NUMBER_3''$NUMBER_4' -p verb_1_wrong '$V1_NUM_FIELD' -p verb_2_wrong '$V2_NUM_FIELD' --correct-word-position '$V1_POSITION' --wrong-word-label verb_1_wrong'
    
    eval 'python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/English_'$NATASK'.txt -o ../Data/Stimuli/English_'$NATASK'_V2 -p number_1 3 -p number_2 5'$NUMBER_3''$NUMBER_4' -p verb_1_wrong '$V1_NUM_FIELD' -p verb_2_wrong '$V2_NUM_FIELD' --correct-word-position '$V2_POSITION' --wrong-word-label verb_2_wrong'
done
