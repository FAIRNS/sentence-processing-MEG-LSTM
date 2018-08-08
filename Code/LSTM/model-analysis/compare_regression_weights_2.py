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

# with open(op.join(settings.path2output, 'ablation_scores.txt'), 'r') as f:
#     ablation = f.readlines()
#     ablation = [s.rstrip().split(' ') for s in ablation]
# ablation = np.asarray(ablation).astype(int)
# IX_ablation = [l[1] for l in np.argsort(ablation, axis=0)]

n = 300
models_names = ['Ridge', 'Lasso'] # 'model_lasso', 'model_ridge'
# ----- Load LASSO model -----
for i, model1 in enumerate(models_names):
    for j, model2 in enumerate(models_names):
        if j > i:
            file_name1 = '%s_regression_number_of_open_nodes_n=%i' % (model1, n)
            file_name2 = '%s_regression_number_of_open_nodes_n=%i' % (model2, n)

            # filename_non_regularized_regression_weights = 'weights_non_regularized.pkl'
            with open(op.join(settings.path2output, 'num_open_nodes', file_name1 + '.pkl'), 'rb') as f:
                model_obj_1 = pickle.load(f, encoding='latin1')[0]

            with open(op.join(settings.path2output, 'num_open_nodes', file_name2 + '.pkl'), 'rb') as f:
                model_obj_2 = pickle.load(f, encoding='latin1')[0]

            weights_model1 = []; weights_model2 = []
            for i in range(5):
                weights_model1.append(model_obj_1[i].best_estimator_.coef_)
                weights_model2.append(model_obj_2[i].best_estimator_.coef_)
            weights_model1 = np.mean(np.asarray(weights_model1), axis=0)
            weights_model2 = np.mean(np.asarray(weights_model2), axis=0)

            from functions import prepare_for_ablation_exp
            outliers_model1 = prepare_for_ablation_exp.get_weight_outliers(weights_model1)[4]
            outliers_model2 = prepare_for_ablation_exp.get_weight_outliers(weights_model2)[4]
            colors_indicate_accord_on_outliers = ['g' if l1==l2 else 'r' if l1<l2 else 'b' for (l1, l2) in zip(outliers_model1, outliers_model2)]

            outlier_agreed = np.asarray([True if ele1==ele2 else False for (ele1, ele2) in zip (outliers_model1, outliers_model2)])
            outlier_only_LASSO = np.asarray([True if ele1<ele2 else False for (ele1, ele2) in zip (outliers_model1, outliers_model2)])
            outlier_only_Ridge = np.asarray([True if ele1>ele2 else False for (ele1, ele2) in zip (outliers_model1, outliers_model2)])

            # print(len(weights_model1), len(weights_model2))
            fig, ax = plt.subplots(1, 1, figsize=[15,10])
            ax.scatter(weights_model1[outlier_agreed], weights_model2[outlier_agreed], c = 'g', s = 4, edgecolors='face', label='Outlier consensus')
            ax.scatter(weights_model1[outlier_only_LASSO], weights_model2[outlier_only_LASSO], c='r', s=4,
                            edgecolors='face', label='LASSO outlier only')

            ax.scatter(weights_model1[outlier_only_Ridge], weights_model2[outlier_only_Ridge], c='b', s=4,
                            edgecolors='face', label='Ridge outlier only')

            r = np.corrcoef(weights_model1, weights_model2)
            ax.set_xlabel(model1, fontsize = 16)
            ax.set_ylabel(model2, fontsize = 16)
            ax.set_title('Weights comparison', fontsize = 16)
            plt.text(-0.1, 0.2, 'r = %1.2f' % r[0, 1], fontsize = 14)
            # Add y = x line
            lims = [
                np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
                np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
            ]
            ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
            ax.set_aspect('equal')
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            file_name = '%s_%s_regression_weights_correlation.png' % (model1, model2)
            plt.savefig(op.join(settings.path2figures, 'num_open_nodes', file_name))
