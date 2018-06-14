import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from os import path as op

def get_stimuli_and_info(settings, params):
    if settings.stimuli_type == 'MEG_stimuli':
        # load rejected trials
        bad_trials = np.load(settings.bad_trials_file_name)

        # Load stimuli
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block2_300ms/stimuli.p'), 'rb')
        run1 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block6_300ms/stimuli.p'), 'rb')
        run2 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block0_300ms/stimuli.p'), 'rb')
        run3 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block2_300ms/stimuli.p'), 'rb')
        run4 = pickle.load(f)
        all_stim = run1 + run2 + run3 + run4 # concatenate all
        all_stim_clean = [i for j, i in enumerate(all_stim) if j not in bad_trials] # All stimuli without rejected trials

        # Load stimuli info
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block2_300ms/info_stim.p'), 'rb')
        info1 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim/block6_300ms/info_stim.p'), 'rb')
        info2 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block0_300ms/info_stim.p'), 'rb')
        info3 = pickle.load(f)
        f = open(os.path.join(settings.path2stimuli_parent, 'Stim2/block2_300ms/info_stim.p'), 'rb')
        info4 = pickle.load(f)
        all_info = info1 + info2 + info3 + info4 # concatenate all
        all_info_clean = [i for j, i in enumerate(all_info) if j not in bad_trials] # All stimuli info without rejected trials

        IX = [i for i in range(len(all_info_clean)) if all_info_clean[i]['anomaly']=='correct']
        all_info_correct=[i for j,i in enumerate(all_info_clean) if j in IX]

        # Split according to structures (structure = 1 is 4x4; 2 is 2x6; 3 is 6x2)
        IX_structures = []
        for i in range(3):
            IX_structures.append([i for i in range(len(all_info_correct)) if all_info_correct[i]['structure']==i+1])

        labels = ['2-6', '4-4', '6-2']
        colors = ['r', 'g', 'b']

    elif settings.stimuli_type == 'NP_VP_transition':
        with open(os.path.join(settings.path2stimuli, settings.stimuli_file_name), 'r') as f:
            stimuli = f.readlines()
        info =  pickle.load(open(os.path.join(settings.path2stimuli, settings.stimuli_meta_data), 'rb'))

        NP_endings = ['noun', 'adj', 'pronoun', 'proper_noun']
        VP_beginings = ['aux', 'verb', 'pronoun', 'negation']
        IX_structures = []
        labels = []
        colors = []
        for e, ending in enumerate(NP_endings):
            for b, beginning in enumerate(VP_beginings):
                for NP_length in range(1,13,1):
                    for VP_length in range(1, 13, 1):
                        curr_IX = [i for i, d in enumerate(info) if info[i]['NP_ends_with'] == ending and info[i]['VP_begins_with'] == beginning and info[i]['NP_length'] == NP_length and info[i]['VP_length'] == VP_length]
                        if curr_IX:
                            IX_structures.append(curr_IX)
                            curr_label = ending + '_' + beginning + '_NP_' + str(NP_length) + '_VP_' + str(VP_length)
                            labels.append(curr_label)
                            colors.append((e/len(NP_endings), b/len(VP_beginings) ,NP_length/13))

        all_stim_clean = stimuli
        all_info_clean = info
        all_info_correct = info

    elif settings.stimuli_type == 'Relative_clauses':
        with open(os.path.join(settings.path2stimuli, settings.stimuli_file_name), 'r') as f:
            stimuli = f.readlines()
        info =  pickle.load(open(os.path.join(settings.path2stimuli, settings.stimuli_meta_data), 'rb'))


        relevant_keys = ['NP_ends_with', 'relative_clause', 'NP_length', 'VP_length', 'relative_clause_length']

        d = {}
        for k in relevant_keys:
            for s in range(len(info)):
                if k not in d.keys():
                    d[k] = []
                d[k].append(info[s][k])
            d[k] = set(d[k])

        IX_structures = []
        labels = []
        colors = []

        for ending in d['NP_ends_with']:
            for rc in d['relative_clause']:
                for NP_length in d['NP_length']:
                    for VP_length in d['VP_length']:
                        for RC_length in d['relative_clause_length']:
                            curr_IX = [i for i, curr_info in enumerate(info)
                                       if curr_info['NP_ends_with'] == ending
                                       and curr_info['relative_clause'] == rc
                                       and curr_info['NP_length'] == NP_length
                                       and curr_info['VP_length'] == VP_length
                                       and curr_info['relative_clause_length'] == RC_length]
                            if curr_IX:
                                IX_structures.append(curr_IX)
                                if rc is None: rc = 'none'
                                curr_label = ending + '_' + rc + '_NP_' + str(NP_length) + '_RC_' + str(RC_length) + '_VP_' + str(VP_length)
                                labels.append(curr_label)

                                # colors.append((e/len(NP_endings), b/len(VP_beginings) ,NP_length/13))
                            curr_IX = []

        all_stim_clean = stimuli
        all_info_clean = info
        all_info_correct = info

    return all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors


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

