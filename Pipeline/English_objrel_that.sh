Code/Stimuli/Relative_clause_Marco/generate_relatives.pl 1 500 objrel_that > Data/Stimuli/objrel_that.txt 


python3 Code/Stimuli/Relative_clause_Marco/generate_info_from_raw_txt.py -i Data/Stimuli/objrel_that.txt -o Data/Stimuli/objrel_that


python3 Code/LSTM/model-analysis/extract-activations.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.pt --input Data/Stimuli/objrel_that.text --vocabulary Data/LSTM/english_vocab.txt --output Data/LSTM/objrel_that --eos-separator "<eos>" --format pkl --use-unk --unk-token "<unk>" --lang en -g lstm --cuda


python3 Code/LSTM/model-analysis/ablation-experiment.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.pt --input Data/Stimuli/objrel_that --vocabulary Data/LSTM/english_vocab.txt --output Output/objrel_that --eos-separator "<eos>" --format pkl -u 1 -u 750 -g 1 -s 1 --cuda


python3 Code/Stimuli/Relative_clause_Marco/add_success_and_perplexity_to_info.py -i Data/Stimuli/objrel_that.info -r Output/objrel_that.abl -a Data/LSTM/objrel_that.pkl


