import math
import os.path as op
import numpy as np
import matplotlib.pyplot as plt
import mne
from functions import sentcomp_epoching

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


def plot_topomap_optimal_bin(settings, params):

    # Load f-statistic results from Output folder
    f_stats_all = []
    for channel in range(settings.num_MEG_channels):
        file_name = 'MEG_data_sentences_averaged_over_optimal_bin_channel_' + str(channel + 1) + '.npz'
        npzfile = np.load(op.join(settings.path2output, file_name))
        f_stats_all.append(npzfile['arr_1'])

    num_bin_sizes, num_bin_centers = f_stats_all[0].shape

    # Load epochs data from fif file, which includes channel loactions
    epochs = mne.read_epochs(op.join(settings.path2MEGdata, settings.raw_file_name))

    # Generate epochs locked to anomalous words
    anomaly = 0  # 0: normal, 1: nonword (without vowels), 2: syntactic, 3: semantic
    position = [4, 6, 8]  # 0,1,2..8
    responses = [0, 1]  # Correct/wrong response of the subject
    structures = [1, 2, 3]  # 1: 4-4, 2: 2-6, 3: 6-2

    conditions = dict([
        ('Anomalies', [anomaly]),
        ('Positions', position),
        ('Responses', responses),
        ('Structure', structures)])

    knames1, _ = sentcomp_epoching.get_condition(conditions=conditions, epochs=epochs, startTime=-.2,
                                                   duration=1.5, real_speed=params.real_speed/1e3)

    epochs_curr_condition = epochs[knames1]

    # Generate fake power spectrum, to be replace with f-stat later
    freqs = range(51,51 + num_bin_sizes,1); n_cycles = 1
    power = mne.time_frequency.tfr_morlet(epochs_curr_condition, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                                          decim=3, n_jobs=4)
    f_stat_object = power[0]
    f_stat_object._data = np.rollaxis(np.dstack(f_stats_all), -1)
    fig_topo = f_stat_object.plot_topo(layout_scale=1.1, title='F-statistic for varying bin sizes and centers', vmin=0, vmax=5,
                            fig_facecolor='w', font_color='k', show=False)


    f_stat_object.times = np.asarray(range(1,num_bin_centers,1))
    f_stat_object.freqs = np.asarray(freqs)

    #subplot_square_side = math.ceil(np.sqrt(num_bin_centers))

    for i, t in enumerate(f_stat_object.times):
        curr_fig = f_stat_object.plot_topomap(tmin=t, tmax=t, fmin=np.min(freqs), fmax=1 + np.min(freqs), show=False)
        file_name = 'f_stats_topomap_patient_' + settings.patient + '_time_' + str(t)
        plt.savefig(op.join(settings.path2figures, file_name))
        plt.close(curr_fig)

    return fig_topo