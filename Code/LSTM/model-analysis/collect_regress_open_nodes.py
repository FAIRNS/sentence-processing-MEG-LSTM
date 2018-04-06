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
best_weights = []
for seed in range(1,6,1):
    pkl_filename = 'Regression_number_of_open_nodes_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c) + '_seed_'+ str(seed) + '.pckl'
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
    best_weights.append(models['model_lasso'].coefs[best_index, :])

best_weights = np.vstack(best_weights) # stack back to ndarray
file_name = 'Lasso_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c) + '.png'
plt = pr.plot_weights(best_weights, settings, params)
plt.savefig(op.join(settings.path2figures, file_name))


# Sort and save to file
file_name = 'Lasso_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c) + '.txt'
best_weights = np.vstack((np.mean(best_weights, axis=0), range(1,best_weights.shape[1]+1, 1)))
IX = np.argsort(best_weights[0, :])[::-1]
best_weights_sorted = np.transpose(best_weights)[IX]
best_weights_sorted.tofile(op.join(settings.path2output, file_name), sep="\t\n")