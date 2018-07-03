import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import matplotlib.pyplot as plt
import pickle

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

###### LOAD ############
# Load stimuli in groups according to struct
print('loading info file ' + settings.stimuli_meta_data)
all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors = alu.get_stimuli_and_info(settings, params)

# Load LSTM data
print('Loading pre-trained LSTM data...')
with open(op.join(settings.path2LSTMdata, settings.LSTM_file_name), 'rb') as f:
    print(op.join(settings.path2LSTMdata, settings.LSTM_file_name))
    LSTM_and_baselines_data = pickle.load(f)
# LSTM_data = [item for i, item in enumerate(LSTM_data) if i in range(100)]
units = [950, 373, 984, 932, 179, 697, 924, 396, 554, 94,
                 552, 726, 612, 969, 731, 478, 733, 178, 604, 588]
for IX_structure, label in zip(IX_structures, labels):
    print(label)
    LSTM_and_baselines_data_curr_structure = {}
    for key in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']:
       LSTM_and_baselines_data_curr_structure[key] = [sentence_matrix for ind, sentence_matrix in enumerate(LSTM_and_baselines_data[key]) if ind in IX_structure]
    curr_stimuli = [sentence for ind, sentence in enumerate(all_stim_clean) if ind in IX_structure]
    alu.plot_units_activation(LSTM_and_baselines_data_curr_structure, label, curr_stimuli, units, settings, params)
