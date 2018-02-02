import time
from itertools import cycle
import os.path as op
import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model

class settings:
    def __init__(self):
        self.path2MEGdata = op.join('..', 'Data', 'MEG', 'am150105', 'am150105')
        self.path2LSTMdata = op.join('..', 'Data', 'LSTM')
        self.path2figures = op.join('..', 'Figures')
        self.path2output = op.join('..', 'Output')
        self.MEG_file_name = 'patient_am150105_epochs_lock_to_beginning_of_sentence_anomaly_type_0.npy'
        self.LSTM_file_name = 'vectors-LSTM1000-0.npy'


class params:
    def __init__(self):
        self.SOA = 300 # [msec]
        self.real_spead = 301 # [msec]
        self.sfreq = 200 # [Hz]
        self.bin_size = self.SOA # [msec]
        self.bin_size = int(self.sfreq * self.bin_size / 1e3) #[samples]
        self.startTime = 760 #[msec]
        self.seed_split = 1 # random seed for split


def train_model(MEG_data, LSTM_data, settings, params):
    test_size = 0.2 # 5-fold
    for word in range(8):
        # Split data
        print('Split train/test data')
        X_train, X_test, y_train, y_test = train_test_split(LSTM_data[:,:, word], MEG_data[:, word],
                                                            test_size=test_size, random_state=params.seed_split)
        # #############################################################################
        # Compute paths

        n_alphas = 200
        alphas = np.logspace(-10, -2, n_alphas)

        coefs = []
        scores = []
        for a in alphas:
            model_ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
            model_ridge.fit(X_train, y_train)
            coefs.append(model_ridge.coef_)
            scores.append(model_ridge.score(X_test, y_test))
        print('Ridge model fitted for channel ' + str(channel) + ' word ' + str(word + 1))
        # #############################################################################
        # Display results
        fig, ax1 = plt.subplots()
        ax1.plot(alphas, coefs)
        ax1.set_xscale('log')
        ax1.set_xlim(ax1.get_xlim()[::-1])  # reverse axis
        ax1.set_xlabel('alpha')
        ax1.set_ylabel('weights')
        plt.title('Ridge coefficients as a function of the regularization')
        ax2=ax1.twinx()
        ax2.plot(alphas, scores, 'r.')
        ax2.set_ylabel('R^2', color='r')
        ax2.tick_params('y', colors='r')
        plt.axis('tight')
        file_name = 'Ridge_coef_and_R_squared_vs_regularization_size_channel_' + \
                    str(channel) + '_word_' + str(word+1)+'.png'
        plt.savefig(op.join(settings.path2figures, file_name))
        plt.close()
        # LASSO
        eps = 5e-3  # the smaller it is the longer is the path

        t1 = time.time()
        model_lasso = linear_model.LassoCV(cv=5, eps=eps).fit(X_train, y_train)
        t_lasso_cv = time.time() - t1
        print('Lasso model fitted for channel ' + str(channel) + ' word ' + str(word + 1))
        # Display results
        m_log_alphas = -np.log10(model_lasso.alphas_)

        plt.figure()
        #ymin, ymax = 2300, 3800
        plt.plot(m_log_alphas, model_lasso.mse_path_, ':')
        plt.plot(m_log_alphas, model_lasso.mse_path_.mean(axis=-1), 'k',
                 label='Average across the folds', linewidth=2)
        plt.axvline(-np.log10(model_lasso.alpha_), linestyle='--', color='k',
                    label='alpha: CV estimate')

        plt.legend()

        plt.xlabel('-log(alpha)')
        plt.ylabel('Mean square error')
        plt.title('Mean square error on each fold: coordinate descent '
                  '(train time: %.2fs)' % t_lasso_cv)
        plt.axis('tight')

        file_name = 'Lasso_mean_square_error_vs_regularization_size_channel_' + \
                    str(channel) + '_word_' + str(word + 1) + '.png'
        plt.savefig(op.join(settings.path2figures, file_name))
        print('Plots saved for channel ' + str(channel) + ' word ' + str(word + 1))


        print("Computing regularization path using the lasso...")
        alphas_lasso, coefs_lasso, _ = linear_model.lasso_path(X_train, y_train, eps, fit_intercept=False)
        print("Computing regularization path using the elastic net...")
        alphas_enet, coefs_enet, _ = linear_model.enet_path(
            X_train, y_train, eps=eps, l1_ratio=0.8, fit_intercept=False)
        # Display results

        plt.figure()
        ax = plt.gca()

        colors = cycle(['b', 'r', 'g', 'c', 'k'])
        neg_log_alphas_lasso = -np.log10(alphas_lasso)
        neg_log_alphas_enet = -np.log10(alphas_enet)
        for coef_l, coef_e, c in zip(coefs_lasso, coefs_enet, colors):
            l1 = plt.plot(neg_log_alphas_lasso, coef_l, c=c)
            l2 = plt.plot(neg_log_alphas_enet, coef_e, linestyle='--', c=c)

        plt.xlabel('-Log(alpha)')
        plt.ylabel('coefficients')
        plt.title('Lasso and Elastic-Net Paths')
        plt.legend((l1[-1], l2[-1]), ('Lasso', 'Elastic-Net'), loc='lower left')
        plt.axis('tight')

        file_name = 'Lasso_elastic_net_coef_vs_regularization_size_channel_' + \
                         str(channel) + '_word_' + str(word + 1) + '.png'
        plt.savefig(op.join(settings.path2figures, file_name))
        print('Plots saved for channel ' + str(channel) + ' word ' + str(word + 1))

        #plt.ylim(ymin, ymax)
    return model


# --------- Main script -----------
print('Load settings and parameters')
settings = settings()
params = params()

num_channels = 306
print('Loading pre-trained LSTM data...')
LSTM_data = np.load(op.join(settings.path2LSTMdata, settings.LSTM_file_name))
for channel in range(num_channels):
    # Load Data
    print('Loading MEG data for channel ' + str(channel) + '...')
    MEG_file_name = 'MEG_data_sentences_averaged_over_optimal_bin_channel_' +str(channel) +'.npz.npy'
    MEG_data = np.load(op.join(settings.path2output, MEG_file_name))
    # Train regression model between MEG and LSTM data
    model = train_model(MEG_data, LSTM_data, settings, params)

