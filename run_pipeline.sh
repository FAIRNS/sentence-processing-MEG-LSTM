Code/Stimuli/Relative_clause_Marco/generate_relatives.pl 1 10 nounpp > Data/Stimuli/nounpp.txt 


python3 Code/Stimuli/Relative_clause_Marco/generate_info_from_raw_txt.py -i Data/Stimuli/nounpp.txt -o Data/Stimuli/nounpp


python3 Code/LSTM/model-analysis/extract-activations.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt --input Data/Stimuli/nounpp.text --vocabulary Data/LSTM/english_vocab.txt --output Data/LSTM/nounpp --eos-separator "<eos>" --format pkl --use-unk --unk-token "<unk>" --lang en -g lstm


python3 Code/LSTM/model-analysis/ablation-experiment.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt --input Data/Stimuli/nounpp --vocabulary Data/LSTM/english_vocab.txt --output Output/nounpp --eos-separator "<eos>" --format pkl -u 1 -u 750 -g 1 -s 1


python3 Code/Stimuli/Relative_clause_Marco/add_success_and_perplexity_to_info.py -i Data/Stimuli/nounpp.info -r Output/nounpp.abl -a Data/LSTM/nounpp.pkl


