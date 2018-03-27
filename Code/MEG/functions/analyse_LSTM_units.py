import os, mne
import numpy as np
#from Scripts import sentcomp_epoching
import pickle
import codecs
import matplotlib.pyplot as plt
from os import path as op

def get_stimuli_and_info(settings, params):
    # load rejected trials
    bad_trials = np.load(settings.bad_trials_file_name)

    # Load stimuli
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block2_300ms/stimuli.p'), 'r')
    run1 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block6_300ms/stimuli.p'), 'r')
    run2 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block0_300ms/stimuli.p'), 'r')
    run3 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block2_300ms/stimuli.p'), 'r')
    run4 = pickle.load(f)
    all_stim = run1 + run2 + run3 + run4 # concatenate all
    all_stim_clean = [i for j, i in enumerate(all_stim) if j not in bad_trials] # All stimuli without rejected trials

    # Load stimuli info
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block2_300ms/info_stim.p'), 'r')
    info1 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block6_300ms/info_stim.p'), 'r')
    info2 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block0_300ms/info_stim.p'), 'r')
    info3 = pickle.load(f)
    f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block2_300ms/info_stim.p'), 'r')
    info4 = pickle.load(f)
    all_info = info1 + info2 + info3 + info4 # concatenate all
    all_info_clean = [i for j, i in enumerate(all_info) if j not in bad_trials] # All stimuli info without rejected trials

    IX = [i for i in range(len(all_info_clean)) if all_info_clean[i]['anomaly']=='correct']
    all_info_correct=[i for j,i in enumerate(all_info_clean) if j in IX]

    # Split according to structures (structure = 1 is 4x4; 2 is 2x6; 3 is 6x2)
    IX_structure1 = [i for i in range(len(all_info_correct)) if all_info_correct[i]['structure']==1]
    IX_structure2 = [i for i in range(len(all_info_correct)) if all_info_correct[i]['structure']==2]
    IX_structure3 = [i for i in range(len(all_info_correct)) if all_info_correct[i]['structure']==3]

    return all_stim_clean, all_info_clean, all_info_correct, IX_structure1, IX_structure2, IX_structure3


