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

# Load Stimuli
print('Loading number of open nodes data')
with open(op.join(settings.path2LSTMdata, settings.bnc_data), 'rb') as f:
    stimuli = pickle.load(f)
    sentences = [i[0] for i in stimuli]
    meta = [i[2] for i in stimuli]
    stimuli = None # clear from memory
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
    X = extract_activations_from_LSTM.test_LSTM(sentences, vocab, settings.eos_separator, settings, True)
    print('Saving LSTM activations to Data folder...')
    with open(op.join(settings.path2LSTMdata, settings.LSTM_pretested_file_name), "wb") as f:
        pickle.dump(X, f)

sentences = None # clear from memory

X = [x.transpose() for x in X] # Transpose elements
X = np.vstack(X) # Reshape into a design matrix (num_words X num_units)

# For DEBUG ------
# X = X[0:500, :]
# y = y[0:500]
# -------------

pkl_filename = 'Regression_number_of_open_nodes_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_h_or_c_' + str(settings.h_or_c)  + '_seed_' + str(params.seed_split) + '.pckl'
if preferences.run_Ridge:
    pkl_filename = 'Ridge_' + pkl_filename
if preferences.run_LASSO:
    pkl_filename = 'LASSO_' + pkl_filename
if preferences.run_ElasticNet:
    pkl_filename = 'ElasticNet_' + pkl_filename

if not op.exists(op.join(settings.path2output, pkl_filename)):

    # ## Split data to train/test sets
    print('Splitting data to train/test sets')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold,
                                                    random_state=params.seed_split)
    X = None; y = None # Clear these from memory

    models = {}
    # ############ Ridge Regression ############
    if preferences.run_Ridge:
        print('Fitting a Ridge regression model')
        settings.method = 'Ridge'
        # Train model
        model_ridge = mfe.train_model(X_train, y_train, settings, params)
        # Evaluate model on test set
        ridge_scores_test = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)
        # Generate and save figures
        # plt = pr.regularization_path(model_ridge, settings, params)
        file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_channel_' + \
                     '.png'
        # plt.savefig(op.join(settings.path2figures, file_name))
        # plt.close()
        models['model_ridge'] = model_ridge
        models['ridge_scores_test'] = ridge_scores_test
    # ##########################################

    # ############ Lasso Regression ############
    if preferences.run_LASSO:
        print('Fitting a lasso model')
        settings.method = 'Lasso'
        # Train model
        model_lasso = mfe.train_model(X_train, y_train, settings, params)
        # Evaluate model on test set
        lasso_scores_test = mfe.evaluate_model(model_lasso, X_test, y_test, settings, params)
        # Generate and save figures
        # plt = pr.regularization_path(model_lasso, settings, params)
        file_name = 'Lasso_coef_and_R_squared_vs_regularization_size.png'
        # plt.savefig(op.join(settings.path2figures, file_name))
        # plt.close()
        models['model_lasso'] = model_lasso
        models['lasso_scores_test'] = lasso_scores_test
        print('Done fitting')
    # ##########################################

    # ############ Elastic-net Regression #####
    if preferences.run_ElasticNet:
        print('Fitting an elastic-net model for channel ')
        settings.method = 'Elastic_net'
        model_enet = mfe.train_model(X_train, y_train, settings, params)
        # Evaluate model on test set
        enet_scores_test = mfe.evaluate_model(model_enet, X_test, y_test, settings, params)
        # Generate and save figures
        # plt = pr.regularization_path(model_enet, settings, params)
        file_name = 'Elastic_net_coef_and_R_squared_vs_regularization_size_channel_' + '.png'
        # plt.savefig(op.join(settings.path2figures, file_name))
        # plt.close()
        models['model_enet'] = model_enet
        models['enet_scores_test'] = model_enet
    # ##########################################

    # ############# Save models and results #####
    with open(op.join(settings.path2output, pkl_filename), "wb") as f:
        pickle.dump(models, f)
        pickle.dump(settings, f)
        pickle.dump(params, f)
    print('Models were saved to Output folder')
