# V1 is the outermost verb, V3 is the innermost.

# GENERATE STIMULI
python ../Code/Stimuli/English_Yair/NA_tasks_generator.py --natask OR_OR -seed 1 -n 256 > ../Data/Stimuli/English_OR_OR.txt

# TRANSFORM TO LINZEN FORMAT
python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/English_OR_OR.txt -o ../Data/Stimuli/English_OR_OR_V1 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 10 -p verb_2_wrong 11 -p verb_3_wrong 12 --correct-word-position 10 --wrong-word-label verb_1_wrong

python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/English_OR_OR.txt -o ../Data/Stimuli/English_OR_OR_V2 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 10 -p verb_2_wrong 11 -p verb_3_wrong 12 --correct-word-position 9 --wrong-word-label verb_2_wrong

python3 ../Code/Stimuli/generate_info_from_raw_txt.py -i ../Data/Stimuli/English_OR_OR.txt -o ../Data/Stimuli/English_OR_OR_V3 -p number_1 3 -p number_2 5 -p number_3 7 -p verb_1_wrong 10 -p verb_2_wrong 11 -p verb_3_wrong 12 --correct-word-position 8 --wrong-word-label verb_3_wrong

# EXTRACT PREDICTIONS
python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt -i ../Data/Stimuli/English_OR_OR_V1 -v ../Data/LSTM/models/english/english_vocab.txt -o ../Output/English_OR_OR_V1 --eos-separator "<eos>" --format pkl --lang en --uppercase-first-word &

python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt -i ../Data/Stimuli/English_OR_OR_V2 -v ../Data/LSTM/models/english/english_vocab.txt -o ../Output/English_OR_OR_V2 --eos-separator "<eos>" --format pkl --lang en --uppercase-first-word &

python3 ../Code/LSTM/model-analysis/extract_predictions.py ../Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt -i ../Data/Stimuli/English_OR_OR_V3 -v ../Data/LSTM/models/english/english_vocab.txt -o ../Output/English_OR_OR_V3 --eos-separator "<eos>" --format pkl --lang en --uppercase-first-word &

#python3 Code/LSTM/model-analysis/extract-activations.py Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt --input Data/Stimuli/English_objrel_pronoun_V1.text --vocabulary Data/LSTM/models/english/english_vocab.txt --output Data/LSTM/English_objrel_pronoun_V1 --eos-separator <eos> --format pkl --use-unk --unk-token <unk> --lang en -g lstm --cuda

#python Code/Stimuli/English/NA_tasks/add_success_and_perplexity_to_info.py -i Data/Stimuli/English_objrel_pronoun_V1.info -r Output/English_objrel_pronoun_V1.abl -a Data/LSTM/English_objrel_pronoun_V1.pkl

#python Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/English_objrel_pronoun_V1.text -meta Data/Stimuli/English_objrel_pronoun_V1.info -activations Data/LSTM/English_objrel_pronoun_V1.pkl -o Figures/English_objrel_pronoun_775.png -c objrel_pronoun -g 4 r - 6 775 cell number_1 singular number_2 singular success correct -g 1 r - 6 775 gates.c_tilde number_1 singular number_2 singular success correct -g 1 r \-- 6 775 gates.c_tilde number_1 singular number_2 plural success correct -g 1 b \-- 6 775 gates.c_tilde number_1 plural number_2 singular success correct -g 1 b - 6 775 gates.c_tilde number_1 plural number_2 plural success correct -g 2 r - 6 775 gates.in number_1 singular number_2 singular success correct -g 2 r \-- 6 775 gates.in number_1 singular number_2 plural success correct -g 2 b \-- 6 775 gates.in number_1 plural number_2 singular success correct -g 2 b - 6 775 gates.in number_1 plural number_2 plural success correct -g 3 r - 6 775 gates.forget number_1 singular number_2 singular success correct -g 3 r \-- 6 775 gates.forget number_1 singular number_2 plural success correct -g 3 b \-- 6 775 gates.forget number_1 plural number_2 singular success correct -g 3 b - 6 775 gates.forget number_1 plural number_2 plural success correct -g 4 r \-- 6 775 cell number_1 singular number_2 plural success correct -g 4 b \-- 6 775 cell number_1 plural number_2 singular success correct -g 4 b - 6 775 cell number_1 plural number_2 plural success correct -g 5 r - 6 775 gates.out number_1 singular number_2 singular success correct -g 5 r \-- 6 775 gates.out number_1 singular number_2 plural success correct -g 5 b \-- 6 775 gates.out number_1 plural number_2 singular success correct -g 5 b - 6 775 gates.out number_1 plural number_2 plural success correct -x The boy(s) that (s)he greet(s) run(s) away -y $\tilde{C_t}$ $i\_t$ $f\_t$ $C\_t$ $o\_t$ --no-legend --facecolor w

