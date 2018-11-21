##
# import pickle, os, sys
# import numpy as np
# import matplotlib.pyplot as plt

# from functions import load_settings_params as lsp
# from functions import prepare_for_ablation_exp as prep

import os, pickle
# wrong_info = pickle.load(open('../../../Data/Stimuli/wrong_nounpp.info', 'rb'))
# prob_verbs = ['admire', 'admires', 'avoid', 'avoids', 'understand', 'understands']
def modify_file(path2file):
    dest_folder, filename = os.path.split(path2file)
    lines = open(path2file, 'r').readlines()
    sentences_row1 = [l.split('\t')[0] for l in lines if l.split('\t')[2]=='correct']
    sentences_row2 = [l.split('\t')[0] for l in lines if l.split('\t')[2] == 'wrong']
    conditions = [l.split('\t')[1] for l in lines if l.split('\t')[2]=='correct']
    new_lines = ['nounpp\t' + s1 + '\t' + c.split('_')[0] + '\t' + c.split('_')[1] + '\t' + s2.split(' ')[-1] for (s1, s2, c) in zip (sentences_row1, sentences_row2, conditions)]# if not w.split(' ')[-1] in prob_verbs]
    with open(os.path.join(dest_folder, filename[5::]), 'w') as f:
        for item in new_lines:
            f.write("%s\n" % item)


file_correct='/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/temp_correct_nounpp.txt'
file_wrong='/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/temp_wrong_nounpp.txt'

modify_file(file_correct)
modify_file(file_wrong)



# split1 = set('578 1149 988 1041 1101 29 186 1198 198 31 264 131 916 758 1241 1005 488'.split(' '))
# split2 = set('988 1041 578 1101 1149 186 1198 29 198 759 31 916 1019 758 1082 1229 488'.split(' '))
# split3 = set('988 578 1149 1041 29 1198 758 186 198 916 1101 488 355'.split(' '))
# split4 = set('78 1149 186 1041 1198 988 1101 29 198 131 488 916 31 758 264 355 646'.split(' '))
# split5 = set('578 988 1041 1149 1229 758 1101 916 1005 29 186 1061 759 31 1198 930 488'.split(' '))
#
# units_to_ablate = split1.intersection(split2, split3, split4, split5)
# print(units_to_ablate)
##


