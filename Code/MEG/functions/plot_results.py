from itertools import cycle
import math
import numpy as np
import matplotlib.pyplot as plt


def regularization_path(model, settings, params):
    fig, ax1 = plt.subplots()

    # Plot regression coef for each regularization size (alpha)
    ax1.plot(model.alphas, model.coefs)
    ax1.set_xscale('log')
    # ax1.set_xlim(ax1.get_xlim()[::-1])  # reverse axis
    ax1.set_xlabel('Regularization size')
    ax1.set_ylabel('weights')
    plt.title(settings.method + ' regression')

    # Plot error on the same figure
    ax2 = ax1.twinx()
    scores = model.cv_results_['mean_test_score']
    scores_std = model.cv_results_['std_test_score']
    std_error = scores_std / np.sqrt(params.CV_fold)
    ax2.plot(model.alphas, scores, 'r.')
    ax2.fill_between(model.alphas, scores + std_error, scores - std_error, alpha=0.2)
    ax2.set_ylabel('R-square', color='r')
    ax2.tick_params('y', colors='r')

    scores_train = model.cv_results_['mean_train_score']
    scores_train_std = model.cv_results_['std_train_score']
    std_train_error = scores_train_std / np.sqrt(params.CV_fold)
    ax2.plot(model.alphas, scores_train, 'g.')
    ax2.fill_between(model.alphas, scores_train + std_train_error, scores_train - std_train_error, alpha=0.2)

    plt.axis('tight')

    return plt


# plt.figure()
#     # ymin, ymax = 2300, 3800
#     plt.plot(m_log_alphas, model_lasso.mse_path_, ':')
#     plt.plot(m_log_alphas, model_lasso.mse_path_.mean(axis=-1), 'k',
#              label='Average across the folds', linewidth=2)
#     plt.axvline(-np.log10(model_lasso.alpha_), linestyle='--', color='k',
#                 label='alpha: CV estimate')
#
#     plt.legend()
#
#     plt.xlabel('-log(alpha)')
#     plt.ylabel('Mean square error')
#     plt.title('Mean square error on each fold: coordinate descent '
#               '(train time: %.2fs)' % t_lasso_cv)
#     plt.axis('tight')
#
#     file_name = 'Lasso_mean_square_error_vs_regularization_size_channel_' + \
#                 str(channel) + '_word_' + str(word + 1) + '.png'
#     plt.savefig(op.join(settings.path2figures, file_name))
#     print('Plots saved for channel ' + str(channel) + ' word ' + str(word + 1))
