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

###### PCA ###########
# PCA - LSTM hidden states (h)
alu.plot_PCA_trajectories('hidden', LSTM_and_baselines_data['hidden'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline (kbow: bag-of-(last k)-words of nomalized word embeddings)
alu.plot_PCA_trajectories('norm_kbow_vectors', LSTM_and_baselines_data['norm_kbow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline (kbow: bag-of-(last k)-words of word embeddings)
alu.plot_PCA_trajectories('kbow_vectors', LSTM_and_baselines_data['kbow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# # PCA - LSTM cell memory (c)
alu.plot_PCA_trajectories('cell', LSTM_and_baselines_data['cell'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline3 (normalized word-embedding vectors)
alu.plot_PCA_trajectories('norm_word_vectors', LSTM_and_baselines_data['norm_word_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline2 (bag-of-words of nomalized word embeddings)
alu.plot_PCA_trajectories('norm_bow_vectors', LSTM_and_baselines_data['norm_bow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline1 (word-embedding vectors)
alu.plot_PCA_trajectories('word_vectors', LSTM_and_baselines_data['word_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - baseline2 (bag-of-words of word embeddings)
alu.plot_PCA_trajectories('bow_vectors', LSTM_and_baselines_data['bow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

# PCA - LSTM hidden + memory ([h, c])
# alu.plot_PCA_trajectories(LSTM_and_baselines_data, all_stim_clean, IX_structures, labels, colors, settings, params)

# fig, fig_tuples = alu.plot_PCA_trajectories(LSTM_data[:,0:1000,:], IX_structures, labels, colors, settings, params)
# file_name = 'PCA_LSTM_h_' + settings.patient + settings.LSTM_file_name + '.png'
# plt.figure(fig.number); plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
# plt.figure(fig_tuples.number); plt.savefig(op.join(settings.path2figures, 'units_activation', 'tuples_' + file_name))

# fig, fig_tuples =  alu.plot_PCA_trajectories(LSTM_data[:, 1000:2001,:], IX_structures, labels, colors, settings, params)
# file_name = 'PCA_LSTM_c_' + settings.patient + settings.LSTM_file_name + '.png'
# plt.figure(fig.number); plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
# plt.figure(fig_tuples.number); plt.savefig(op.join(settings.path2figures, 'units_activation', 'tuples_' + file_name))

# file_name = 'PCA_LSTM_h_c_' + settings.patient + settings.LSTM_file_name + '.png'
# plt.figure(fig.number); plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
# plt.figure(fig_tuples.number); plt.savefig(op.join(settings.path2figures, 'units_activation', 'tuples_' + file_name))

# file_name = 'PCA_word_vectors_' + settings.patient + settings.LSTM_file_name + '.png'
# plt.figure(fig.number); plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
# plt.figure(fig_tuples.number); plt.savefig(op.join(settings.path2figures, 'units_activation', 'tuples_' + file_name))

# file_name = 'PCA_word_vectors_BOW_' + settings.patient + settings.LSTM_file_name + '.png'
# plt.figure(fig.number); plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
# plt.figure(fig_tuples.number); plt.savefig(op.join(settings.path2figures, 'units_activation', 'tuples_' + file_name))

# Split according to structures (structure = 1 is 4x4; 2 is 2x6; 3 is 6x2)
# alu.plot_units_activation(LSTM_data, labels, IX_structures, settings, params)

#
# word_vectors_data = np.load(op.join(settings.path2LSTMdata, settings.word_vectors_file_name))
# word_vectors_BOW_data = np.load(op.join(settings.path2LSTMdata, settings.word_vectors_BOW_file_name))
