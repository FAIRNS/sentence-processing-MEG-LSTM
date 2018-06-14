import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import matplotlib.pyplot as plt
import pickle

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

#
with open(op.join(settings.path2stimuli, settings.stimuli_file_name), 'r') as f:
    stimuli = [s[14::] for s in f.readlines()]

file_name = 'relative_clause_English.txt'
with open(op.join(settings.path2stimuli, file_name), 'w') as f:
    for stim in stimuli:
        f.write("%s" % stim)

# lengths = [len(stim.split(' ')) for stim in stimuli]
# plt.hist(lengths)
# plt.show()

info = []
for stim in range(len(stimuli)):
    d = {}
    d['NP_ends_with'] = 'noun'
    d['relative_clause'] = 'that'
    d['NP_length'] = 2
    d['VP_length'] = 4
    d['relative_clause_length'] = 4
    info.append(d)

info_file_name = 'info_RC_English.p'
with open(op.join(settings.path2stimuli, info_file_name), 'wb') as f:
    pickle.dump(info, f)