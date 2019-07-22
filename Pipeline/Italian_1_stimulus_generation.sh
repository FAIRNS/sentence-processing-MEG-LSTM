#!/bin/bash 
#for NATASK in 'nounpp' 'subjrel_that' 'objrel_that'
for NATASK in 'nounpp';
do
    TEST_WORD_POSITION=6
    WRONG_WORD_LABEL='verb_2_wrong'
    IX="-2"
    V2=" -p verb_2_wrong 7"
    if [ "$NATASK" == "nounpp" ] ;then
        IX="-1"
        V2=""
        TEST_WORD_POSITION=5
        WRONG_WORD_LABEL='verb_1_wrong'
    fi
    # ---------------------
    # Execute pipeline steps
    # ----------------------
    # 1. Generate all possible stimuli from lexicon
    echo 'Generating data...'
    eval 'python3 ../Code/Stimuli/Italian/NA_tasks_generator.py --natask '$NATASK' > ../Data/Stimuli/Italian_'$NATASK'.txt'
    # 2. Subsample 4000 stimuli
    echo
    echo 'Subsampling data...'
    eval 'python3 ../Code/Stimuli/Italian/subsample_dataset.py -f ../Data/Stimuli/Italian_'$NATASK'.txt -n 250 -seed 1 --IX-last '$IX' > ../Data/Stimuli/Italian_'$NATASK'_4000.txt'
    # 3. Sanity check: verify and print to screen feature distriution
    echo
    echo 'Test:'
    eval 'python3 ../Code/Stimuli/Italian/verify_stimuli_file_is_balanced.py -f ../Data/Stimuli/Italian_'$NATASK'_4000.txt'
    # 4. Prepare in Linzen's format and generate an info pkl file
    echo
    echo 'Transform to Linzen format'
    eval 'python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_'$NATASK'_4000.txt -o ../Data/Stimuli/Italian_'$NATASK'_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6'$V2' --correct-word-position '$TEST_WORD_POSITION' --wrong-word-label '$WRONG_WORD_LABEL
done


####################
### FOR V1     #####
####################
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_subjrel_that_4000.txt -o ../Data/Stimuli/Italian_subjrel_that_V1_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 3 --wrong-word-label verb_1_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_that_4000.txt -o ../Data/Stimuli/Italian_objrel_that_V1_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 5 --wrong-word-label verb_1_wrong



######################################
### FOR objrel_nounpp V1 and V2  #####
######################################
######
# objrel_nounpp   il bambino che il contadino accanto ai padri guarda conosce i   masculine   singular    masculine   singular    masculine   plural  guardano    conoscono
######
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_nounpp_4032.txt -o ../Data/Stimuli/Italian_objrel_nounpp_V1_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 8 --wrong-word-label verb_1_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_nounpp_4032.txt -o ../Data/Stimuli/Italian_objrel_nounpp_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong


######################################
### FOR nounpp_objrel V1 and V2  #####
######################################
######
# nounpp_objrel   il bambino accanto al padri che il contadino guarda conosce i   masculine   singular    masculine   plural    masculine   singular  guardano    conoscono
######
# python3 ../Code/Stimuli/Italian/NA_tasks_generator.py --natask nounpp_objrel > ../Data/Stimuli/Italian_nounpp_objrel.txt
# python3 ../Code/Stimuli/Italian/subsample_dataset_two_attractors.py -f ../Data/Stimuli/Italian_nounpp_objrel.txt -n 63 -seed 1 --IX-last -2 --max-iter 50 > ../Data/Stimuli/Italian_nounpp_objrel_4032.txt
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_objrel_4032.txt -o ../Data/Stimuli/Italian_nounpp_objrel_V1_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 8 --wrong-word-label verb_1_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_objrel_4032.txt -o ../Data/Stimuli/Italian_nounpp_objrel_V1_capitalized_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 8 --wrong-word-label verb_1_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_objrel_4032.txt -o ../Data/Stimuli/Italian_nounpp_objrel_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_objrel_4032.txt -o ../Data/Stimuli/Italian_nounpp_objrel_capitalized_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong



######################################
### FOR embedding_mental         #####
######################################
# python3 ../Code/Stimuli/Italian/NA_tasks_generator.py -t embedding_mental -n 63 > ../Data/Stimuli/Italian_embedding_mental_4032.txt
# python3 ../Code/Stimuli/Italian/verify_stimuli_file_is_balanced.py -f ../Data/Stimuli/Italian_embedding_mental_4032.txt > ../Data/Stimuli/Italian_embedding_mental_4032.log
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_embedding_mental_4032.txt -o ../Data/Stimuli/Italian_embedding_mental_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong

######################################
### FOR embedding_mental SR      #####
######################################
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_embedding_mental_SR_4000.txt -o ../Data/Stimuli/Italian_embedding_mental_SR_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 6 --wrong-word-label verb_2_wrong


####################
### FOR GENDER #####
####################
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_copula_4000.txt -o ../Data/Stimuli/Italian_nounpp_copula_number_4000 -p number_1 3 -p gender_1 2 -p number_2 5 -p gender_2 4 -p verb_1_wrong 6 -p adj_1_wrong 7 --correct-word-position 5 --wrong-word-label verb_1_wrong
# python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_nounpp_copula_4000.txt -o ../Data/Stimuli/Italian_nounpp_copula_gender_4000 -p number_1 3 -p gender_1 2 -p number_2 5 -p gender_2 4 -p verb_1_wrong 6 -p adj_1_wrong 7 --correct-word-position 6 --wrong-word-label adj_1_wrong
