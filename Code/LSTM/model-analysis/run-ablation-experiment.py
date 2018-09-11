import os

# Paths
script = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py'
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model.tab'
vocab = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_'
eos = '"<eos>"'
format = 'pkl'
seed = 1 # random seed for numpy
unit_to_kill = 1 # unit number (counting from one!)
g = 1 # group size of units to kill in including random ones

cmd = script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                    ' --eos-separator ' + eos + ' --format ' + format + ' -u ' + str(unit_to_kill) + ' -g '\
      + str(g) + ' -s ' + str(seed)
print(cmd)
# os.system(cmd)

