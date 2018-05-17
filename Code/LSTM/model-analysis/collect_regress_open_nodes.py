import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import plot_results as pr
import matplotlib.pyplot as plt
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

bar_plot_width = 0.35  # the width of the bars
models_names = ['model_ridge'] # 'model_lasso', 'model_ridge'
# ----- Load LASSO model -----
for i, model in enumerate(models_names):
    best_weights = []
    for seed in range(1,6,1):
        if model == 'model_ridge':
            prefix_str = 'Ridge'
        elif model == 'model_lasso':
            prefix_str = 'LASSO'
        pkl_filename = prefix_str + '_Regression_number_of_open_nodes_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_layer_' + str(settings.which_layer) + '_h_or_c_' + str(settings.h_or_c) + '_seed_'+ str(seed) + '.pckl'
        with open(op.join(settings.path2output, pkl_filename), "rb") as f:
            models = pickle.load(f)

        # ---- Generate figures --------
        # Regularization path
        file_name = model + '_coef_and_R_squared_vs_regularization_size.png'
        fig_path = pr.regularization_path(models[model], settings, params)

        fig_path.savefig(op.join(settings.path2figures, file_name))
        fig_path.close()

        # Best weights (correspond to optimal regularization size)
        if model == 'model_ridge':
            best_index = models['model_ridge'].best_index_
        elif model == 'model_lasso':
            best_index = models['model_lasso'].best_index_

        best_weights.append(models[model].coefs[best_index])

    best_weights = np.vstack(best_weights) # stack back to ndarray
    ind = np.arange(best_weights.shape[1]) + 1  # the x locations for the groups

    fig, axs = plt.subplots(len(models_names), sharex=True, sharey=True)
    axs.bar(ind, np.mean(best_weights, axis=0), bar_plot_width, color='b', yerr=np.std(best_weights, axis=0))
    axs.set_ylabel('Weight size')
    axs.set_xlabel('Unit')
    axs.set_xlim([0, best_weights.shape[1]])
    axs.set_title(model)
    plt.show()

    file_name = model + '_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(
        settings.h_or_c) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close(fig)

    # pr.plot_weights(best_weights, model, axs, i, settings, params)

    # Sort and save to file
    file_name = model + '_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c) + '.txt'
    best_weights = np.vstack((np.mean(best_weights, axis=0), range(1,best_weights.shape[1]+1, 1)))
    IX = np.argsort(best_weights[0, :])[::-1]
    best_weights_sorted = np.transpose(best_weights)[IX]
    np.savetxt(op.join(settings.path2output, file_name), best_weights_sorted, fmt='%1.2f, %i')
    print('Saved to: ' + op.join(settings.path2output, file_name))

