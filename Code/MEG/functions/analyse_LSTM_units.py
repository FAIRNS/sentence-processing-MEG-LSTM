import os
import numpy as np
import pickle
import codecs
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os import path as op
import itertools

def get_stimuli_and_info(settings, params, relevant_keys):
    '''

    :param settings.stimuli_type ('MEG_stimuli'/'NP_VP_transition'/'Relative_clauses'): which stimuli to load
    :param params:
    relevant_keys: (list of string) Split analyses according to which keys (e.g., 'RC_type', 'sentence_length', 'number_1', 'number_2', 'success')
    :return:
    '''
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
        #print([i for i, inf in enumerate(info) if 'relative_claue' not in inf.keys()])
        print('RC types in the stimuli: ' + ', '.join(set([d['RC_type'] for d in info])))

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

    elif settings.stimuli_type == 'from_marco_script':
        print('Stimuli: English synthetic dataset with RC')
        #print('Loading info file: ' + os.path.join(settings.path2stimuli, settings.stimuli_file_name))
        with open(os.path.join(settings.path2stimuli, settings.stimuli_file_name), 'r') as f:
            stimuli = f.readlines()
        info =  pickle.load(open(os.path.join(settings.path2stimuli, settings.stimuli_meta_data), 'rb'))

        #relevant_keys = ['RC_type', 'sentence_length', 'number_1', 'number_2', 'success']
        list_values = []
        d = {} # dict containing all possible values of each relevant key
        for k in relevant_keys:
            for s in range(len(info)):
                if k not in d.keys():
                    d[k] = []
                d[k].append(info[s][k])
            d[k] = set(d[k])
            list_values.append(list(d[k]))
        
        # Separate the stimuli according to all possible comibination of values in relevant keys
        IX_structures = []
        labels = []
        colors = []
        
        for tuple_values in itertools.product(*list_values):
            print(tuple_values)
            curr_IX = []
            for i, curr_info in enumerate(info):
                check_if_all_vals_in_curr_info_match_curr_tuple = True
                for j, key in enumerate(relevant_keys):
                    if curr_info[key] != tuple_values[j]:
                        check_if_all_vals_in_curr_info_match_curr_tuple = False
                if check_if_all_vals_in_curr_info_match_curr_tuple:
                    curr_IX.append(i)
            if curr_IX: # Check if not an empty set
                IX_structures.append(curr_IX)
                curr_label = "_".join(map(str, tuple_values))
                labels.append(curr_label)

        all_stim_clean = stimuli
        all_info_clean = info
        all_info_correct = info

    return all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors


