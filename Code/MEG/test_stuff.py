import os.path as op
from functions import plot_results as pr
from functions import load_settings_params as lsp
from functions import sentcomp_epoching
import matplotlib.pyplot as plt

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()


# fig_f_stats_topo = pr.plot_topomap_optimal_bin(settings, params)
# file_name = 'f_stats_topo_patient_' + settings.patient
# plt.savefig(op.join(settings.path2figures, file_name))
# plt.close(fig_f_stats_topo)


settings.collect_data = False
params.step = 10 # Size of time bins to average over
for i in range(30):
	try:
		print 'Current time point index ' + str(i)
		params.i = i
		fig_R_squared_topo = pr.plot_topomap_regression_results(settings, params)
		file_name = 'R_squared_topo_patient_' + settings.patient + '_timepoint_' + str(i*10) + '_' + settings.LSTM_file_name + '.png'
		plt.savefig(op.join(settings.path2figures, 'R_squared_topos', file_name))
		plt.close(fig_R_squared_topo)
	except:
		print 'Failed in time group ' + str(i)
		pass
