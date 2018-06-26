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


file_name_regress_from_word_position = 'Ridge_Regression_number_of_open_nodes_from_word_position_all.pckl'

with open(op.join(settings.path2output, file_name_regress_from_word_position), 'rb') as f:
    results_regress_from_word_position = pickle.load(f, encoding='latin1')

R_squared = []
for seed in range(1,6,1):
    file_name_regress_from_LSTM_to_residuals = 'Ridge_Regression_number_of_open_nodes_after_partial_out_word_position_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_layer_' + str(settings.which_layer) + '_h_or_c_' + str(
                    settings.h_or_c) + '_seed_' + str(seed) + '.pckl'

    # filename_non_regularized_regression_weights = 'weights_non_regularized.pkl'
    with open(op.join(settings.path2output, file_name_regress_from_LSTM_to_residuals), 'rb') as f:
        results_regress_from_LSTM_to_residuals = pickle.load(f, encoding='latin1')
    R_squared.append(results_regress_from_LSTM_to_residuals['ridge_scores_test'])
print(np.mean(R_squared), np.std(R_squared))


file_name_best_weights_model_from_LSTM_to_residuals = 'model_ridge_best_coef_all_MODEL_hidden650_batch128_dropout0.2_lr20.0.cpu.pt_h_or_c_0_layer_0.pkl'
with open(op.join(settings.path2output, file_name_best_weights_model_from_LSTM_to_residuals), 'rb') as f:
    best_weights_model_from_LSTM_to_residuals = pickle.load(f, encoding='latin1')


print('weights')

# fig, ax = plt.subplots(1, 1)
# ax.scatter(weights_model1, weights_model2, s=1)
# r = np.corrcoef(weights_model1, weights_model2)
# ax.set_xlabel(model1, fontsize=16)
# ax.set_ylabel(model2, fontsize=16)
# ax.set_title('h_or_c_' + str(settings.h_or_c) + '_layer_' + str(settings.which_layer), fontsize=16)
# plt.text(-1, 0.5, 'r = %1.2f' % r[0, 1], fontsize=14)
# # Add y = x line
# lims = [
#     np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
#     np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
# ]
# ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
# ax.set_aspect('equal')
# ax.set_xlim(lims)
# ax.set_ylim(lims)
# file_name = 'regression_weights_correlation' '_h_or_c_' + str(settings.h_or_c) + '_layer_' + str(
#     settings.which_layer) + '.png'
# plt.savefig(op.join(settings.path2figures, file_name))