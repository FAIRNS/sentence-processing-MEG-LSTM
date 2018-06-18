import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm
import numpy as np
# ------------------------------
vector_type = 'hidden'

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

# Load LSTM data
print('Loading pre-trained LSTM data...')
with open(op.join(settings.path2LSTMdata, settings.LSTM_file_name), 'rb') as f:
	LSTM_and_baselines_data = pickle.load(f)
data = LSTM_and_baselines_data[vector_type]
del LSTM_and_baselines_data

# Load stimuli in groups according to struct
all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors = alu.get_stimuli_and_info(settings, params)

# Load PCA data
file_name = 'PCA_LSTM_traject' + vector_type + settings.LSTM_file_name + '.pkl'
with open(op.join(settings.path2figures, 'units_activation', file_name), 'rb') as f:
	vectors_PCA_trajectories = pickle.load(f)

# calc dist per structure
print('After PCA: average across each syntactic structure type')
for i, IX_structure in enumerate(IX_structures):
	try:
		print(i)
		PCA2_Noun = []; PCA2_verb = []; PCA2_relativeNoun = []; PCA2_relativeVerb = []
		vectors_of_curr_structure = [vec for ind, vec in enumerate(vectors_PCA_trajectories) if ind in IX_structure]
		info_of_curr_structure = [i for ind, i in enumerate(all_info_correct) if ind in IX_structure]
		for i, curr_info in enumerate(info_of_curr_structure):
			curr_PoS = curr_info['PoS']
			IX_Noun = [IX for IX, pos in enumerate(curr_PoS) if pos == 'Noun']
			IX_verb = [IX for IX, pos in enumerate(curr_PoS) if pos == 'verb']
			IX_relativeNoun = [IX for IX, pos in enumerate(curr_PoS) if pos == 'relativeNoun']
			IX_relativeVerb = [IX for IX, pos in enumerate(curr_PoS) if pos == 'relativeVerb']
			PCA2_Noun.append(vectors_of_curr_structure[i][1, IX_Noun])
			PCA2_verb.append(vectors_of_curr_structure[i][1, IX_verb])
			PCA2_relativeNoun.append(vectors_of_curr_structure[i][1, IX_relativeNoun])
			PCA2_relativeVerb.append(vectors_of_curr_structure[i][1, IX_relativeVerb])

		fig, ax = plt.subplots()
		bins = range(-20, 21, 2)
		print(bins)
		plt.hist(PCA2_Noun, bins, alpha=0.5, label='Main noun', facecolor='b')
		plt.hist(PCA2_verb, bins, alpha=0.5, label='Main verb', facecolor='c')
		plt.hist(PCA2_relativeNoun, bins, alpha=0.5, label='RC noun', facecolor='r')
		plt.hist(PCA2_relativeVerb, bins, alpha=0.5, label='RC verb', facecolor='m')
		ax.set_title('Number of sentences in struct: ' + str(len(IX_structure)))
		plt.legend(loc='upper right')
		file_name = 'struct_' + str(i) + '.png'
		plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
		plt.close(fig)
		print('Plotting histograms...saved to png')
	except KeyboardInterrupt:
		sys.exit()