def plot_units_activation(LSTM_data, labels, IX_structure1, IX_structure2, IX_structure3, settings, params):
    for unit in range(LSTM_data['gates.in'].shape[1]):
        print 'Unit ' + str(unit)
        fig, axarr = plt.subplots(2, 3)
        # Hidden units
        mean_h_activity_structure1 = np.mean(LSTM_data['vectors'][IX_structure1, unit, :], axis=0)
        std_h_activity_structure1 = np.std(LSTM_data['vectors'][IX_structure1, unit, :], axis=0)
        mean_h_activity_structure2 = np.mean(LSTM_data['vectors'][IX_structure2, unit, :], axis=0)
        std_h_activity_structure2 = np.std(LSTM_data['vectors'][IX_structure2, unit, :], axis=0)
        mean_h_activity_structure3 = np.mean(LSTM_data['vectors'][IX_structure3, unit, :], axis=0)
        std_h_activity_structure3 = np.std(LSTM_data['vectors'][IX_structure3, unit, :], axis=0)
        # Plot
        h1 = axarr[1, 2].errorbar(range(1, 9, 1), mean_h_activity_structure1, yerr=std_h_activity_structure1)
        h2 = axarr[1, 2].errorbar(range(1, 9, 1), mean_h_activity_structure2, yerr=std_h_activity_structure2)
        h3 = axarr[1, 2].errorbar(range(1, 9, 1), mean_h_activity_structure3, yerr=std_h_activity_structure3)
        axarr[1, 2].set_title('Hidden unit')
        axarr[1, 2].set_xlim(0, 9)
        axarr[1, 2].set_ylim(-1.1, 1.1)
        fig.legend((h1, h2, h3), labels, 'upper right')
        # Cells
        mean_c_activity_structure1 = np.mean(LSTM_data['vectors'][IX_structure1, 1000 + unit, :], axis=0)
        std_c_activity_structure1 = np.std(LSTM_data['vectors'][IX_structure1, 1000 + unit, :], axis=0)
        mean_c_activity_structure2 = np.mean(LSTM_data['vectors'][IX_structure2, 1000 + unit, :], axis=0)
        std_c_activity_structure2 = np.std(LSTM_data['vectors'][IX_structure2, 1000 + unit, :], axis=0)
        mean_c_activity_structure3 = np.mean(LSTM_data['vectors'][IX_structure3, 1000 + unit, :], axis=0)
        std_c_activity_structure3 = np.std(LSTM_data['vectors'][IX_structure3, 1000 + unit, :], axis=0)
        # Plot
        axarr[1, 1].errorbar(range(1, 9, 1), mean_c_activity_structure1, yerr=std_c_activity_structure1)
        axarr[1, 1].errorbar(range(1, 9, 1), mean_c_activity_structure2, yerr=std_c_activity_structure2)
        axarr[1, 1].errorbar(range(1, 9, 1), mean_c_activity_structure3, yerr=std_c_activity_structure3)
        axarr[1, 1].set_title('Cell')
        axarr[1, 1].set_xlim(0, 9)
        axarr[1, 1].set_ylim(-1.1, 1.1)

        for i, gate in enumerate([LSTM_data.files[i] for i in [3, 4, 5, 6]]):  # Loop over gates and c_tilda:
            # Gates/c_tilda
            mean_struct1 = np.mean(LSTM_data[gate][IX_structure1, unit, :], axis=0)
            std_struct1 = np.std(LSTM_data[gate][IX_structure1, unit, :], axis=0)
            mean_struct2 = np.mean(LSTM_data[gate][IX_structure2, unit, :], axis=0)
            std_struct2 = np.std(LSTM_data[gate][IX_structure2, unit, :], axis=0)
            mean_struct3 = np.mean(LSTM_data[gate][IX_structure3, unit, :], axis=0)
            std_struct3 = np.std(LSTM_data[gate][IX_structure3, unit, :], axis=0)
            # Plot
            axarr[i / 3, i % 3].errorbar(range(1, 9, 1), mean_struct1, yerr=std_struct1)
            axarr[i / 3, i % 3].errorbar(range(1, 9, 1), mean_struct2, yerr=std_struct2)
            axarr[i / 3, i % 3].errorbar(range(1, 9, 1), mean_struct3, yerr=std_struct3)
            axarr[i / 3, i % 3].set_title(gate)
            axarr[i / 3, i % 3].set_xlim(0, 9)
            axarr[i / 3, i % 3].set_ylim(-0.1, 1.1)
            if i == 3:
                axarr[i / 3, i % 3].set_ylim(-1.1, 1.1)

        file_name = 'units_activation_unit_' + str(unit)
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))
        plt.close(fig)

