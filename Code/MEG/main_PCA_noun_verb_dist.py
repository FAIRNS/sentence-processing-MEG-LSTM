import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import matplotlib.pyplot as plt
import pickle
import sys
import numpy as np
from scipy import stats

# ------------------------------
vector_type = 'hidden'

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

# Load stimuli in groups according to struct
print('Load stimuli and info')
all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors = alu.get_stimuli_and_info(settings, params)

# Load PCA data
file_name = 'PCA_LSTM_traject_' + vector_type + settings.LSTM_file_name + '.pkl'
print('Loading: ' + file_name)
with open(op.join(settings.path2figures, 'units_activation', file_name), 'rb') as f:
	vectors_PCA_trajectories = pickle.load(f)

# calc dist per structure
print('After PCA: average across each syntactic structure type')
PCA2_Noun_all_structs = []; PCA2_verb_all_structs = []; PCA2_relativeNoun_all_structs = []; PCA2_relativeVerb_all_structs = []
for i_struct, IX_structure in enumerate(IX_structures):
	if IX_structure:
		curr_stimuli = [stim for ind, stim in enumerate(all_stim_clean) if ind in IX_structures[i_struct]]
		print(str(i_struct) + ': ' + curr_stimuli[0])
		PCA2_Noun = []; PCA2_verb = []; PCA2_relativeNoun = []; PCA2_relativeVerb = []
		vectors_of_curr_structure = [vec for ind, vec in enumerate(vectors_PCA_trajectories) if ind in IX_structure]
		info_of_curr_structure = [i_info for ind, i_info in enumerate(all_info_correct) if ind in IX_structure]
		for i_info, curr_info in enumerate(info_of_curr_structure):
			if 'PoS' in curr_info.keys():
				curr_PoS = curr_info['PoS']
				IX_Noun = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'Noun']
				IX_verb = [IX for IX, pos in enumerate(curr_PoS) if pos == 'verb']
				IX_relativeNoun = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'relativeNoun']
				IX_relativeVerb = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'relativeVerb']
				# print(curr_PoS)
				# print(IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb)
				if all([v < vectors_of_curr_structure[i_info].shape[1] for v in IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb]):
					PCA2_Noun.append(vectors_of_curr_structure[i_info][1, IX_Noun][0])
					PCA2_verb.append(vectors_of_curr_structure[i_info][1, IX_verb][0])
					PCA2_relativeNoun.append(vectors_of_curr_structure[i_info][1, IX_relativeNoun][0])
					PCA2_relativeVerb.append(vectors_of_curr_structure[i_info][1, IX_relativeVerb][0])
					PCA2_Noun_all_structs.append(vectors_of_curr_structure[i_info][1, IX_Noun][0])
					PCA2_verb_all_structs.append(vectors_of_curr_structure[i_info][1, IX_verb][0])
					PCA2_relativeNoun_all_structs.append(vectors_of_curr_structure[i_info][1, IX_relativeNoun][0])
					PCA2_relativeVerb_all_structs.append(vectors_of_curr_structure[i_info][1, IX_relativeVerb][0])
				else:
					# print(curr_info)
					# print(vectors_of_curr_structure[i].shape)
					# print(curr_PoS)
					# print(IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb)
					print(curr_stimuli[i_info])


		print('Calc stats: Main noun - Main verb vs. RC noun - RC verb')
		main_noun_minus_verb = [x-y for (x,y) in zip(PCA2_Noun, PCA2_verb)]
		RC_noun_minus_verb = [x - y for (x, y) in zip(PCA2_relativeNoun, PCA2_relativeVerb)]
		t, p = stats.ttest_ind(main_noun_minus_verb, RC_noun_minus_verb)

		print('Generating histograms...')
		fig, ax = plt.subplots(figsize=[30, 20])
		bins = range(-20, 21, 1)
		plt.hist(PCA2_Noun, 20, range=[-20, 20], alpha=0.5, label='Main noun', facecolor='b')
		plt.hist(PCA2_verb, 20, range=[-20, 20], alpha=0.5, label='Main verb', facecolor='c')
		plt.hist(PCA2_relativeNoun, 20, range=[-20, 20], alpha=0.5, label='RC noun', facecolor='r')
		plt.hist(PCA2_relativeVerb, 20, range=[-20, 20], alpha=0.5, label='RC verb', facecolor='m')
		ax.set_title('%s #sentences: %s p-value %1.5f ' % (curr_stimuli[0], str(len(IX_structure)), p), fontsize=24)
		ax.set_xlabel('Second-PC value', fontsize=30)
		ax.set_ylabel('Number of words', fontsize=30)
		ax.tick_params(axis='both', labelsize=26)
		plt.legend(loc='upper right')
		file_name = 'PC2_LSTM_' + vector_type + '_' + labels[i_struct] + '_' + settings.stimuli_file_name + '.svg'
		plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
		plt.close(fig)
		print('Plotting histograms...saved to png')

