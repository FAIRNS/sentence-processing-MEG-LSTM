import pickle
path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_english_marco.p'

with open(path2output_info, 'rb') as f:
    data = pickle.load(f)
print(data)


####
import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import plot_results as pr
import matplotlib.pyplot as plt
# from functions import plot_results as pr
from tqdm import tqdm
import torch
import sys
import pickle
sys.path.append(os.path.abspath('../src/word_language_model'))
import data
import time

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

file_name_best_weights_model_from_LSTM_to_residuals = 'model_ridge_best_coef_all_MODEL_hidden650_batch128_dropout0.2_lr20.0.cpu.pt_h_or_c_0_layer_0.pkl'
with open(op.join(settings.path2output, file_name_best_weights_model_from_LSTM_to_residuals), 'rb') as f:
    best_weights_model_from_LSTM_to_residuals = pickle.load(f, encoding='latin1')

from functions import prepare_for_ablation_exp as pfa
k, n, ave, std = pfa.get_weight_outliers(best_weights_model_from_LSTM_to_residuals[0])
print('k = %i, n = %i' % (k, n))

print('Loading pre-tested LSTM model on test sentences...')
file_name = 'LSTM_activations_pretested_on_sentences_hidden650_batch128_dropout0.2_lr20.0.cpu.pt.pkl'
with open(op.join(settings.path2LSTMdata, file_name), "rb") as f:
    X = pickle.load(f)
# For DEBUG:
X = [x for i,x in enumerate(X) if i<100]
# ---------
X = [x.transpose() for x in X] # Transpose elements
X = np.vstack(X) # Reshape into a design matrix (num_words X num_units)
print(X.shape)

X = X[0:1000, 0:5]

st_time = time.time()
VIF_values1 = pfa.calc_VIF(X)
print(time.time()-st_time)

st_time = time.time()
VIF_values2, IX_filter, ave_features, std_features = pfa.get_VIF_values(X)
print(time.time()-st_time)

print(VIF_values1, VIF_values2)

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