def plot_PCA_trajectories(LSTM_data, IX_structure1, IX_structure2, IX_structure3, settings, params):
    from sklearn import decomposition
    num_trials = LSTM_data['vectors'].shape[0]
    # Concatenate all timepoints before PCAing
    h = np.empty((0,1000))
    for timepoint in range(8):
        h = np.vstack((h, LSTM_data['vectors'][:,0:1000,timepoint]))

    # PCA
    pca = decomposition.PCA(n_components=2)
    pca.fit(h)
    h_pca = pca.transform(h)
    h_pca_sequence = np.empty((num_trials, 2, 8))
    for timepoint in range(8):
        st = num_trials * timepoint
        ed = num_trials * (timepoint + 1)
        h_pca_sequence[:,:,timepoint] = h_pca[st:ed, :]

    h_pca_sequence_mean_structure1 = np.mean(h_pca_sequence[IX_structure1, :, :], axis=0)
    h_pca_sequence_mean_structure2 = np.mean(h_pca_sequence[IX_structure2, :, :], axis=0)
    h_pca_sequence_mean_structure3 = np.mean(h_pca_sequence[IX_structure3, :, :], axis=0)

    fig, axarr = plt.subplots(1, 3, figsize=(20, 10))
    axarr[0].scatter(h_pca_sequence_mean_structure1[0, :], h_pca_sequence_mean_structure1[1, :], label='4-4', color='r')
    h1 = axarr[0].plot(h_pca_sequence_mean_structure1[0, :], h_pca_sequence_mean_structure1[1, :], color='r')
    axarr[0].scatter(h_pca_sequence_mean_structure2[0, :], h_pca_sequence_mean_structure2[1, :], color='g')
    h2 = axarr[0].plot(h_pca_sequence_mean_structure2[0, :], h_pca_sequence_mean_structure2[1, :], label='2-6', color='g')
    delta_x = 0.1*np.random.rand(1)
    for timepoint in range(8):
        axarr[0].annotate(str(timepoint + 1), xy=(
        delta_x + h_pca_sequence_mean_structure1[0, timepoint], delta_x + h_pca_sequence_mean_structure1[1, timepoint]), color='r')
    delta_x = 0.1 * np.random.rand(1)
    for timepoint in range(8):
        axarr[0].annotate(str(timepoint + 1), xy=(
        delta_x + h_pca_sequence_mean_structure2[0, timepoint], delta_x + h_pca_sequence_mean_structure2[1, timepoint]), color='g')
    axarr[0].legend()
    axarr[0].set_xlabel('PC1', fontsize=16)
    axarr[0].set_ylabel('PC2', fontsize=16)

    axarr[1].scatter(h_pca_sequence_mean_structure1[0, :], h_pca_sequence_mean_structure1[1, :], label='4-4', color='r')
    h1 = axarr[1].plot(h_pca_sequence_mean_structure1[0, :], h_pca_sequence_mean_structure1[1, :], color='r')
    axarr[1].scatter(h_pca_sequence_mean_structure3[0, :], h_pca_sequence_mean_structure3[1, :], color='b')
    h3 = axarr[1].plot(h_pca_sequence_mean_structure3[0, :], h_pca_sequence_mean_structure3[1, :], label='6-2', color='b')
    for timepoint in range(8):
        axarr[1].annotate(str(timepoint + 1), xy=(
        delta_x + h_pca_sequence_mean_structure1[0, timepoint], delta_x + h_pca_sequence_mean_structure1[1, timepoint]), color='r')
    delta_x = 0.1 * np.random.rand(1)
    for timepoint in range(8):
        axarr[1].annotate(str(timepoint + 1), xy=(
        delta_x + h_pca_sequence_mean_structure3[0, timepoint], delta_x + h_pca_sequence_mean_structure3[1, timepoint]), color='b')
    axarr[1].legend()
    axarr[1].set_xlabel('PC1', fontsize=16)
    axarr[1].set_ylabel('PC2', fontsize=16)

    axarr[2].scatter(h_pca_sequence_mean_structure2[0, :], h_pca_sequence_mean_structure2[1, :], label='2-6', color='g')
    h2 = axarr[2].plot(h_pca_sequence_mean_structure2[0, :], h_pca_sequence_mean_structure2[1, :], color='g')
    axarr[2].scatter(h_pca_sequence_mean_structure3[0, :], h_pca_sequence_mean_structure3[1, :], label='6-2', color='b')
    h3 = axarr[2].plot(h_pca_sequence_mean_structure3[0, :], h_pca_sequence_mean_structure3[1, :], color='b')
    for timepoint in range(8):
        axarr[2].annotate(str(timepoint + 1), xy=(
        delta_x + h_pca_sequence_mean_structure2[0, timepoint], delta_x + h_pca_sequence_mean_structure2[1, timepoint]), color='g')
    delta_x = 0.1 * np.random.rand(1)
    for timepoint in range(8):
        axarr[2].annotate(str(timepoint + 1), xy=(
            delta_x + h_pca_sequence_mean_structure3[0, timepoint],
            delta_x + h_pca_sequence_mean_structure3[1, timepoint]), color='b')
    axarr[2].legend()
    axarr[2].set_xlabel('PC1', fontsize=16)
    axarr[2].set_ylabel('PC2', fontsize=16)

    return fig