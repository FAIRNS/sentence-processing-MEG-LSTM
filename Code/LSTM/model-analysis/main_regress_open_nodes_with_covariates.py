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
base_folder = os.sep + os.path.join(*path[:i+1])

# number for filtering
n = 5

# base_folder = '/home/yl254115/Projects/FAIRNS'
txt_file = os.path.join(base_folder, 'Code/Stimuli/sentence_generator_Marco/20k_sentences.txt')
model = os.path.join(base_folder, 'Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt')
vocab = os.path.join(base_folder, 'Data/LSTM/english_vocab.txt')
data_file = os.path.join(base_folder, 'Code/Stimuli/sentence_generator_Marco/activations_20k_sentences_n=%i.pkl' %n)
frequency_file = os.path.join(base_folder, 'Data/LSTM/english_word_frequencies.txt')

regenerate_data=False

eos = '<eos>'
use_unk = True
unk = '<unk>'
lang = 'en'
get_representations = ['word', 'lstm']
# out
pkl_filename = os.path.join(base_folder, 'Output/Ridge_regression_number_of_open_nodes.pkl')

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

# check if datafile exists, if not, create it, otherwise load it
if os.path.exists(data_file) and not regenerate_data:
    print("Activations for this setting already generated, loading data from %s\n" % data_file)
    data_sentences = pickle.load(open(data_file, 'rb'))
else:
    data_sentences = annotated_data.Data()
    data_sentences.add_corpus(txt_file, separator='|', column_names=['sentence', 'structure', 'open_nodes_count', 'adjacent_boundary_count'])
    data_sentences.data = data_sentences.filter_sentences(n=n) # Filter data to get a uniform distribution of sentence types
    data_sentences.add_word_frequency_counts(frequency_file)
    data_sentences.add_activation_data(model, vocab, eos, unk, use_unk, lang, get_representations)
    pickle.dump(data_sentences, open(data_file, 'wb'))

# decorrelate data
c_dict = data_sentences.decorrelation_matrix()
# x1, x2, y1, y2, n = find_max_rectangle(c_dict)
# TODO implement function to find max rectangle
data_sentences.decorrelate(3, 5, 2, 4, 2)

# all_tuples = list(c_dict.keys())
# all_tuples.sort()
# for tup in all_tuples:
#     # if tup[0] >= 9 and tup[0] <= 15 and tup[1] >= 3 and tup[1] <= 10:
#     print('(%i, %i): %i' % (tup[0], tup[1], c_dict[tup]))
# exit()

#TODO(?): data_sentences.omit_depth_zero() # Not needed for Marco's sentence generator

data_sentences_train, data_sentences_test = data_manip.split_data(data_sentences.data, params) # Train-test split
scores_ridge = []; VIF = []
for split in range(params.CV_fold):
    # Preparing the data for regression, by breaking down sentences into X, y matrices that are word-wise:
    X_train, y_train, X_test, y_test = data_manip.prepare_data_for_regression(data_sentences_train[split], data_sentences_test[split])
    print(X_train.shape)
    # TODO: data_sentences.decorrelate_position_depth()
    # if split == 0: VIF = vif.calc_VIF(X_train) # calc VIF for first split only

    # Train a Ridge regression model:
    model_ridge = mfe.train_model_ridge(X_train, y_train, settings, params)

    # Evaluate model (using R-squared) on test set:
    scores_curr_split, MSE_per_depth = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)

    scores_ridge.append(scores_curr_split)
    print('Split %i: Mean validation score %1.2f +- %1.2f, alpha = %1.2f; Test scores: %1.2f' % (
    split + 1, model_ridge.cv_results_['mean_test_score'][model_ridge.best_index_],
    model_ridge.cv_results_['std_test_score'][model_ridge.best_index_], model_ridge.best_params_['alpha'], scores_curr_split))

# Save to drive:
with open(pkl_filename, 'wb') as f:
    pickle.dump((model_ridge, scores_ridge, VIF), f)
