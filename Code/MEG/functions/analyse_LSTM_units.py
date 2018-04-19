import os\
    # , mne
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
        print('Unit ' + str(unit))
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

def plot_PCA_trajectories(data, IX_structures, labels, colors, settings, params):
    # input:
    # data (ndarray): num_trails X num_features X num_timepoints
    # Return:
    # fig - figure handle to subplots for each syntactic structure
    # fig_tuple - figure handle to subplots for each pair of syntactic structures compared on the same plot
    from sklearn import decomposition
    from sklearn import preprocessing
    import itertools

    num_trials = data.shape[0]
    num_dim = data.shape[1]
    num_structures = len(IX_structures)

    # Reshape: concatenate all timepoints before PCAing (num_trials*num_timepoints X num_features)
    vectors = np.empty((0, num_dim))
    for timepoint in range(8):
        vectors = np.vstack((vectors, data[:, :, timepoint]))

    # standardization of the data before PCA
    standardized_scale = preprocessing.StandardScaler().fit(vectors)
    vectors_standardized = standardized_scale.transform(vectors)

    # PCA
    pca = decomposition.PCA(n_components=2)
    pca.fit(vectors_standardized)
    vectors_PCA_projected = pca.transform(vectors_standardized)

    # Reshape back to num_trials X num_PCs X num_timepoints
    vector_PCA_trajectories = np.empty((num_trials, 2, 8))
    for timepoint in range(8):
        st = num_trials * timepoint
        ed = num_trials * (timepoint + 1)
        vector_PCA_trajectories[:, :, timepoint] = vectors_PCA_projected[st:ed, :]

    # Average across each syntactic structure type
    vectors_pca_trajectories_mean_over_structure = []; vectors_pca_trajectories_std_structure = []
    for i, IX_structure in enumerate(IX_structures):
        vectors_pca_trajectories_mean_over_structure.append(np.mean(vector_PCA_trajectories[IX_structure, :, :], axis=0))
        vectors_pca_trajectories_std_structure.append(np.std(vector_PCA_trajectories[IX_structure, :, :], axis=0))

    # Plot averaged trajectories for all structures
    fig, axarr = plt.subplots(1, num_structures, figsize=(20, 10))
    for i in range(num_structures):
        axarr[i].scatter(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :], label=labels[i], color=colors[i])
        axarr[i].errorbar(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :],
                          xerr=vectors_pca_trajectories_std_structure[i][0, :],
                          yerr=vectors_pca_trajectories_std_structure[i][1, :],
                          color=colors[i])

        # Annotate with number the subsequent time points on the trajectories
        delta_x = 0.03 # Shift the annotation of the time point by a small step
        for timepoint in range(8):
            axarr[i].annotate(str(timepoint + 1), xy=(delta_x + vectors_pca_trajectories_mean_over_structure[i][0, timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[i][1, timepoint]), color=colors[i])
        axarr[i].legend()
        axarr[i].set_xlabel('PC1', fontsize=16)
        axarr[i].set_ylabel('PC2', fontsize=16)

    # Loop over all possible pairs of structures and compare each pair of structures on the same plot
    structure_tuples = list(itertools.combinations(range(len(IX_structures)), 2)) # n over 2 pairs.
    fig_tuples, axarr = plt.subplots(1, len(structure_tuples), figsize=(20, 10))
    for sub_plot, structure_tuple in enumerate(structure_tuples):
        for i in structure_tuple: # Loop over all structures in tuple
            axarr[sub_plot].scatter(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :], label=labels[i], color=colors[i])
            axarr[sub_plot].errorbar(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :],
                              xerr=vectors_pca_trajectories_std_structure[i][0, :],
                              yerr=vectors_pca_trajectories_std_structure[i][1, :],
                              color=colors[i])
            # Annotate numbers of timepoints
            delta_x = 0.03
            for timepoint in range(8):
                axarr[sub_plot].annotate(str(timepoint + 1), xy=(delta_x + vectors_pca_trajectories_mean_over_structure[i][0, timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[i][1, timepoint]), color=colors[i])

        axarr[sub_plot].legend()
        axarr[sub_plot].set_xlabel('PC1', fontsize=16)
        axarr[sub_plot].set_ylabel('PC2', fontsize=16)

    return fig, fig_tuples