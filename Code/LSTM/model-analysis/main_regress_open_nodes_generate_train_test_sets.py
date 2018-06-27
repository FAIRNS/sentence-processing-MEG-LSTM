import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import extract_activations_from_LSTM
import sys
import pickle
sys.path.append(os.path.abspath('../src/word_language_model'))
import data

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
preferences = lsp.preferences()

if len(sys.argv) > 1:
    print('seed_split ' + sys.argv[1])
    seed_split = int(sys.argv[1])
    params.seed_split = seed_split

# Load Stimuli
print('Loading number of open nodes data')
with open(op.join(settings.path2LSTMdata, settings.bnc_data), 'rb') as f:
    stimuli = pickle.load(f)
    sentences = [i[0] for i in stimuli]
    meta = [i[2] for i in stimuli]
    stimuli = None  # clear from memory
    # For debug
    # sentences = [s for i, s in enumerate(sentences) if i in range(10)]
    # meta = [s for i, s in enumerate(meta) if i in range(10)]
    # ------
    num_open_nodes = [i[settings.y_label] for i in meta]
    y = np.asarray([item for sublist in num_open_nodes for item in sublist])

# Load vocabulary
vocab = data.Dictionary(op.join(settings.path2LSTMdata, settings.vocabulary_file))

# Load LSTM model
print('Loading models...')
if preferences.load_pretested_LSTM:
    #Load LSTM data
    print('Loading pre-tested LSTM model on test sentences...')
    with open(op.join(settings.path2LSTMdata, settings.LSTM_pretested_file_name), "rb") as f:
        X = pickle.load(f)
else:
    pkl_filename_LSTM_data = 'LSTM_data_pretested_' + settings.LSTM_pretested_file_name
    X = extract_activations_from_LSTM.test_LSTM(sentences, vocab, settings.eos_separator, settings, False)
    print('Saving LSTM activations to Data folder...')
    with open(op.join(settings.path2LSTMdata, settings.LSTM_pretested_file_name), "wb") as f:
        pickle.dump(X, f)

sentences = None # clear from memory

X = [x.transpose() for x in X] # Transpose elements
X = np.vstack(X) # Reshape into a design matrix (num_words X num_units)

num_units = X.shape[1]
if settings.which_layer == 0:
    X = X
elif settings.which_layer == 1:
    X = X[:, 0:int(num_units/2)]
elif settings.which_layer == 2:
    X = X[:, int(num_units/2):]
else:
    sys.stderr('settings.which_layer has to be either 0, 1 or 2')

# If requested, omit zero depth, which mostly corresponds to full-stop, question marks, etc.
print(X.shape[0], y.shape[0])
if preferences.omit_zero_depth:
    IX = (y != 0)
    X = X[IX, :]

if settings.residuals_after_partial_out_word_position:
    with open(op.join(settings.path2output, settings.residuals_after_partial_out_word_position_file_name), 'rb') as f:
        models = pickle.load(f)
        y = models['residuals'] # Residuals are already with zero
        print('Loading y labels as residuals, after partialling out word position')
        if not preferences.omit_zero_depth:
            sys.stderr('Residuals are without zero depth. Set preferences.omit_zero_depth = True')

print(X.shape[0], y.shape[0])
# For DEBUG ------
# X = X[0:1000, :]
# y = y[0:1000]
# -------------

for seed_split in range(1, 6, 1):
    # ## Split data to train/test sets
    print('Splitting data to train/test sets; seed = ' + str(seed_split))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold, random_state=seed_split)
    pkl_filename = 'train_test_data_number_of_open_nodes_after_partial_out_word_position_' + settings.y_label + '_MODEL_' + \
                   settings.LSTM_pretrained_model + '_layer_' + str(
        settings.which_layer) + '_h_or_c_' + str(settings.h_or_c) + '_seed_' + str(seed_split) + '.pkl'
    with open(op.join(settings.path2data, 'Regression_open_nodes', pkl_filename), 'wb') as f:
        pickle.dump([X_train, X_test, y_train, y_test], f)
