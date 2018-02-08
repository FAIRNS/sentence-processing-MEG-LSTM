import os.path as op
from functions import plot_results as pr
from functions import load_settings_params as lsp
from functions import sentcomp_epoching
import matplotlib.pyplot as plt

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()


fig_f_stats_topo = pr.plot_topomap_optimal_bin(settings, params)
file_name = 'f_stats_topo_patient_' + settings.patient
plt.savefig(op.join(settings.path2figures, file_name))
plt.close(fig_f_stats_topo)