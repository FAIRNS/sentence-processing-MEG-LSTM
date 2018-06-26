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

# # Load LSTM model
# print('Loading models...')
# if preferences.load_pretested_LSTM:
#     #Load LSTM data
#     print('Loading pre-tested LSTM model on test sentences...')
#     with open(op.join(settings.path2LSTMdata, settings.LSTM_pretested_file_name), "rb") as f:
#         X = pickle.load(f)
# else:
#     pkl_filename_LSTM_data = 'LSTM_data_pretested_' + settings.LSTM_pretested_file_name
#     X = extract_activations_from_LSTM.test_LSTM(sentences, vocab, settings.eos_separator, settings, False)
#     print('Saving LSTM activations to Data folder...')
#     with open(op.join(settings.path2LSTMdata, settings.LSTM_pretested_file_name), "wb") as f:
#         pickle.dump(X, f)
#
# sentences = None # clear from memory
#
# X = [x.transpose() for x in X] # Transpose elements
# X = np.vstack(X) # Reshape into a design matrix (num_words X num_units)
#
# num_units = X.shape[1]
# if settings.which_layer == 0:
#     X = X
# elif settings.which_layer == 1:
#     X = X[:, 0:int(num_units/2)]
# elif settings.which_layer == 2:
#     X = X[:, int(num_units/2):]
# else:
#     sys.stderr('settings.which_layer has to be either 0, 1 or 2')
#
# # If requested, omit zero depth, which mostly corresponds to full-stop, question marks, etc.
# print(X.shape[0], y.shape[0])
# if preferences.omit_zero_depth:
#     IX = (y != 0)
#     X = X[IX, :]
#
# if settings.residuals_after_partial_out_word_position:
#     with open(op.join(settings.path2output, settings.residuals_after_partial_out_word_position_file_name), 'rb') as f:
#         models = pickle.load(f)
#         y = models['residuals'] # Residuals are already with zero
#         print('Loading y labels as residuals, after partialling out word position')
#         if not preferences.omit_zero_depth:
#             sys.stderr('Residuals are without zero depth. Set preferences.omit_zero_depth = True')
#
# print(X.shape[0], y.shape[0])
# For DEBUG ------
# X = X[0:1000, :]
# y = y[0:1000]
# -------------

pkl_filename = 'Regression_number_of_open_nodes_after_partial_out_word_position_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_layer_' + str(settings.which_layer) + '_h_or_c_' + str(settings.h_or_c)  + '_seed_' + str(params.seed_split) + '.pckl'

if preferences.run_Ridge:
    pkl_filename = 'Ridge_' + pkl_filename
if preferences.run_LASSO:
    pkl_filename = 'LASSO_' + pkl_filename
if preferences.run_ElasticNet:
    pkl_filename = 'ElasticNet_' + pkl_filename
print(pkl_filename)
if not op.exists(op.join(settings.path2output, pkl_filename)) or preferences.override_previous_runs:
    split_filename = 'train_test_data_number_of_open_nodes_after_partial_out_word_position_' + settings.y_label + '_MODEL_' + settings.LSTM_pretrained_model + '_layer_' + str(
        settings.which_layer) + '_h_or_c_' + str(settings.h_or_c) + '_seed_' + str(params.seed_split) + '.pckl'

    # ## Split data to train/test sets
    with open(op.join(settings.path2data, split_filename), 'rb') as f:
        data = pickle.load(f)
    # print('Splitting data to train/test sets')
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold,
    #                                                 random_state=params.seed_split)
    # X = None; y = None # Clear these from memory

    models = {}
    # ############ Ridge Regression ############
    if preferences.run_Ridge:
        print('Fitting a Ridge regression model')
        settings.method = 'Ridge'
        # Train model
        model_ridge = mfe.train_model(data['X_train'], data['y_train'], settings, params)
        # Evaluate model on test set
        ridge_scores_test, MSE_per_depth_test = mfe.evaluate_model(model_ridge, data['X_test'], data['y_test'], settings, params)
        print(ridge_scores_test)
        MSE_per_depth_train = []
        if settings.calc_MSE_per_each_depth:
            for depth in set(data['y_train']):
                X_train_curr_depth = data['X_train'][data['y_train'] == depth, :]
                y_train_curr_depth = data['y_train'][data['y_train'] == depth]
                y_predicted_curr_depth = model_ridge.predict(X_train_curr_depth)
                scores_curr_depth = ((y_train_curr_depth - y_predicted_curr_depth) ** 2).sum() / y_train_curr_depth.shape[0]
                MSE_per_depth_train.append([depth, scores_curr_depth])
        print(MSE_per_depth_train)
        print(MSE_per_depth_test)

        # Generate and save figures
        # plt = pr.regularization_path(model_ridge, settings, params)
        file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_channel_' + \
                     '.png'
        # plt.savefig(op.join(settings.path2figures, file_name))
        # plt.close()
        models['model_ridge'] = model_ridge
        models['ridge_scores_test'] = ridge_scores_test
        models['MSE_per_depth_train'] = MSE_per_depth_train
        models['MSE_per_depth_test'] = MSE_per_depth_test
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
