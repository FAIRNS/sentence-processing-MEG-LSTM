import os.path as op
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import plot_results as pr

# --------- Main script -----------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

# Load LSTM data
print('Loading pre-trained LSTM data...')
LSTM_data = np.load(op.join(settings.path2LSTMdata, settings.LSTM_file_name))

# Loop over channels and fit a regression model between LSTM units and MEG channel
for channel in range (227,230,1): #range(params.num_channels):
    # Load Data
    print('Loading MEG data for channel ' + str(channel+1) + '...')
    MEG_file_name = 'MEG_data_sentences_averaged_over_optimal_bin_channel_' +str(channel+1) +'.npy'
    MEG_data = np.load(op.join(settings.path2output, MEG_file_name))

    # Reshape data to num_trials X num_features
    print('Reshaping datasets')
    num_trials, num_hidden_units, num_timepoints = LSTM_data.shape
    X = np.empty([0, num_hidden_units]) # LSTM data
    y = np.empty([0]) # MEG data
    for word in range(8):
        X = np.vstack((X, LSTM_data[:,:, word]))
        y = np.hstack((y, MEG_data[:, word]))

    # ## Split data to train/test sets
    print('Splitting data to train/test sets')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold,
                                                        random_state=params.seed_split)
    # ############ Ridge Regression ############
    print('Fitting a ridge model for channel ' + str(channel+1))
    settings.method = 'Ridge'
    # Train model
    model_ridge = mfe.train_model(X_train, y_train, settings, params)
    # Evaluate model on test set
    ridge_scores_test = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)
    # Generate and save figures
    plt = pr.regularization_path(model_ridge, settings, params)
    file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_channel_' + \
                str(channel+1) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close()
    # ##########################################

    # ############ Lasso Regression ############
    print('Fitting a lasso model for channel ' + str(channel+1))
    settings.method = 'Lasso'
    # Train model
    model_lasso = mfe.train_model(X_train, y_train, settings, params)
    # Evaluate model on test set
    lasso_scores_test = mfe.evaluate_model(model_lasso, X_test, y_test, settings, params)
    # Generate and save figures
    plt = pr.regularization_path(model_lasso, settings, params)
    file_name = 'Lasso_coef_and_R_squared_vs_regularization_size_channel_' + \
                str(channel+1) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close()
    # ##########################################

    # ############ Elastic-net Regression #####
    print('Fitting an elastic-net model for channel ' + str(channel))
    settings.method = 'Elastic_net'
    model_enet = mfe.train_model(X_train, y_train, settings, params)
    # Evaluate model on test set
    enet_scores_test = mfe.evaluate_model(model_enet, X_test, y_test, settings, params)
    # Generate and save figures
    plt = pr.regularization_path(model_enet, settings, params)
    file_name = 'Elastic_net_coef_and_R_squared_vs_regularization_size_channel_' + \
                str(channel + 1) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close()
    # ##########################################