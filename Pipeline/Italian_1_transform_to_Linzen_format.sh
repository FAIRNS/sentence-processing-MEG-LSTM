# This script transforms the output from the NA_task_generator into Linzen's format.

echo "OBJREL-SHORT V1 (main)"
python ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_that_4000.txt -o ../Data/Stimuli/Italian_objrel_that_V1_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 6 --wrong-word-label verb_2_wrong -s objrel_short_V1

echo "OBJREL-SHORT V2 (embedded)"
python ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_that_4000.txt -o ../Data/Stimuli/Italian_objrel_that_V2_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 5 --wrong-word-label verb_1_wrong -s objrel_short_V2

echo "OBJREL-LONG V1 (main)"
python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_nounpp_4032.txt -o ../Data/Stimuli/Italian_objrel_nounpp_V1_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong -s objrel_long_V1

echo "OBJREL-LONG V2 (main)"
python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_objrel_nounpp_4032.txt -o ../Data/Stimuli/Italian_objrel_nounpp_V2_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 8 --wrong-word-label verb_1_wrong -s objrel_long_V2

echo "SC-SHORT V1 (main)"
python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_embedding_mental_SR_4000.txt -o ../Data/Stimuli/Italian_sc_short_V1_4000 -p number_1 3 -p number_2 5 -p verb_1_wrong 6 -p verb_2_wrong 7 --correct-word-position 6 --wrong-word-label verb_2_wrong -s sc_short_V1

echo "SC-LONG V1 (main)"
python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/Italian_embedding_mental_4032.txt -o ../Data/Stimuli/Italian_sc_long_V1_4032 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 8 -p verb_2_wrong 9 --correct-word-position 9 --wrong-word-label verb_2_wrong -s sc_long_V1