print('Calc stats: Main noun - Main verb vs. RC noun - RC verb')
main_noun_minus_verb = [x-y for (x,y) in zip(PCA2_Noun_all_structs, PCA2_verb_all_structs)]
RC_noun_minus_verb = [x - y for (x, y) in zip(PCA2_relativeNoun_all_structs, PCA2_relativeVerb_all_structs)]
t, p = stats.ttest_ind(main_noun_minus_verb, RC_noun_minus_verb)

print('Generating histogram for all structures...')
fig, ax = plt.subplots(figsize=[24, 16])
bins = range(-20, 21, 1)
plt.hist(PCA2_Noun_all_structs, 20, range=[-20, 20], alpha=0.5, label='Main noun', facecolor='b')
plt.hist(PCA2_verb_all_structs, 20, range=[-20, 20], alpha=0.5, label='Main verb', facecolor='c')
plt.hist(PCA2_relativeNoun_all_structs, 20, range=[-20, 20], alpha=0.5, label='RC noun', facecolor='r')
plt.hist(PCA2_relativeVerb_all_structs, 20, range=[-20, 20], alpha=0.5, label='RC verb', facecolor='m')
#ax.set_title('All structures (# %i) p-value %1.5f ' % (len(PCA2_Noun_all_structs), p), fontsize=24)
ax.set_xlabel('PC2 value', fontsize=30)
ax.set_ylabel('Number of words', fontsize=30)
ax.tick_params(axis='both', labelsize=26)
plt.legend(loc='upper right', fontsize = 30, framealpha=1)
file_name = 'PC2_LSTM_' + vector_type + '_all_structures_' + settings.stimuli_file_name + '.svg'
plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
plt.close(fig)
print('Plotting histograms...saved to png')


