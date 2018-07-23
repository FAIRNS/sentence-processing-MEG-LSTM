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
print('PCA - LSTM hidden states (h)')
alu.plot_PCA_trajectories('hidden', LSTM_and_baselines_data['hidden'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline (kbow: bag-of-(last k)-words of nomalized word embeddings)')
alu.plot_PCA_trajectories('norm_kbow_vectors', LSTM_and_baselines_data['norm_kbow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline (kbow: bag-of-(last k)-words of word embeddings)')
alu.plot_PCA_trajectories('kbow_vectors', LSTM_and_baselines_data['kbow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - LSTM cell memory (c)')
alu.plot_PCA_trajectories('cell', LSTM_and_baselines_data['cell'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline3 (normalized word-embedding vectors)')
alu.plot_PCA_trajectories('norm_word_vectors', LSTM_and_baselines_data['norm_word_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline2 (bag-of-words of nomalized word embeddings)')
alu.plot_PCA_trajectories('norm_bow_vectors', LSTM_and_baselines_data['norm_bow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline1 (word-embedding vectors)')
alu.plot_PCA_trajectories('word_vectors', LSTM_and_baselines_data['word_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

print('PCA - baseline2 (bag-of-words of word embeddings)')
alu.plot_PCA_trajectories('bow_vectors', LSTM_and_baselines_data['bow_vectors'], all_stim_clean, IX_structures, labels, colors, settings, params)

