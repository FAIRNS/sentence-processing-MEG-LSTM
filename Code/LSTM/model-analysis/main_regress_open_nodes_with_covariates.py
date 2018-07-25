import os
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import data_manip
from functions import annotated_data
from functions import vif
import sys
import pickle
sys.path.append(os.path.abspath('../src/word_language_model'))
import matplotlib.pyplot as plt

# inp
path = sys.path[0].split('/')
i = path.index('sentence-processing-MEG-LSTM')
base_folder = os.sep + os.path.join(*path[:i])

# base_folder = '/home/yl254115/Projects/FAIRNS'
txt_file = os.path.join(base_folder, 'sentence-processing-MEG-LSTM/Code/Stimuli/sentence_generator_Marco/20k_sentences.txt')
model = os.path.join(base_folder, 'sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt')
vocab = os.path.join(base_folder, 'sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt')
eos = '<eos>'
use_unk = True
unk = '<unk>'
lang = 'en'
get_representations = ['word', 'lstm']
# out
pkl_filename = os.path.join(base_folder, 'sentence-processing-MEG-LSTM/Output/Ridge_regression_number_of_open_nodes.pkl')

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

data_sentences = annotated_data.Data()
data_sentences.add_corpus(txt_file, separator='|', column_names=['sentence', 'structure', 'open_nodes_count', 'adjacent_boundary_count'])
data_sentences.data = data_sentences.filter(n=100) # Filter data to get a uniform distribution of sentence types
data_sentences.add_activation_data(model, vocab, eos, unk, use_unk, lang, get_representations)
#TODO(?): data_sentences.omit_depth_zero() # Not needed for Marco's sentence generator
#TODO: Add word position and frequency to design matrix.

data_sentences_train, data_sentences_test = data_manip.split_data(data_sentences.data, params) # Train-test split
scores_ridge = []
for split in range(params.CV_fold):
    # Preparing the data for regression, by breaking down sentences into X, y matrices that are word-wise:
    X_train, y_train, X_test, y_test = data_manip.prepare_data_for_regression(data_sentences_train[split], data_sentences_test[split])
    # TODO: data_sentences.decorrelate_position_depth()
    if split == 0: VIF = vif.calc_VIF(X_train) # calc VIF for first split only

    # Train a Ridge regression model:
    model_ridge = mfe.train_model(X_train, y_train, settings, params)

    # Evaluate model (using R-squared) on test set:
    scores_curr_split, MSE_per_depth = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)

    scores_ridge.append(scores_curr_split)
    print('Split %i: Mean validation score %1.2f +- %1.2f, alpha = %1.2f; Test scores: %1.2f' % (
    split + 1, model_ridge.cv_results_['mean_test_score'][model_ridge.best_index_],
    model_ridge.cv_results_['std_test_score'][model_ridge.best_index_], model_ridge.best_params_['alpha'], scores_curr_split))

# Save to drive:
with open(pkl_filename, 'wb') as f:
    pickle.dump((model_ridge, scores_ridge, VIF), f)
