
from functions import load_settings_params as lsp
import pickle
from os import path as op
from matplotlib import pyplot as plt
import numpy as np

print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

vector_types = ['hidden', 'cell', 'word_vectors', 'bow_vectors']
for vector_type in vector_types:
	file_name = 'PCA_LSTM_' + vector_type + settings.LSTM_file_name + '.pkl'
	with open(op.join(settings.path2figures, 'units_activation', file_name), 'rb') as f:
		PCA_results = pickle.load(f)
	PCs = PCA_results[0].components_

	fig, axs = plt.subplots(2, 1)
	PC1 = PCs[0, :]
	IX1 = np.argsort(np.abs(PC1))
	PC1_sorted = PC1[IX1]
	axs[0].bar(range(1000), PC1_sorted)
	axs[0].set_title('PC1')
	axs[0].set_xticks(range(0,1000,30))
	axs[0].set_xticklabels(IX1[0:1000:30], rotation = 90)
	axs[0].set_xticklabels([])

	PC2 = PCs[1, :]
	IX2 = np.argsort(np.abs(PC2))
	PC2_sorted = PC2[IX2]
	axs[1].bar(range(1000), PC2_sorted)
	axs[1].set_title('PC2')
	axs[1].set_xticklabels(IX2)
	axs[1].set_xticklabels([])

	plt.suptitle(vector_type)
	file_name_weights = 'PCA_weights_' + vector_type + '_' + settings.LSTM_file_name + '.png'
	plt.savefig(op.join(settings.path2figures, 'units_activation', file_name_weights))



######################################################################3
# import os.path as op
# from functions import plot_results as pr
# from functions import load_settings_params as lsp
# from functions import sentcomp_epoching
# import matplotlib.pyplot as plt
#
# # --------- Main script -----------
# print('Load settings and parameters')
# settings = lsp.settings()
# params = lsp.params()
#
#
# # fig_f_stats_topo = pr.plot_topomap_optimal_bin(settings, params)
# # file_name = 'f_stats_topo_patient_' + settings.patient
# # plt.savefig(op.join(settings.path2figures, file_name))
# # plt.close(fig_f_stats_topo)
#
#
# settings.collect_data = False
# params.step = 10 # Size of time bins to average over
# for i in range(30):
# 	try:
# 		print 'Current time point index ' + str(i)
# 		params.i = i
# 		fig_R_squared_topo = pr.plot_topomap_regression_results(settings, params)
# 		file_name = 'R_squared_topo_patient_' + settings.patient + '_timepoint_' + str(i*10) + '_' + settings.LSTM_file_name + '.png'
# 		plt.savefig(op.join(settings.path2figures, 'R_squared_topos', file_name))
# 		plt.close(fig_R_squared_topo)
# 	except:
# 		print 'Failed in time group ' + str(i)
# 		pass