def plot_units_activation(LSTM_data, label, curr_stimuli, units, settings, params):
    from tqdm import tqdm
    if not units:
        units = range(LSTM_data['gates.in'][0].shape[0])
    for unit in tqdm(units):
        #print('Unit ' + str(unit))
        # Hidden units
        mean_h_activity_structure = np.mean(np.vstack([LSTM_data['hidden'][i][unit, :] for i in range(len(LSTM_data['hidden']))]), axis=0)
        mean_c_activity_structure = np.mean(np.vstack([LSTM_data['cell'][i][unit, :] for i in range(len(LSTM_data['cell']))]), axis=0)

        std_h_activity_structure = np.std(np.vstack([LSTM_data['hidden'][i][unit, :] for i in range(len(LSTM_data['hidden']))]), axis=0)
        std_c_activity_structure = np.std(np.vstack([LSTM_data['cell'][i][unit, :] for i in range(len(LSTM_data['cell']))]), axis=0)

        mean_gates_structure = {}
        std_gates_structure = {}
        for gate in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']:  # Loop over gates and c_tilda:
            mean_gates_structure[gate] = np.mean(np.vstack([LSTM_data[gate][i][unit, :] for i in range(len(LSTM_data[gate]))]), axis=0)
            std_gates_structure[gate] = np.std(np.vstack([LSTM_data[gate][i][unit, :] for i in range(len(LSTM_data[gate]))]), axis=0)

        # Plot
        fig, ax = plt.subplots(1, 2, figsize=(30,20))
        ###num_words_in_curr_structure = mean_h_activity_structure.shape[2]
        ax[0].errorbar(range(1, mean_h_activity_structure.shape[0]+1), mean_h_activity_structure, yerr=std_h_activity_structure, label = 'hidden', linewidth=3)
        ax[0].errorbar(range(1, mean_c_activity_structure.shape[0]+1), mean_c_activity_structure, yerr=std_c_activity_structure, label = 'cell', linewidth=3)
        ax[0].errorbar(range(1, mean_gates_structure['gates.c_tilde'].shape[0]+1), mean_gates_structure['gates.c_tilde'], yerr=std_gates_structure['gates.c_tilde'], label = 'gates.c_tilde', linewidth=3)
        ax[0].set_ylabel('Activation', fontsize =26)
        ax[0].set_xticks(range(1, mean_gates_structure['gates.c_tilde'].shape[0]+1))
        ax[0].set_xticklabels(curr_stimuli[0].split(' '), rotation='vertical', fontsize=22)
        #ax.set_xlim(0, 9)
        #ax[0].set_ylim(-1.1, 1.1)
        ax[0].legend(loc=(1.04,1), fontsize=20)

        for gate in ['gates.in', 'gates.forget', 'gates.out']:
            ax[1].errorbar(range(1, mean_gates_structure[gate].shape[0]+1), mean_gates_structure[gate], yerr=std_gates_structure[gate], label = gate, linewidth=3)
        ax[1].set_ylabel('Activation', fontsize =26)
        #ax.set_xlim(0, mean_h_activity_structure.shape[0])
        #ax[1].set_ylim(-0.1, 1.1)
        ax[1].legend(loc=(1.04,1), fontsize=20)
        ax[1].set_xticks(range(1, mean_gates_structure['gates.c_tilde'].shape[0]+1))
        ax[1].set_xticklabels(curr_stimuli[0].split(' '), rotation='vertical', fontsize=22)

        file_name = 'units_activation_unit_' + str(unit) + label
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.svg'))
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.png'))
        plt.close(fig)


        fig, ax = plt.subplots(figsize=(24, 16))
        mean_i_c_tilde_activity_structure = np.mean(np.multiply(np.vstack([LSTM_data['gates.in'][i][unit, :] for i in range(len(LSTM_data['gates.in']))]),np.vstack([LSTM_data['gates.c_tilde'][i][unit, :] for i in range(len(LSTM_data['gates.c_tilde']))])), axis=0)
        std_i_c_tilde_activity_structure = np.mean(np.multiply(np.vstack([LSTM_data['gates.in'][i][unit, :] for i in range(len(LSTM_data['gates.in']))]),np.vstack([LSTM_data['gates.c_tilde'][i][unit, :] for i in range(len(LSTM_data['gates.c_tilde']))])), axis=0)
        fig.subplots_adjust(bottom=0.25)
        
        ax.errorbar(range(1, mean_i_c_tilde_activity_structure.shape[0]+1), mean_i_c_tilde_activity_structure, yerr=std_i_c_tilde_activity_structure, label = '$i_t \\tilde{C}_t$', linewidth=5, ls='--')
        ax.errorbar(range(1, mean_gates_structure['gates.forget'].shape[0]+1), mean_gates_structure['gates.forget'], yerr=std_gates_structure['gates.forget'], label = '$f_t$', linewidth=5, ls='--')
        ax.set_ylabel('Activation', fontsize =26)
        ax.set_xticks(range(1, mean_gates_structure['gates.forget'].shape[0]+1))
        ax.set_xticklabels(curr_stimuli[0].split(' '), rotation='vertical')
        #ax.set_xlim(0, 9)
        #ax.set_ylim(-1.1, 1.1)
        ax.tick_params(labelsize=30)
        ax.legend(fontsize=24, numpoints=1, loc=(1, 0.5), framealpha=0)
        file_name = 'units_forget_activation_unit_' + str(unit) + label
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.svg'))
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.png'))
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(24, 16))
        ax.errorbar(range(1, mean_h_activity_structure.shape[0]+1), mean_h_activity_structure, yerr=std_h_activity_structure, label = '$h_t$', linewidth=5, ls='--')
        ax.errorbar(range(1, mean_c_activity_structure.shape[0]+1), mean_c_activity_structure, yerr=std_c_activity_structure, label = '$C_t$', linewidth=5, ls='--')
        ax.set_ylabel('Activation', fontsize =26)
        #ax.set_xlim(0, mean_h_activity_structure.shape[0])
        #ax.set_ylim(-1.1, 1.1)
        ax.set_xticks(range(1, mean_h_activity_structure.shape[0]+1))
        ax.set_xticklabels(curr_stimuli[0].split(' '), rotation='vertical')
        ax.legend(fontsize=24, numpoints=1, loc=(1, 0.5), framealpha=0)
        ax.tick_params(labelsize=30)
        fig.subplots_adjust(bottom=0.25)

        file_name = 'units_h_c_activation_unit_' + str(unit) + label
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name +'.svg'))
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name +'.png'))
        plt.close(fig)

        
        fig, ax = plt.subplots(figsize=(24, 16))
        ax.errorbar(range(1, mean_gates_structure['gates.in'].shape[0]+1), mean_gates_structure['gates.in'], yerr=std_gates_structure['gates.in'], label = '$i_t$', linewidth=5, ls='--')
        ax.errorbar(range(1, mean_i_c_tilde_activity_structure.shape[0]+1), mean_i_c_tilde_activity_structure, yerr=std_i_c_tilde_activity_structure, label = '$i_t \\tilde{C}_t$', linewidth=5, ls='--')
        ax.errorbar(range(1, mean_gates_structure['gates.forget'].shape[0]+1), mean_gates_structure['gates.forget'], yerr=std_gates_structure['gates.forget'], label = '$f_t$', linewidth=5, ls='--')
        ax.errorbar(range(1, mean_h_activity_structure.shape[0]+1), mean_h_activity_structure, yerr=std_h_activity_structure, label = '$h_t$', linewidth=5)
        ax.errorbar(range(1, mean_c_activity_structure.shape[0]+1), mean_c_activity_structure, yerr=std_c_activity_structure, label = '$C_t$', linewidth=5)
        ax.set_ylabel('Activation', fontsize =26)
        ax.set_xticks(range(1, mean_h_activity_structure.shape[0]+1))
        ax.set_xticklabels(curr_stimuli[0].split(' '), rotation='vertical')
        ax.legend(fontsize=24, numpoints=1, loc=(1, 0.5), framealpha=0)
        ax.tick_params(labelsize=30)
        fig.subplots_adjust(bottom=0.25)

        file_name = 'units_h_c_forget_activation_unit_' + str(unit) + label
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.svg'))
        plt.savefig(op.join(settings.path2figures, 'units_activation', file_name + '.png'))
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
    print('Prepare data for PCA: breaking down sentences into words')
    vectors = np.vstack([trial_data.T for trial_data in tqdm(data)])

    print('Prepare data for PCA: standardize data')
    standardized_scale = preprocessing.StandardScaler().fit(vectors)
    vectors_standardized = standardized_scale.transform(vectors)

    print('Run PCA')
    n_components = 5
    pca = decomposition.PCA(n_components=n_components)
    pca.fit(vectors_standardized)
    print(pca.explained_variance_ )
    print(pca.explained_variance_ratio_)
    print(pca.explained_variance_ratio_.cumsum())
    vectors_PCA_projected = pca.transform(vectors_standardized)

    file_name = 'PCA_LSTM_' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2figures, 'units_activation', file_name), 'wb') as f:
        pickle.dump(pca, f)

    file_name = 'PCA_LSTM_projections_' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2figures, 'units_activation', file_name), 'wb') as f:
        pickle.dump(vectors_PCA_projected, f)
    vector_PCA_trajectories = []
    st = 0
    for trial, trial_data in enumerate(tqdm(data)):
        curr_sentence_data = []
        for timepoint in range(trial_data.shape[1]):
            curr_sentence_data.append(vectors_PCA_projected[st, :])
            st += 1
        vector_PCA_trajectories.append(np.asarray(curr_sentence_data).transpose())

    file_name = 'PCA_LSTM_' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2output, 'PCA', file_name), 'wb') as f:
        pickle.dump(pca, f)
    
    file_name = 'PCA_vectors_LSTM_' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2output, 'PCA', file_name), 'wb') as f:
        pickle.dump(vector_PCA_trajectories, f)

    file_name = 'PCA_LSTM_traject' + vector_type + settings.LSTM_file_name + '.pkl'
    with open(op.join(settings.path2output, 'PCA', file_name), 'wb') as f:
        pickle.dump(vector_PCA_trajectories, f)


    print('After PCA: average across each syntactic structure type')
    vectors_pca_trajectories_mean_over_structure = []; vectors_pca_trajectories_std_structure = []
    for i, IX_structure in enumerate(IX_structures):
        vectors_of_curr_structure = [vec for ind, vec in enumerate(vector_PCA_trajectories) if ind in IX_structure]
        #print(i, len(vectors_of_curr_structure ))
        vectors_pca_trajectories_mean_over_structure.append(np.mean(np.asarray(vectors_of_curr_structure), axis=0))
        vectors_pca_trajectories_std_structure.append(np.std(np.asarray(vectors_of_curr_structure), axis=0))

    # Plot averaged trajectories for all structures
    import itertools
    for PCs in itertools.combinations(range(n_components), 2):
        print(PCs)
        for i in tqdm(range(num_structures)):
            if IX_structures[i]:
                print(i, labels[i])
                curr_stimuli = [stim for ind, stim in enumerate(all_stim_clean) if ind in IX_structures[i]]
                generate_figure_for_PC_trajectory(PCs, pca.explained_variance_ratio_, curr_stimuli, vectors_pca_trajectories_mean_over_structure[i], vectors_pca_trajectories_std_structure[i], labels[i], vector_type, settings)


