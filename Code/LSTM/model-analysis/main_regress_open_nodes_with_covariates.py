import os.path as op
import os
import numpy as np
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import extract_activations_from_LSTM
from functions import data_manip
import sys
import pickle
sys.path.append(os.path.abspath('../src/word_language_model'))
import matplotlib.pyplot as plt


# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

#
pkl_filename = 'Ridge_regression_number_of_open_nodes.pkl'

# Load Stimuli
print('Loading number of open nodes data')
# Load a list of dict, each dict element corresponds to a sentence ['sentence'], ['open_nodes'], ['activations']
data_sentences = data_manip.load_data_from_sentence_generator(settings)
# For DEBUG ------
data_sentences = [data for i, data in enumerate(data_sentences) if i in range(100)]
# -------------

# Split data: each list (train/test) is of the size of the number of CV splits:
data_sentences_train, data_sentences_test = data_manip.split_data(data_sentences, params)
data_sentences = None # Clear from memory
scores_ridge = []
for split in range(params.CV_fold):
    # Preparing the data for regression, by breaking down sentences into X, y matrices that are word-wise:
    X_train, y_train, X_test, y_test = data_manip.prepare_data_for_regression(data_sentences_train[split], data_sentences_test[split])

    # Train a Ridge regression model:
    model_ridge = mfe.train_model(X_train, y_train, settings, params)

    # Evaluate model (using R-squared) on test set:
    scores_curr_split, MSE_per_depth = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)

    scores_ridge.append(scores_curr_split)
    print('Split %i: Mean validation score %1.2f +- %1.2f, alpha = %1.2f; Test scores: %1.2f' % (
    split + 1, model_ridge.cv_results_['mean_test_score'][model_ridge.best_index_],
    model_ridge.cv_results_['std_test_score'][model_ridge.best_index_], model_ridge.best_params_['alpha'], scores_curr_split))
