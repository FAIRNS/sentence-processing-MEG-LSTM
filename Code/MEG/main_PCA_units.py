import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import numpy as np
from functions import sentcomp_epoching
import matplotlib.pyplot as plt

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
labels = ['4-4', '2-6', '6-2']

# Load LSTM data
print('Loading pre-trained LSTM data...')
LSTM_data = np.load(op.join(settings.path2LSTMdata, settings.LSTM_file_name))
word_vectors_data = np.load(op.join(settings.path2LSTMdata, settings.word_vectors_file_name))
word_vectors_BOW_data = np.load(op.join(settings.path2LSTMdata, settings.word_vectors_BOW_file_name))

# Load stimuli in groups according to struct
all_stim_clean, all_info_clean, all_info_correct, IX_structure1, IX_structure2, IX_structure3 = alu.get_stimuli_and_info(settings, params)

# PCA - LSTM
fig = alu.plot_PCA_trajectories(LSTM_data, IX_structure1, IX_structure2, IX_structure3, settings, params)
file_name = 'PCA_LSTM_' + settings.patient + settings.LSTM_file_name + '.png'
plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))

# PCA - baseline1 (word-embedding vectors)
fig1 = alu.plot_PCA_trajectories(word_vectors_data, IX_structure1, IX_structure2, IX_structure3, settings, params)
file_name = 'PCA_word_vectors_' + settings.patient + settings.LSTM_file_name + '.png'
plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))

# PCA - baseline2 (bag-of-words of word embeddings)
fig2 = alu.plot_PCA_trajectories(word_vectors_BOW_data, IX_structure1, IX_structure2, IX_structure3, settings, params)
file_name = 'PCA_word_vectors_BOW_' + settings.patient + settings.LSTM_file_name + '.png'
plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))

# Split according to structures (structure = 1 is 4x4; 2 is 2x6; 3 is 6x2)
alu.plot_units_activation(LSTM_data, labels, IX_structure1, IX_structure2, IX_structure3, settings, params)
