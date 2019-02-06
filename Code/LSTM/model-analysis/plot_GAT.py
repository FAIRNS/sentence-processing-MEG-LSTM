import pickle, sys, os
import matplotlib.pyplot as plt
import numpy as np
import torch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/word_language_model')))
import data


sentence = ['The', 'boy', 'near', 'the', 'cars', 'greets']
path2savefig = '../../../Figures/GAT1d_cell_nounpp_SR_LR_single_unit.png'
# Load GAT results
path2pkl = '../../../Output/GAT1d_cell_Ou.pkl'
# path2pkl = '../../../Figures/GAT1d_hidden_nounpp_SR_LR.pkl'
results = pickle.load(open(path2pkl, 'rb'))

# parser.add_argument('-model', type=str, help='Meta file stored once finished training the corpus')
# parser.add_argument('-v', '--vocabulary', default='../../../Data/LSTM/english_vocab.txt')
model = '../../../Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
vocabulary = '../../../Data/LSTM/english_vocab.txt'
input = '../../../Data/Stimuli/singular_plural_verbs.txt'



def get_SNRs(model, vocabulary):
    '''

    :param model: path to LSTM model
    :param vocabulary:  path to vocab used for training the model
    :return: SNRs: list (#units in 2nd layer) of SNR values between weights (singular/plural).
    '''
    print('Loading models...')
    print('\nmodel: ' + model + '\n')
    model = torch.load(model)
    model.rnn.flatten_parameters()
    embeddings_out = model.decoder.weight.data.numpy()
    vocab = data.Dictionary(vocabulary)

    # Read list of contrasted words (e.g., singular vs. plural verbs).
    with open(input, 'r') as f:
        lines = f.readlines()
    verbs_singular = [l.split('\t')[0].strip() for l in lines]
    verbs_plural = [l.split('\t')[1].strip() for l in lines]
    verbs_all = verbs_singular + verbs_plural
    print('\nVerbs used:')
    print(verbs_all)

    # Get index in the vocab for all words and extract embeddings
    idx_verbs_singular = [vocab.word2idx[w] for w in verbs_singular]
    idx_verbs_plural = [vocab.word2idx[w] for w in verbs_plural]

    # Calc SNR
    SNRs = []
    for from_unit in range(650):
        output_weights_singular = embeddings_out[idx_verbs_singular, from_unit]
        output_weights_plural = embeddings_out[idx_verbs_plural, from_unit]
        SNR = np.abs(np.mean(output_weights_singular) - np.mean(output_weights_plural)) / (
                    np.std(output_weights_singular) + np.std(output_weights_plural))
        SNRs.append(SNR)
    print('SNR Percentile 95: %1.2f' % np.percentile(SNRs, 95))

    return SNRs


def get_SR_LR_AUC_based_units(results):
    SR_units_AUC_based = [[], [], []]
    LR_units_AUC_based = []
    percentile_AUC = np.percentile(results['scores_all_single_units'], 95, axis=0)
    for u in range(results['scores_all_single_units'].shape[0]):
        curr_AUC_vec = results['scores_all_single_units'][u, :]
        cnt = -1
        for pos in range(1, 5):
            has_high_AUC = curr_AUC_vec[pos] > 0.9 # percentile_AUC[pos]
            is_in_2nd_layer = u >= 650
            has_high_SNR = SNRs[u - 650] > np.percentile(SNRs, 95)
            if is_in_2nd_layer and has_high_AUC and has_high_SNR:
                cnt += 1
            else:
                break
        if cnt > -1:  # is a number unit
            if cnt < 3:  # is a short-range unit
                SR_units_AUC_based[cnt].append((u, curr_AUC_vec))
            else:  # maybe a long-range unit
                LR_units_AUC_based.append((u, curr_AUC_vec))
    return SR_units_AUC_based, LR_units_AUC_based


def get_SR_LR_weights_based(results):
    # LG number units
    LR_number_units = results['LG_units']
    SR_units = [847, 629, 497, 1123, 92, 1042] # Number taken from weights of the SVM of the full-model
    SR_number_units = []
    for SR_unit in SR_units:
        SR_number_units += [(SR_unit, results['scores_all_single_units'][SR_unit, :])]
    return SR_number_units, LR_number_units


