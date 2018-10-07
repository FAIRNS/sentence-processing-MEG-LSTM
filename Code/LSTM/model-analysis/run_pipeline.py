import argparse
parser = argparse.ArgumentParser(description='Run pipeline from generating stimuli to visualize activation plots')
parser.add_argument('-c', '--condition', type=str, help='Condition for which to generate stimuli. E.g., objrel, subjrel_that (based on Marco script)')
parser.add_argument('-n', '--num_stimuli', type=str, help='Num of stimuli for current Condition')
args = parser.parse_args()

print('Code/Stimuli/Relative_clause_Marco/generate_relatives.pl 1 %s %s > Data/Stimuli/%s.txt \n\n' % (args.num_stimuli, args.condition, args.condition))

print('python3 Code/Stimuli/Relative_clause_Marco/generate_info_from_raw_txt.py -i Data/Stimuli/%s.txt -o Data/Stimuli/%s\n\n' % (args.condition, args.condition))

print('python3 Code/LSTM/model-analysis/extract-activations.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt --input Data/Stimuli/%s.text --vocabulary Data/LSTM/english_vocab.txt --output Data/LSTM/%s --eos-separator "<eos>" --format pkl --use-unk --unk-token "<unk>" --lang en -g lstm\n\n' % (args.condition, args.condition))

print('python3 Code/LSTM/model-analysis/ablation-experiment.py Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt --input Data/Stimuli/%s --vocabulary Data/LSTM/english_vocab.txt --output Output/%s --eos-separator "<eos>" --format pkl -u 1 -u 750 -g 1 -s 1\n\n' % (args.condition, args.condition))

print('python3 Code/Stimuli/Relative_clause_Marco/add_success_and_perplexity_to_info.py -i Data/Stimuli/%s.info -r Output/%s.abl -a Data/LSTM/%s.pkl\n\n' % (args.condition, args.condition, args.condition))

