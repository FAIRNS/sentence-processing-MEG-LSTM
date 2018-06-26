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

if settings.h_or_c == 0:
    h_c = 'hidden'
elif settings.h_or_c == 1:
    h_c = 'cell'

if settings.which_layer == 0:
    layer = 'both layers'
elif settings.which_layer == 1:
    layer = 'first layer'
elif settings.which_layer == 2:
    layer = 'second layer'

with open(op.join(settings.path2output, 'ablation_scores.txt'), 'r') as f:
    ablation = f.readlines()
    ablation = [s.rstrip().split(' ') for s in ablation]
ablation = np.asarray(ablation).astype(int)
IX_ablation = [l[1] for l in np.argsort(ablation, axis=0)]


models_names = ['model_ridge', 'model_non_regularized'] # 'model_lasso', 'model_ridge'
# ----- Load LASSO model -----
for i, model1 in enumerate(models_names):
    for j, model2 in enumerate(models_names):
        if j > i:
            file_name1 = model1 + '_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(
                    settings.h_or_c) + '_layer_' + str(settings.which_layer)

            file_name2 = model2 + '_best_coef_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(
                settings.h_or_c) + '_layer_' + str(settings.which_layer)

            # filename_non_regularized_regression_weights = 'weights_non_regularized.pkl'
            with open(op.join(settings.path2output, file_name1 + '.pkl'), 'rb') as f:
                weights_model1 = pickle.load(f, encoding='latin1')

            IX_regress = np.argsort(-np.abs(weights_model1), axis=0)
            # IX_regress = [n + 650 for n in IX_regress]


            with open(op.join(settings.path2output, file_name2 + '.pkl'), 'rb') as f:
                weights_model2 = pickle.load(f, encoding='latin1')




            fig, ax = plt.subplots(1, 1)
            ax.scatter(weights_model1, weights_model2, s = 1)
            r = np.corrcoef(weights_model1, weights_model2)
            ax.set_xlabel(model1, fontsize = 16)
            ax.set_ylabel(model2, fontsize = 16)
            ax.set_title('h_or_c_' + str(settings.h_or_c) + '_layer_' + str(settings.which_layer), fontsize = 16)
            plt.text(-1, 0.5, 'r = %1.2f' % r[0, 1], fontsize = 14)
            # Add y = x line
            lims = [
                np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
                np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
            ]
            ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
            ax.set_aspect('equal')
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            file_name = 'regression_weights_correlation' '_h_or_c_' + str(settings.h_or_c) + '_layer_' + str(settings.which_layer) + '.png'
            plt.savefig(op.join(settings.path2figures, file_name))