def plot_PCA_trajectories(vector_type, data, all_stim_clean, IX_structures, labels, colors, settings, params):
    # input:
    # data (ndarray): num_trails X num_features X num_timepoints
    # Return:
    # fig - figure handle to subplots for each syntactic structure
    # fig_tuple - figure handle to subplots for each pair of syntactic structures compared on the same plot
    from sklearn import decomposition
    from sklearn import preprocessing
    import itertools
    import pickle
    from tqdm import tqdm

    num_trials = len(data)
    num_dim = data[0].shape[0] # Extract dimension from first trial
    num_structures = len(IX_structures)

    # Reshape: concatenate all timepoints before PCAing (num_trials*num_timepoints X num_features)
    vectors = np.empty((0, num_dim))
    # for timepoint in range(8):
    #     vectors = np.vstack((vectors, data[:, :, timepoint]))
    print('Prepare data for PCA: breaking down sentences into words')
    for trial_data in tqdm(data):
        for timepoint in range(trial_data.shape[1]):
            vectors = np.vstack((vectors, trial_data[:, timepoint]))


    print('Prepare data for PCA: standardize data')
    standardized_scale = preprocessing.StandardScaler().fit(vectors)
    vectors_standardized = standardized_scale.transform(vectors)

    print('Run PCA')
    pca = decomposition.PCA(n_components=2)
    pca.fit(vectors_standardized)
    vectors_PCA_projected = pca.transform(vectors_standardized)

    print('After PCA: reshape back into num_trials X num_PCs X num_timepoints as vector_PCA_trajectories')
    vector_PCA_trajectories = []
    st = 0
    for trial, trial_data in enumerate(tqdm(data)):
        curr_sentence_data = []
        for timepoint in range(trial_data.shape[1]):
            curr_sentence_data.append(vectors_PCA_projected[st, :])
            st += 1
        vector_PCA_trajectories.append(np.asarray(curr_sentence_data).transpose())

    file_name = 'PCA_LSTM_' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2figures, 'units_activation', file_name), 'wb') as f:
        pickle.dump([pca, vectors_PCA_projected], f)
    # with open(op.join(settings.path2figures, 'units_activation', file_name), 'rb') as f:
    #     data_saved = pickle.load(f)
    #     pca, vectors_PCA_projected = data_saved[0], data_saved[1]

    print('After PCA: average across each syntactic structure type')
    vectors_pca_trajectories_mean_over_structure = []; vectors_pca_trajectories_std_structure = []
    for i, IX_structure in enumerate(IX_structures):
        vectors_of_curr_structure = [vec for ind, vec in enumerate(vector_PCA_trajectories) if ind in IX_structure]
        vectors_pca_trajectories_mean_over_structure.append(np.mean(np.asarray(vectors_of_curr_structure), axis=0))
        vectors_pca_trajectories_std_structure.append(np.std(np.asarray(vectors_of_curr_structure), axis=0))

    # Plot averaged trajectories for all structures
    for i in range(num_structures):
        if IX_structures[i]:
            print(i, labels[i])
            curr_stimuli = [stim for ind, stim in enumerate(all_stim_clean) if ind in IX_structures[i]]
            fig, axarr = plt.subplots(figsize=(20, 10))
            axarr.scatter(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :], label=labels[i])
            axarr.errorbar(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :],
                              xerr=vectors_pca_trajectories_std_structure[i][0, :],
                              yerr=vectors_pca_trajectories_std_structure[i][1, :])

            # Annotate with number the subsequent time points on the trajectories
            delta_x = 0.03 # Shift the annotation of the time point by a small step
            for timepoint in range(vectors_pca_trajectories_mean_over_structure[i].shape[1]):
                axarr.annotate(str(timepoint + 1) + ' ' + str(curr_stimuli[0]).split(' ')[timepoint], xy=(delta_x + vectors_pca_trajectories_mean_over_structure[i][0, timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[i][1, timepoint]), fontsize=16)

            axarr.legend()
            axarr.set_xlabel('PC1', fontsize=16)
            axarr.set_ylabel('PC2', fontsize=16)
            axarr.set_title('num of sentences = ' + str(len(curr_stimuli)), fontsize=16)

            file_name = 'PCA_LSTM_' + vector_type + '_' + labels[i] + '_' + settings.stimuli_file_name + '.png'
            plt.figure(fig.number)
            plt.savefig(op.join(settings.path2figures, 'units_activation', file_name))

    # fig, axarr = plt.subplots(1, num_structures, figsize=(20, 10))
    # for i in range(num_structures):
    #     axarr[i].scatter(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :], label=labels[i], color=colors[i])
    #     axarr[i].errorbar(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :],
    #                       xerr=vectors_pca_trajectories_std_structure[i][0, :],
    #                       yerr=vectors_pca_trajectories_std_structure[i][1, :],
    #                       color=colors[i])
    #
    #     # Annotate with number the subsequent time points on the trajectories
    #     delta_x = 0.03 # Shift the annotation of the time point by a small step
    #     for timepoint in range(8):
    #         axarr[i].annotate(str(timepoint + 1), xy=(delta_x + vectors_pca_trajectories_mean_over_structure[i][0, timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[i][1, timepoint]), color=colors[i])
    #     axarr[i].legend()
    #     axarr[i].set_xlabel('PC1', fontsize=16)
    #     axarr[i].set_ylabel('PC2', fontsize=16)
    #
    # # Loop over all possible pairs of structures and compare each pair of structures on the same plot
    # structure_tuples = list(itertools.combinations(range(len(IX_structures)), 2)) # n over 2 pairs.
    # fig_tuples, axarr = plt.subplots(1, len(structure_tuples), figsize=(20, 10))
    # for sub_plot, structure_tuple in enumerate(structure_tuples):
    #     for i in structure_tuple: # Loop over all structures in tuple
    #         axarr[sub_plot].scatter(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :], label=labels[i], color=colors[i])
    #         axarr[sub_plot].errorbar(vectors_pca_trajectories_mean_over_structure[i][0, :], vectors_pca_trajectories_mean_over_structure[i][1, :],
    #                           xerr=vectors_pca_trajectories_std_structure[i][0, :],
    #                           yerr=vectors_pca_trajectories_std_structure[i][1, :],
    #                           color=colors[i])
    #         # Annotate numbers of timepoints
    #         delta_x = 0.03
    #         for timepoint in range(8):
    #             axarr[sub_plot].annotate(str(timepoint + 1), xy=(delta_x + vectors_pca_trajectories_mean_over_structure[i][0, timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[i][1, timepoint]), color=colors[i])
    #
    #     axarr[sub_plot].legend()
    #     axarr[sub_plot].set_xlabel('PC1', fontsize=16)
    #     axarr[sub_plot].set_ylabel('PC2', fontsize=16)
    #
    # return fig, fig_tuples
    pass