# settings = lsp.settings()
# n = 300
# model1 = 'Ridge'
# file_name1 = '%s_regression_number_of_open_nodes_n=%i' % (model1, n)
# with open(os.path.join(settings.path2output, 'num_open_nodes', file_name1 + '.pkl'), 'rb') as f:
#     model_obj_1 = pickle.load(f, encoding='latin1')[0]
# weights_model1 = []
# for i in range(5):
#     weights_model1.append(model_obj_1[i].best_estimator_.coef_)
# weights_model1 = np.asarray(weights_model1)
# output_filename = os.path.join(settings.path2output, 'num_open_nodes', file_name1 + '.txt')
# prep.generate_text_file_with_sorted_weights(weights_model1, output_filename)
#
#
# ##
# l = [1, 12, 2, 43 , 454]
# IX=np.asarray(l) <= 10
#
# A = np.arange(20).reshape([5, 4])
# A = A[:, IX]
#
# print('Rejected units: %s' % ' '.join([str(i) for i, v in enumerate(IX) if not v]))
#
# path2figures = os.path.join('..', '..', '..', 'Figures')
# path = sys.path[0].split('/')
# i = path.index('sentence-processing-MEG-LSTM')
# base_folder = os.sep + os.path.join(*path[:i+1])
# pkl_filename = os.path.join(base_folder, 'Output/Ridge_regression_number_of_open_nodes.pkl')
#
# with open(pkl_filename, 'rb') as f:
#     data = pickle.load(f)
# VIF = data[-1]
# plt.hist(VIF, 50)
# plt.xlabel('VIF', size=18)
# plt.ylabel('Number of featuress', size=18)
# plt.savefig(os.path.join(path2figures, 'num_open_nodes', 'VIF_dist.png'))
# plt.close()
#
# path2file = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/model_ridge_best_coef_all_MODEL_hidden650_batch128_dropout0.2_lr20.0.cpu.pt_h_or_c_0_layer_0.pkl'
# with open(path2file, 'rb') as f:
#     data = pickle.load(f)
# weights = data[0]
# IX = np.abs(weights).argsort()
# units_sorted = np.asarray(range(1300))[IX[::-1]]
#
#
# ##
# path2file = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_French.p'
# with open(path2file, 'rb') as f:
#     data = pickle.load(f)
#
# ##
# import numpy as np
# import matplotlib.pyplot as plt
#
# #mat = np.empty((7, 3))
# lst = []
# for r in range(100):
#     for i, k in enumerate(range(3,10)):
#         for j, l in enumerate(range(5, 8)):
#             lst.append([k, l])
# lst = np.asarray(lst)
# print(np.corrcoef(lst[:, 0], lst[:, 1]))
#
#
# plt.scatter(lst[:, 0], lst[:, 1])
# plt.show()
#
# import pickle
# path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_english_marco.p'
#
# with open(path2output_info, 'rb') as f:
#     data = pickle.load(f)
# print(data)
#
#
# ####
# import os.path as op
# import os
# import numpy as np
# from sklearn.model_selection import train_test_split
# from functions import load_settings_params as lsp
# from functions import plot_results as pr
# import matplotlib.pyplot as plt
# # from functions import plot_results as pr
# from tqdm import tqdm
# import torch
# import sys
# import pickle
# sys.path.append(os.path.abspath('../src/word_language_model'))
# import data
# import time
#
# # --------- Main script -----------
# print('Load settings and parameters')
# settings = lsp.settings()
# params = lsp.params()
# preferences = lsp.preferences()
#
# if settings.h_or_c == 0:
#     h_c = 'hidden'
# elif settings.h_or_c == 1:
#     h_c = 'cell'
#
# if settings.which_layer == 0:
#     layer = 'both layers'
# elif settings.which_layer == 1:
#     layer = 'first layer'
# elif settings.which_layer == 2:
#     layer = 'second layer'
#
# file_name_best_weights_model_from_LSTM_to_residuals = 'model_ridge_best_coef_all_MODEL_hidden650_batch128_dropout0.2_lr20.0.cpu.pt_h_or_c_0_layer_0.pkl'
# with open(op.join(settings.path2output, file_name_best_weights_model_from_LSTM_to_residuals), 'rb') as f:
#     best_weights_model_from_LSTM_to_residuals = pickle.load(f, encoding='latin1')
#
# from functions import prepare_for_ablation_exp as pfa
# k, n, ave, std = pfa.get_weight_outliers(best_weights_model_from_LSTM_to_residuals[0])
# print('k = %i, n = %i' % (k, n))
#
# print('Loading pre-tested LSTM model on test sentences...')
# file_name = 'LSTM_activations_pretested_on_sentences_hidden650_batch128_dropout0.2_lr20.0.cpu.pt.pkl'
# with open(op.join(settings.path2LSTMdata, file_name), "rb") as f:
#     X = pickle.load(f)
# # For DEBUG:
# X = [x for i,x in enumerate(X) if i<100]
# # ---------
# X = [x.transpose() for x in X] # Transpose elements
# X = np.vstack(X) # Reshape into a design matrix (num_words X num_units)
# print(X.shape)
#
# X = X[0:1000, 0:5]
#
# st_time = time.time()
# VIF_values1 = pfa.calc_VIF(X)
# print(time.time()-st_time)
#
# st_time = time.time()
# VIF_values2, IX_filter, ave_features, std_features = pfa.get_VIF_values(X)
# print(time.time()-st_time)
#
# print(VIF_values1, VIF_values2)
#
# # fig, ax = plt.subplots(1, 1)
# # ax.scatter(weights_model1, weights_model2, s=1)
# # r = np.corrcoef(weights_model1, weights_model2)
# # ax.set_xlabel(model1, fontsize=16)
# # ax.set_ylabel(model2, fontsize=16)
# # ax.set_title('h_or_c_' + str(settings.h_or_c) + '_layer_' + str(settings.which_layer), fontsize=16)
# # plt.text(-1, 0.5, 'r = %1.2f' % r[0, 1], fontsize=14)
# # # Add y = x line
# # lims = [
# #     np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
# #     np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
# # ]
# # ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
# # ax.set_aspect('equal')
# # ax.set_xlim(lims)
# # ax.set_ylim(lims)
# # file_name = 'regression_weights_correlation' '_h_or_c_' + str(settings.h_or_c) + '_layer_' + str(
# #     settings.which_layer) + '.png'
# plt.savefig(op.join(settings.path2figures, file_name))