# Get signal-to-noise of weights
SNRs = get_SNRs(model, vocabulary)
# Get units suggested from weights of a SVM classifier
SR_units_weights_based, LR_units_weights_based = get_SR_LR_weights_based(results)
# Get units based by GAT
SR_units_AUC_based, LR_units_AUC_based = get_SR_LR_AUC_based_units(results)

# Plot results
fig1, ax1 = plt.subplots(figsize=(10, 10))
colors = ['b', 'r']
line_styles = [':', '--']
# colors += colors; line_styles += line_styles
LR_units = []
for u, LR_unit in enumerate(LR_units_weights_based):
    unit, curr_data = LR_unit
    LR_units.append(unit)
    curr_data = curr_data[:-2]
    label = 'Unit ' + str(unit+1) + ' (LR)'
    ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=6, label=label, color=colors[u], ls=line_styles[u])

#for u, LR_unit in enumerate(LR_units_AUC_based):
#    unit, curr_data = LR_unit
#    curr_data = curr_data[:-2]
#    label = 'Unit ' + str(unit + 1) + ' (LR)'
#    color = np.random.rand(1,3).tolist()[0]
#    if unit not in [775, 987]:
#        ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=1, label=label, color='c', ls='--')
#print('LR based on AUC:')
#print([u for (u, _) in LR_units_AUC_based])


#colors = ['y', '#d3d3d3', 'm', 'c']
#for pos, SR_pos in enumerate(SR_units_AUC_based):
#    print('position: ' + str(pos))
#    print([u for (u, vec) in SR_pos])
#    for u, SR_unit in enumerate(SR_pos):
#        unit, curr_data = SR_unit
#        curr_data = curr_data[:-2]
#        label = 'Unit ' + str(unit + 1) + ' (SR ' + str(pos) + ')'
#        color = np.random.rand(1,3).tolist()[0]
#        if unit not in [775, 987]:
#            ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=2, label=label, color=colors[pos], ls='--')



# Plot full model
ax1.plot(range(results['scores_full_model'].shape[0]), results['scores_full_model'], linewidth=2, label='Full-model minus LR-units', color='k')

# Plot number units and average across number units
all_SR_units = [tuple[0] for sublist in SR_units_AUC_based for tuple in sublist]
all_LR_units = [tuple[0] for tuple in LR_units_AUC_based]
non_number_units = list(set(range(1300)) - set(all_LR_units) - set(all_SR_units))
curr_data = results['scores_all_single_units'][non_number_units, :-2]
#ax1.errorbar(x=range(curr_data.shape[1]), y=np.mean(curr_data, axis=0), yerr=np.std(curr_data, axis=0), lw=2, ls=':', label='non-number units', color='k')



#### Cosmetics and save figures
# fig1.subplots_adjust(right=0.75)
ax1.set_xlim((0, len(sentence)-1))
ax1.axhline(0.5, color='k', ls = '--')
# ax1.axvline(4, color='r', ls = '-.')
ax1.set_xticklabels(sentence, fontsize=30)
ax1.tick_params(axis='x', which='major', pad=15)
ax1.set_ylabel('AUC', fontsize = 30)
ax1.set_yticks([0, 0.5, 1])
ax1.set_yticklabels([0, 0.5, 1], fontsize=30)
# ax1.set_title('Training time: subject ("athletes")', fontsize=16)
ax1.set_ylim((0, 1.05))
# ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
handles, labels = ax1.get_legend_handles_labels()
a, b = labels.index('Full-model minus LR-units'), labels.index('Unit 988 (LR)')
labels[b], labels[a] = labels[a], labels[b]
handles[b], handles[a] = handles[a], handles[b]
# ax1.legend(handles, labels, loc='upper center', ncol=1, fontsize=25, bbox_to_anchor=(0., 1.02, 1., .102))
ax1.legend(handles, labels, loc=3, fontsize=20)#, bbox_to_anchor=(1.05, 1))
plt.show()
fig1.savefig(path2savefig, dpi=100)
