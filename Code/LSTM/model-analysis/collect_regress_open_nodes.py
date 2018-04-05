import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import plot_results as pr

# from functions import plot_results as pr
import torch
import sys
import pickle
sys.path.append(os.path.abspath('../src/word_language_model'))
import data

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

# ----- Load LASSO model -----
pkl_filename = 'Regression_number_of_open_nodes_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c) + '.pckl'
with open(op.join(settings.path2output, pkl_filename), "rb") as f:
    models = pickle.load(f)

# ---- Generate figures --------

# Regularization path
file_name = 'Lasso_coef_and_R_squared_vs_regularization_size.png'
plt = pr.regularization_path(models['model_lasso'], settings, params)
plt.savefig(op.join(settings.path2figures, file_name))
plt.close()

# Best weights (correspond to optimal regularization size)
best_index = models['model_lasso'].best_index_
best_weights = models['model_lasso'].coefs[best_index, :]
file_name = 'Lasso_best_coef.png'
plt = pr.plot_weights(best_weights, settings, params)
plt.savefig(op.join(settings.path2figures, file_name))