def generate_figure_for_PC_trajectory(PCs, explained_variance_ratio_, curr_stimuli, vectors_pca_trajectories_mean_over_structure, vectors_pca_trajectories_std_structure, labels, vector_type, settings):
    fig, axarr = plt.subplots(figsize=(20, 10))
    axarr.scatter(vectors_pca_trajectories_mean_over_structure[PCs[0], :], vectors_pca_trajectories_mean_over_structure[PCs[1], :], label=labels)
    axarr.errorbar(vectors_pca_trajectories_mean_over_structure[PCs[0], :], vectors_pca_trajectories_mean_over_structure[PCs[1], :],
		      xerr=vectors_pca_trajectories_std_structure[PCs[0], :],
		      yerr=vectors_pca_trajectories_std_structure[PCs[1], :], linewidth=5)

    # Annotate with number the subsequent time points on the trajectories
    delta_x = 0.03 # Shift the annotation of the time point by a small step
    #print(vectors_pca_trajectories_mean_over_structure[i].shape[1], str(curr_stimuli[0]).split(' '))
    for timepoint in range(vectors_pca_trajectories_mean_over_structure.shape[1]):
        axarr.annotate(str(timepoint + 1) + ' ' + str(curr_stimuli[0]).split(' ')[timepoint], xy=(delta_x + vectors_pca_trajectories_mean_over_structure[PCs[0], timepoint], delta_x + vectors_pca_trajectories_mean_over_structure[PCs[1], timepoint]), fontsize=30)

    axarr.legend()
    axarr.set_xlabel('PC %i %1.2f' % (PCs[0]+1, explained_variance_ratio_[PCs[0]]), fontsize=26)
    axarr.set_ylabel('PC %i %1.2f' % (PCs[1]+1, explained_variance_ratio_[PCs[1]]), fontsize=26)
    axarr.tick_params(labelsize=30)
    #ax.legend(framealpha=1)
    axarr.set_title(curr_stimuli[0] + '\nnum of sentences = ' + str(len(curr_stimuli)), fontsize=18)

    file_name = 'PCs' + str(PCs) +'_LSTM_' + vector_type + '_' + labels + '_' + settings.LSTM_file_name + settings.stimuli_file_name + '.svg'
    plt.figure(fig.number)
    plt.savefig(op.join(settings.path2figures, 'PCA', 'trajectories', file_name))
    plt.close(fig.number)
    

