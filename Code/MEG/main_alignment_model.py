import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import plot_results as pr
import sys
import pickle

# --------- Main script -----------
vector_type = 'hidden'
print('Vector type: ' + vector_type)
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
# os.chdir(settings.path2code)
# print(os.getcwd())

# Load LSTM data
print('Loading pre-trained LSTM data...')
# LSTM_data = np.load(op.join(settings.path2LSTMdata, settings.LSTM_file_name))
# print(LSTM_data.files)
# LSTM_data = LSTM_data['vectors']
# print(LSTM_data.shape)
#sys.exit('breaked by user in code')
with open(op.join(settings.path2LSTMdata, settings.LSTM_file_name), 'rb') as f:
	LSTM_data = pickle.load(f)

LSTM_data = np.asarray(LSTM_data[vector_type])

# Loop over channels and fit a regression model between LSTM units and MEG channel
if len(sys.argv) > 1:
    print('Channel ' + sys.argv[1])
    channel = int(sys.argv[1])
    if len(sys.argv) > 2:
        print('Time point ' + sys.argv[2])
        time_point = int(sys.argv[2])
else:
    channel = 1
    time_point = 1

# for channel in range(channel, channel+10, 1):
    # If using optimal bin so don't loop over each time point within SOA
step = 10
if settings.use_optimal_bin:
    time_points = [-1]
else:
    time_points = range(0, params.SOA+1, step)

for time_point in time_points:
	pkl_filename = 'Regression_models_' + settings.patient + '_channel_' + str(channel) + '_timepoint_' + str(time_point) + '_averaged_over_' + str(step) + '_' + settings.LSTM_file_name + '.pckl'
	if not op.exists(op.join(settings.path2output, pkl_filename)):
		# Load Data
		print('Loading MEG data for channel ' + str(channel) + ' time point ' + str(time_point) + '...')
		if settings.use_optimal_bin:
			MEG_file_name = 'MEG_data_sentences_averaged_over_optimal_bin_channel_' + str(channel) + '.npz'
			MEG_data = np.load(op.join(settings.path2output, MEG_file_name))
		else:
			if settings.use_sources_data:
				MEG_file_name = 'sources/sources_dat_' + settings.patient + '_vertex_' + str(channel) + '.pkl'
				with open(op.join(settings.path2MEGdata, MEG_file_name), 'rb') as f:
					MEG_data = pickle.load(f, encoding='latin1')
			else:
				MEG_file_name = 'patient_' + settings.patient +'_epochs_lock_to_beginning_of_sentence_anomaly_type_0.npy'
				MEG_data = np.load(op.join(settings.path2MEGdata, MEG_file_name))
			real_speed_sec = int(params.sfreq * params.real_speed / 1e3)
			st = int(params.sfreq * params.startTime / 1e3) + time_point
			ed = st + real_speed_sec*8 # the same time point at the 8^th words
			IX_timepoints = np.arange(st, ed, real_speed_sec)
			print('timepoints ' + str(IX_timepoints))
			if not settings.use_sources_data:
				MEG_data = MEG_data[:,channel-1, :]


		# Reshape data to num_trials X num_features
		print('Reshaping datasets')
		num_trials, num_hidden_units, num_timepoints = LSTM_data.shape
		X = np.empty([0, num_hidden_units]) # LSTM data
		y = np.empty([0]) # MEG data
		for word in range(8):
			X = np.vstack((X, LSTM_data[:,:, word]))
			if settings.use_optimal_bin:
				y = np.hstack((y, MEG_data['arr_0'][:, word]))
			else:
				st = IX_timepoints[word]
				ed = st + step - 1
				MEG_data_mean = np.mean(MEG_data[:, st:ed], axis=1)
				y = np.hstack((y, MEG_data_mean))

	    # ## Split data to train/test sets
		print('Splitting data to train/test sets')
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1./params.CV_fold,
		                                                random_state=params.seed_split)

		models = {}
		# ############ Ridge Regression ############
		if settings.run_Ridge:
			print('Fitting a ridge model for channel ' + str(channel) + ' time point ' + str(time_point))
			settings.method = 'Ridge'
			# Train model
			model_ridge = mfe.train_model(X_train, y_train, settings, params)
			# Evaluate model on test set
			ridge_scores_test = mfe.evaluate_model(model_ridge, X_test, y_test, settings, params)
			# Generate and save figures
			plt = pr.regularization_path(model_ridge, settings, params)
			file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_channel_' + \
						str(channel) + '.png'
			plt.savefig(op.join(settings.path2figures, file_name))
			plt.close()
			models['model_ridge'] = model_ridge
			models['ridge_scores_test'] = ridge_scores_test
		# ##########################################

	    # ############ Lasso Regression ############
		if settings.run_LASSO:
			print('Fitting a lasso model for channel ' + str(channel) + ' time point ' + str(time_point))
			settings.method = 'Lasso'
			# Train model
			model_lasso = mfe.train_model(X_train, y_train, settings, params)
			# Evaluate model on test set
			lasso_scores_test = mfe.evaluate_model(model_lasso, X_test, y_test, settings, params)
			# Generate and save figures
			plt = pr.regularization_path(model_lasso, settings, params)
			file_name = 'Lasso_coef_and_R_squared_vs_regularization_size_channel_' + \
						str(channel) + '_timepoint_' + str(time_point) + '.png'
			plt.savefig(op.join(settings.path2figures, file_name))
			plt.close()
			models['model_lasso'] = model_lasso
			models['lasso_scores_test'] = lasso_scores_test
			print('Done fitting')
	    # ##########################################

	    # ############ Elastic-net Regression #####
		if settings.run_ElasticNet:
			print('Fitting an elastic-net model for channel ' + str(channel))
			settings.method = 'Elastic_net'
			model_enet = mfe.train_model(X_train, y_train, settings, params)
			# Evaluate model on test set
			enet_scores_test = mfe.evaluate_model(model_enet, X_test, y_test, settings, params)
			# Generate and save figures
			plt = pr.regularization_path(model_enet, settings, params)
			file_name = 'Elastic_net_coef_and_R_squared_vs_regularization_size_channel_' + \
						str(channel) + '.png'
			plt.savefig(op.join(settings.path2figures, file_name))
			plt.close()
			models['model_enet'] = model_enet
			models['enet_scores_test'] = model_enet
	    # ##########################################

	    # ############# Save models and results #####
		import pickle
		with open(op.join(settings.path2output, pkl_filename), "wb") as f:
		    pickle.dump(models, f)
		    pickle.dump(settings, f)
		    pickle.dump(params, f)
		print('Models for channel ' + str(channel) + ' time point ' + str(time_point) + 'were saved to Output folder')
