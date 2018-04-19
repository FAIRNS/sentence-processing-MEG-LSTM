script = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py'
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
input_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/NP_VP_transition.txt'
vocab = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/NP_VP_transition.pkl'
eos = '"<eos>"'
format = 'pkl'
get_representations = 'LSTM'

cmd = 'python3 ' + script + ' ' + model + ' --input ' + input_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                    ' --eos-separator ' + eos + ' --format ' + format + ' --get-representations ' + 'lstm'

print(cmd)