def draw_activations(gates, unit, unit_type, prefix='', ls='-', color=None, marker=None):
    if unit_type == 'gates.in*c_tilde':
        unit_activations=gates['gates.in']['plot'][:,unit,:] * gates['gates.c_tilde']['plot'][:,unit,:]
    else:
        unit_activations=gates[unit_type]['plot'][:,unit,:]
    plt.title(unit)
    draw_activation_series(unit_activations, unit_type, prefix, ls, color, marker)

def draw_activation_series(unit_activations, unit_type, prefix='', ls='-', color=None, marker=None):
    labels = [''] * plot_padding + ['head'] + ['+{}'.format(i) for i in range(1, plot_span//2+1)] + ['{}'.format(i) for i in range(-plot_span//2,0)] + ['target']
    x = np.arange(unit_activations.shape[1])
    plt.xticks(x, labels, rotation='vertical', fontsize=30)
    labels={'gates.in*c_tilde': "$i_t \\tilde{C}_t$",
           'cell': '$C$',
           'gates.forget': '$f_t$',
           'hidden': '$h_t$'}
    plt.errorbar(x=x, y=unit_activations.mean(0), yerr=unit_activations.std(0), lw=5, capsize=6, capthick=2, label=prefix+labels[unit_type], ls=ls, color=color, marker=marker)
    handles, labels = plt.gca().get_legend_handles_labels()
    # remove error bars from legend
    handles = [h[0] for h in handles]
    #plt.legend(handles, labels, fontsize=24, loc='upper right', numpoints=1, bbox_to_anchor=(1.1, 1.1), fancybox=True, framealpha=1)
    plt.yticks(fontsize=22)

    pass