# NP_VP structures:
#print('PC2 distribution for NP_VP structures')
#PCA2_Noun_all_structs = []; PCA2_verb_all_structs = []; PCA2_VP_Noun_all_structs = []
#for i_struct, IX_structure in enumerate(IX_structures):
#	if IX_structure:
#		curr_stimuli = [stim for ind, stim in enumerate(all_stim_clean) if ind in IX_structures[i_struct]]
#		print(str(i_struct) + ': ' + curr_stimuli[0])
#		PCA2_Noun = []; PCA2_verb = []; PCA2_VP_Noun = []
#		vectors_of_curr_structure = [vec for ind, vec in enumerate(vectors_PCA_trajectories) if ind in IX_structure]
#		info_of_curr_structure = [i_info for ind, i_info in enumerate(all_info_correct) if ind in IX_structure]
#		for i_info, curr_info in enumerate(info_of_curr_structure):
#			if 'PoS' in curr_info.keys():
#				curr_PoS = curr_info['PoS']
#				IX_Noun = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'Noun']
#				IX_verb = [IX for IX, pos in enumerate(curr_PoS) if pos == 'verb']
#				IX_relativeNoun = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'relativeNoun']
#				IX_relativeVerb = [IX for IX, pos in enumerate(curr_PoS) if pos.lstrip() == 'relativeVerb']
#				# print(curr_PoS)
#				# print(IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb)
#				if all([v < vectors_of_curr_structure[i_info].shape[1] for v in IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb]):
#					PCA2_Noun.append(vectors_of_curr_structure[i_info][1, IX_Noun][0])
#					PCA2_verb.append(vectors_of_curr_structure[i_info][1, IX_verb][0])
#					PCA2_relativeNoun.append(vectors_of_curr_structure[i_info][1, IX_relativeNoun][0])
#					PCA2_relativeVerb.append(vectors_of_curr_structure[i_info][1, IX_relativeVerb][0])
#					PCA2_Noun_all_structs.append(vectors_of_curr_structure[i_info][1, IX_Noun][0])
#					PCA2_verb_all_structs.append(vectors_of_curr_structure[i_info][1, IX_verb][0])
#					PCA2_relativeNoun_all_structs.append(vectors_of_curr_structure[i_info][1, IX_relativeNoun][0])
#					PCA2_relativeVerb_all_structs.append(vectors_of_curr_structure[i_info][1, IX_relativeVerb][0])
#				else:
#					# print(curr_info)
#					# print(vectors_of_curr_structure[i].shape)
#					# print(curr_PoS)
#					# print(IX_Noun + IX_verb + IX_relativeNoun + IX_relativeVerb)
#					print(curr_stimuli[i_info])
#
#
#		print('Calc stats: Main noun - Main verb vs. RC noun - RC verb')
#		main_noun_minus_verb = [x-y for (x,y) in zip(PCA2_Noun, PCA2_verb)]
#		RC_noun_minus_verb = [x - y for (x, y) in zip(PCA2_relativeNoun, PCA2_relativeVerb)]
#		t, p = stats.ttest_ind(main_noun_minus_verb, RC_noun_minus_verb)
#
#		print('Generating histograms...')
#		fig, ax = plt.subplots(figsize=[30, 20])
#		bins = range(-20, 21, 1)
#		plt.hist(PCA2_Noun, 20, range=[-20, 20], alpha=0.5, label='Main noun', facecolor='b')
#		plt.hist(PCA2_verb, 20, range=[-20, 20], alpha=0.5, label='Main verb', facecolor='c')
#		plt.hist(PCA2_relativeNoun, 20, range=[-20, 20], alpha=0.5, label='RC noun', facecolor='r')
#		plt.hist(PCA2_relativeVerb, 20, range=[-20, 20], alpha=0.5, label='RC verb', facecolor='m')
#		ax.set_title('%s #sentences: %s p-value %1.5f ' % (curr_stimuli[0], str(len(IX_structure)), p), fontsize=24)
#		ax.set_xlabel('Second-PC value', fontsize=30)
#		ax.set_ylabel('Number of words', fontsize=30)
#		ax.tick_params(axis='both', labelsize=26)
#		plt.legend(loc='upper right')
#		file_name = 'PC2_LSTM_' + vector_type + '_' + labels[i_struct] + '_' + settings.stimuli_file_name + '.svg'
#		plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
#		plt.close(fig)
#		print('Plotting histograms...saved to png')
#
#print('Calc stats: Main noun - Main verb vs. RC noun - RC verb')
#main_noun_minus_verb = [x-y for (x,y) in zip(PCA2_Noun_all_structs, PCA2_verb_all_structs)]
#RC_noun_minus_verb = [x - y for (x, y) in zip(PCA2_relativeNoun_all_structs, PCA2_relativeVerb_all_structs)]
#t, p = stats.ttest_ind(main_noun_minus_verb, RC_noun_minus_verb)
#
#print('Generating histogram for all structures...')
#fig, ax = plt.subplots(figsize=[30, 20])
#bins = range(-20, 21, 1)
#plt.hist(PCA2_Noun_all_structs, 20, range=[-20, 20], alpha=0.5, label='Main noun', facecolor='b')
#plt.hist(PCA2_verb_all_structs, 20, range=[-20, 20], alpha=0.5, label='Main verb', facecolor='c')
#plt.hist(PCA2_relativeNoun_all_structs, 20, range=[-20, 20], alpha=0.5, label='RC noun', facecolor='r')
#plt.hist(PCA2_relativeVerb_all_structs, 20, range=[-20, 20], alpha=0.5, label='RC verb', facecolor='m')
#ax.set_title('All structures (# %i) p-value %1.5f ' % (len(PCA2_Noun_all_structs), p), fontsize=24)
#ax.set_xlabel('PC2 value', fontsize=30)
#ax.set_ylabel('Number of words', fontsize=30)
#ax.tick_params(axis='both', labelsize=26)
#plt.legend(loc='upper right')
#file_name = 'PC2_LSTM_' + vector_type + '_all_structures_' + settings.stimuli_file_name + '.svg'
#plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
#plt.close(fig)
#print('Plotting histograms...saved to png')
