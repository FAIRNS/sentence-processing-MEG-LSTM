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
import matplotlib.pyplot as plt

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
    X = [word_position for s in sentences for word_position, _ in enumerate(s)]
    X = np.expand_dims(np.asarray(X), axis=1)
# Load vocabulary
vocab = data.Dictionary(op.join(settings.path2LSTMdata, settings.vocabulary_file))
X = X + 1

del sentences # clear from memory

if preferences.omit_zero_depth:
    IX = (y != 0)
    X = X[IX, :]
    y = y[IX]
print(X.shape[0], y.shape[0])

# For DEBUG ------
# X = X[0:500, :]
# y = y[0:500]
# -------------

pkl_filename = 'Regression_number_of_open_nodes_from_word_position_' + settings.y_label + '.pckl'

if preferences.run_Ridge:
    pkl_filename = 'Ridge_' + pkl_filename
if preferences.run_LASSO:
    pkl_filename = 'LASSO_' + pkl_filename
if preferences.run_ElasticNet:
    pkl_filename = 'ElasticNet_' + pkl_filename
print(pkl_filename)
if not op.exists(op.join(settings.path2output, pkl_filename)) or preferences.override_previous_runs:

    # ## Split data to train/test sets
    # print('Splitting data to train/test sets')
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold,
    #                                                 random_state=params.seed_split)
    # del X, y # Clear from memory

    models = {}
    # ############ Ridge Regression ############
    if preferences.run_Ridge:
        print('Fitting a Ridge regression model')
        settings.method = 'Ridge'
        # Train model
        model_ridge = mfe.train_model(X, y, settings, params)
        # Evaluate model on test set
        ridge_scores_test = mfe.evaluate_model(model_ridge, X, y, settings, params)

        y_predicted = model_ridge.predict(X)

        # Generate and save figures
        # plt = pr.regularization_path(model_ridge, settings, params)
        # file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_word_position.png'
        # plt.savefig(op.join(settings.path2figures, file_name))
        # plt.close()
        models['model_ridge'] = model_ridge
        models['ridge_scores_test'] = ridge_scores_test
        models['residuals'] = y - y_predicted

        # Plot outputs
        file_name = 'Regression_depth_from_word_position.png'
        fig, ax = plt.subplots(figsize=[30, 20])
        plt.hist2d(X[:,0], y, bins=range(31), cmap=plt.cm.YlOrRd)
        h_cb = plt.colorbar()
        h_cb.set_label('Number of words', fontsize=20)
        ax.plot(X, y_predicted, color='blue', linewidth=3)
        ax.set_xlabel('Word position', fontsize=30)
        ax.set_ylabel('Tree depth', fontsize=30)
        ax.set_ylim([0, 12])
        ax.text(1, 8, 'y = %1.2fx + %1.2f' % (models['model_ridge'].coefs[models['model_ridge'].best_index_], models['model_ridge'].intercepts[models['model_ridge'].best_index_]), fontsize=30)
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.tick_params(axis='both', which='minor', labelsize=20)
        # plt.tight_layout()
        plt.savefig(op.join(settings.path2figures, file_name))

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
