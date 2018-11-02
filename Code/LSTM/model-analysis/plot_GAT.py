import pickle
import matplotlib.pyplot as plt
import numpy as np

sentence = ['The', 'athletes', 'behind', 'the', 'table', 'observe(s)']
path2savefig = '../../../Figures/GAT1d_cell_nounpp_SR_LR_single_unit.png'
# Load GAT results
path2pkl = '../../../Figures/GAT1d_cell_nounpp_SR_LR.pkl'
# path2pkl = '../../../Figures/GAT1d_hidden_nounpp_SR_LR.pkl'
results = pickle.load(open(path2pkl, 'rb'))

fig1, ax1 = plt.subplots(1)
# # Plot full model and 2nd layer
# for model_name in ['scores_full_model']: #['scores_full_model', 'scores_2nd_layer']:
#     label=' '.join(model_name[7:].capitalize().split('_'))
#     curr_data = results[model_name]
#     ax1.errorbar(x=range(curr_data.shape[0]-2), y=curr_data[:-2], linewidth=2, label=label, color='k')
#

# LG number units
LR_number_units = results['LG_units']
colors = ['b', 'r']
line_styles = [':', '--']
LR_units = []
for u, LR_unit in enumerate(LR_number_units):
    unit, curr_data = LR_unit
    LR_units.append(unit)
    curr_data = curr_data[:-2]
    label = 'Unit ' + str(unit+1) + ' (LR)'
    ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=6, label=label, color=colors[u], ls=line_styles[u])

# SR number units
SR_units = [847, 629, 497, 1123, 92, 1042] # Number taken from weights of the SVM of the full-model
SR_number_units = []
for SR_unit in SR_units:
    SR_number_units += [(SR_unit, results['scores_all_single_units'][SR_unit, :])]
for u, SR_unit in enumerate(SR_number_units):
    unit, curr_data = SR_unit
    curr_data = curr_data[:-2]
    label = 'Unit ' + str(unit + 1) + ' (SR)'
    color = np.random.rand(1,3).tolist()[0]
    # ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=1, label=label, color='c', ls='--')

SR_units_AUC_based = [[],[],[]]
LR_units_AUC_based = []
mean_AUC = np.mean(results['scores_all_single_units'], axis=0)
std_AUC = np.std(results['scores_all_single_units'], axis=0)
percentile_AUC_SR = np.percentile(results['scores_all_single_units'], 95, axis=0)
percentile_AUC_LR = np.percentile(results['scores_all_single_units'], 95, axis=0)
thresh_AUC = mean_AUC + 3*std_AUC
for u in range(results['scores_all_single_units'].shape[0]):
    curr_AUC_vec = results['scores_all_single_units'][u, :]
    cnt = -1
    # Enables to set a different thresh for the subject position then the one used for the following time steps
    # if curr_AUC_vec[1]>percentile_AUC[1]:
    #     cnt += 1
    if curr_AUC_vec[4] < np.percentile(results['scores_all_single_units'], 5, axis=0)[4]:
        for pos in range(1, 4):
            is_SR_pos = curr_AUC_vec[pos]>percentile_AUC_SR[pos]
            if is_SR_pos:
                cnt += 1
            else:
                break
        if cnt > -1: SR_units_AUC_based[cnt].append((u, curr_AUC_vec))
    else:
        is_LR = True
        for pos in range(1, 5):
            if curr_AUC_vec[pos]<percentile_AUC_LR[pos]: is_LR = False
        if is_LR: LR_units_AUC_based.append((u, curr_AUC_vec))


for u, LR_unit in enumerate(LR_units_AUC_based):
    unit, curr_data = LR_unit
    curr_data = curr_data[:-2]
    label = 'Unit ' + str(unit + 1) + ' (LR)'
    color = np.random.rand(1,3).tolist()[0]
    if unit not in [775, 987]:
        ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=1, label=label, color='c', ls='--')
print('LR based on AUC:')
print([u for (u, _) in LR_units_AUC_based])

colors = ['y', 'm']
for pos, SR_pos in enumerate(SR_units_AUC_based[1::]):
    print('position: ' + str(pos+1))
    print([u for (u, vec) in SR_pos])
    for u, SR_unit in enumerate(SR_pos):
        unit, curr_data = SR_unit
        curr_data = curr_data[:-2]
        label = 'Unit ' + str(unit + 1) + ' (SR ' + str(pos+1) + ')'
        color = np.random.rand(1,3).tolist()[0]
        if unit not in [775, 987]:
            ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=1, label=label, color=colors[pos], ls='--')



# Plot number units and average across number units
non_number_units = list(set(range(1300)) - set(LR_units) - set(SR_units))
curr_data = results['scores_all_single_units'][non_number_units, :-2]
ax1.errorbar(x=range(curr_data.shape[1]), y=np.mean(curr_data, axis=0), yerr=np.std(curr_data, axis=0), linewidth=2, label='Other units', color='k')


# for u in range(1300):
#     curr_data = results['scores_all_single_units'][u, :-2]
#     ax1.errorbar(x=range(curr_data.size), y=curr_data, linewidth=0.05, color='c')


#### Cosmetics and save figures
fig1.subplots_adjust(right=0.6, bottom=0.25)
ax1.axhline(0.5, color='k', ls = '--')
ax1.axvline(4, color='r', ls = '-.')
ax1.set_xticklabels(sentence, rotation=90, fontsize=18)
ax1.set_ylabel('AUC', fontsize = 18)
ax1.set_title('Training time: subject ("athletes")', fontsize=16)
ax1.set_ylim((0, 1.05))
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
fig1.savefig(path2savefig)