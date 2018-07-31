import os
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import data_manip
from functions import annotated_data
from functions import vif
from functions import plot_results
from functions import prepare_for_ablation_exp
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../src/word_language_model'))

# inp
path = sys.path[0].split('/')
i = path.index('sentence-processing-MEG-LSTM')
base_folder = os.sep + os.path.join(*path[:i+1])

# number for filtering
n = 10000
calc_VIF = True # VIF calc may be slow

# base_folder = '/home/yl254115/Projects/FAIRNS'
txt_file = os.path.join(base_folder, 'Data/Stimuli/1M_sentences.txt')
model = os.path.join(base_folder, 'Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt')
vocab = os.path.join(base_folder, 'Data/LSTM/english_vocab.txt')
data_file = os.path.join(base_folder, 'Output/num_open_nodes/activations_1M_sentences_n=%i.pkl' %n)
frequency_file = os.path.join(base_folder, 'Data/LSTM/english_word_frequencies.txt')

regenerate_data=False

eos = '<eos>'
use_unk = True
unk = '<unk>'
lang = 'en'
get_representations = ['word', 'lstm']
get_representations = ['lstm']
# out
pkl_filename = os.path.join(base_folder, 'Output/Ridge_regression_number_of_open_nodes.pkl')

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

### check if datafile exists, if not, create it, otherwise load it:
if os.path.exists(data_file) and not regenerate_data:
    print("Activations for this setting already generated, loading data from %s\n" % data_file)
    data_sentences = pickle.load(open(data_file, 'rb'))
else:
    data_sentences = annotated_data.Data()
    data_sentences.add_corpus(txt_file, separator='|', column_names=['sentence', 'structure', 'open_nodes_count', 'adjacent_boundary_count'])
    data_sentences.data = data_sentences.filter_sentences(n=n, elements=list(range(25))) # Filter data to get a uniform distribution of sentence types
    data_sentences.add_word_frequency_counts(frequency_file)
    data_sentences.add_activation_data(model, vocab, eos, unk, use_unk, lang, get_representations)
    pickle.dump(data_sentences, open(data_file, 'wb'))

### Decorrelate position and depth in data:
c_dict = data_sentences.decorrelation_matrix(plot_pos_depth=True) # get position-depth tuples in data
pos_min=6; pos_max=11; depth_min=2; depth_max=7
min_n = data_sentences.get_min_number_of_samples_in_rectangle(c_dict, pos_min=pos_min, pos_max=pos_max, depth_min=depth_min, depth_max=depth_max)
data_sentences.decorrelate(pos_min=pos_min, pos_max=pos_max, depth_min=depth_min, depth_max=depth_max, n=min_n) # decorrelate data

# TODO implement function to find max rectangle
# TODO(?): data_sentences.omit_depth_zero() # Not needed for Marco's sentence generator

### Train/test regression model:
data_sentences_train, data_sentences_test = data_manip.split_data(data_sentences.data, params) # Train-test split
models_ridge = []; weights = []; scores_ridge = []; scores_reduced_model = []; VIF = []; units_outliers = []
for split in range(params.CV_fold):
    # Preparing the data for regression, by breaking down sentences into X, y matrices that are word-wise:
    X_train, y_train, X_test, y_test = data_manip.prepare_data_for_regression(data_sentences_train[split], data_sentences_test[split])
    X_train, X_test = data_manip.standardize_data(X_train, X_test)
    if split == 0 and calc_VIF: VIF = vif.calc_VIF(X_train) # calc VIF for first split only

    # Train a Ridge regression model:
    model_ridge = mfe.train_model_ridge(X_train, y_train, settings, params)

    # Evaluate model (R-squared) on test set:
    scores_curr_split, MSE_per_depth = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)
    scores_ridge.append(scores_curr_split)

    # Evalue reduced model (without covariats, such as word frequency):
    model_ridge.best_estimator_.coef_[-1] = 0 # remove word-frequency regressor
    scores_reduced_model_curr_split, _ = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)
    scores_reduced_model.append(scores_reduced_model_curr_split)

    # Save resulting weights
    curr_weights = model_ridge.best_estimator_.coef_
    weights.append(curr_weights)
    models_ridge.append(model_ridge)

    # Plot regularization path:
    p = plot_results.regularization_path(model_ridge, settings, params)
    file_name = 'regularization_path_split %i' % split + '.png'
    p.savefig(os.path.join(settings.path2figures, 'num_open_nodes', file_name))
    p.close()

    # For each split, find units with largest weights:
    num_features = curr_weights.shape[0]
    IX = np.abs(curr_weights).argsort()
    units_sorted = np.asarray(range(num_features))[IX[::-1]] # Sort units in descending order wrt weight size
    k, n, ave, std = prepare_for_ablation_exp.get_weight_outliers(curr_weights) # Find outlier weights (>3SD)
    units_outliers.append(units_sorted[0:k]) # Append for each split

    # Print info to screen
    print('Split %i:' % (split+1))
    print('num_samples_train, num_samples_test, num_features = (%i, %i, %i)' % (X_train.shape[0], X_test.shape[0], X_train.shape[1]))
    print('k=%i, n=%i, mean_weight=%1.5f, std_weights=%1.5f' % (k, n, ave, std))
    print('Units for ablation: ' + ' '.join(['%i' % unit for unit in units_sorted[0:k]]))
    print('Mean validation score %1.2f +- %1.2f, alpha = %1.2f; Test scores: %1.5f (reduced model: %1.5f)' % (
    model_ridge.cv_results_['mean_test_score'][model_ridge.best_index_],
    model_ridge.cv_results_['std_test_score'][model_ridge.best_index_], model_ridge.best_params_['alpha'],
    scores_curr_split, scores_reduced_model_curr_split))
    print('\n')

### Save to drive:
if calc_VIF: print(np.min(VIF), np.max(VIF), np.mean(VIF))
with open(pkl_filename, 'wb') as f:
    pickle.dump((models_ridge, scores_ridge, scores_reduced_model_curr_split, units_outliers, VIF), f)


### Plot stuff:
weights_mean = np.mean(np.asarray(weights), axis=0)
weights_std = np.std(np.asarray(weights), axis=0)
num_features = weights_mean.shape[0]
IX = np.abs(weights_mean).argsort()
units_sorted = np.asarray(range(num_features))[IX[::-1]]
k, n, ave, std = prepare_for_ablation_exp.get_weight_outliers(weights_mean)

print('After averaging across splits:')
print('mean test score: %1.2f' % np.mean(scores_ridge))
print('k=%i, n=%i, mean_weight=%1.2f, std_weights=%1.2f' % (k, n, ave, std))
print('Units for ablation: ' + ' '.join(['%i' % unit for unit in units_sorted[0:k]]))


plt.bar(range(num_features), weights_mean[IX], yerr=weights_std[IX])
plt.xlabel('Units (sorted order)', size=18)
plt.ylabel('Weight size', size=18)
plt.savefig(os.path.join(settings.path2figures, 'num_open_nodes', 'weights_ridge_synthetic.png'))
plt.close()

plt.hist(np.abs(weights_mean), 50)
plt.xlabel('Weight size', size=18)
plt.ylabel('Number of units', size=18)
plt.savefig(os.path.join(settings.path2figures, 'num_open_nodes', 'weights_ridge_synthetic_dist.png'))
plt.close()