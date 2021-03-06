import matplotlib.pyplot as plt
import pickle
from matplotlib.legend import Legend
import seaborn as sns
import pandas as pd
import numpy as np
path2_fullmodel_results = '/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Pipeline/Italian_nounpp_results_19_models'
path2_fullmodel_results = '../../../Pipeline/Italian_nounpp_results_19_models'
path2_ablation_results = 'dict_ablation_results.pkl'


# scatter of full-model performance
with open(path2_fullmodel_results, 'r') as f:
    lines = f.readlines()

dict_results = {}
for l in lines:
    if l.startswith('Number-agreement'):
        curr_seed = int(l.split()[-1])
        dict_results[curr_seed] = {}
    if l.startswith('[['):
        fields = l.split("'")
        N1 = fields[3]
        N2 = fields[7]
        curr_cond = '%s%s' % (N1[0], N2[0])
    if l.startswith('0') or l.startswith('1'):
        dict_results[curr_seed][curr_cond] = float(l)

fig, ax = plt.subplots()
for s in dict_results.keys():
    sp = dict_results[s]['sp']
    ps = dict_results[s]['ps']
    ax.scatter(sp, ps, c='b')
ax.plot([0, 1], [0, 1], 'k-', alpha=0.75, zorder=0)
ax.set_aspect('equal')
ax.set_xlim([0.89, 1])
ax.set_ylim([0.89, 1])
ax.set_xlabel('SP', fontsize=14)
ax.set_ylabel('PS', fontsize=14)

plt.savefig('../../../Figures/SP_vs_PS_all_models.png')

# dist of ablation results
dict_ablation_results = pickle.load(open(path2_ablation_results, 'rb'))
df = {}
df['seed'] = []
df['unit'] = []
df['Condition'] = []
for measure in ['accuracy', 'log_p_diff', 'normalized_p_diff']:
    df[measure] = []

for s in dict_ablation_results.keys():
    if s != 'K':
        ss = str(int(s) + 1)
    else:
        ss = s
    for u in dict_ablation_results[s].keys():
        df['seed'].append('Model ' + ss)
        df['unit'].append(u)
        df['Condition'].append('SP')
        df['accuracy'].append(dict_ablation_results[s][u]['SP']['accuracy'])
        df['log_p_diff'].append(dict_ablation_results[s][u]['SP']['log_p_diff'][0])
        df['normalized_p_diff'].append(dict_ablation_results[s][u]['SP']['normalized_p_diff'][0])
        df['seed'].append('Model ' + ss)
        df['unit'].append(u)
        df['Condition'].append('PS')
        df['accuracy'].append(dict_ablation_results[s][u]['PS']['accuracy'])
        df['log_p_diff'].append(dict_ablation_results[s][u]['PS']['log_p_diff'][0])
        df['normalized_p_diff'].append(dict_ablation_results[s][u]['PS']['normalized_p_diff'][0])

df = pd.DataFrame(df)
df['error'] = df.apply(lambda row: 1-row['accuracy'], axis=1)

list_order = []
for i in range(1, 20):
    list_order.append('Model %i' % i)
list_order.append('Model K')

# Plot
ylabels = {'accuracy':'Accuracy', 'log_p_diff':'Loss Difference', 'normalized_p_diff':'Success Probability'}
for measure in ['accuracy', 'log_p_diff', 'normalized_p_diff']:
    print(measure)
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.boxplot(x='seed', y=measure, hue="Condition", data=df, whis=1.5, order=list_order, ax=ax)
    sns.stripplot(x='seed',y=measure, hue="Condition", data=df, dodge=True, jitter=0.05, order=list_order, ax=ax)

    ax.get_legend().set_visible(False)
    leg = Legend(ax, [ax.patches[0], ax.patches[1]], ['SP', 'PS'], loc='lower right', frameon=False, fontsize=20)
    ax.add_artist(leg)

    ax.set_xlabel('')
    ax.set_ylabel(ylabels[measure], fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()

    plt.savefig(f'../../../Figures/Ablation_results_all_models_{measure}.png')

    #############
    # K's model #
    #############
    df_K = df.loc[df['seed'] == 'Model K']
    fig, ax = plt.subplots(figsize=(10, 10))
    # sns.boxplot(x='seed', y="performance", hue="condition", data=df_K, whis=1.5, ax=ax)
    sns.stripplot(x='seed',y=measure, hue="Condition", data=df_K, dodge=True, jitter=0.05, ax=ax)

    plt.setp(plt.gca().get_legend().get_title(),fontsize='26')
    plt.setp(plt.gca().get_legend().get_texts(), fontsize='20')

    # leg = Legend(ax, [ax.patches[0], ax.patches[1]], ['SP', 'PS'], loc='lower right', frameon=False, fontsize=20)
    # ax.add_artist(leg)
    ax.set_xlabel('')
    ax.set_xticklabels('')
    ax.set_ylabel(ylabels[measure], fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()

    df_sp = df_K.loc[df_K['Condition']=='SP']
    min_sp = eval(f'df_sp.loc[(df_sp["{measure}"] == df_sp.{measure}.min())]["{measure}"]')
    min_sp_u = eval(f'df_sp.loc[(df_sp["{measure}"] == df_sp.{measure}.min())]["unit"].values[0]')
    df_ps = df_K.loc[df_K['Condition']=='PS']
    min_ps = eval(f'df_ps.loc[(df_ps["{measure}"] == df_ps.{measure}.min())]["{measure}"]')
    min_ps_u = eval(f'df_ps.loc[(df_ps["{measure}"] == df_ps.{measure}.min())]["unit"].values[0]')
    plt.text(-0.18, min_sp, str(min_sp_u), fontsize=16)
    plt.text(0.14, min_ps, str(min_ps_u), fontsize=16)

    plt.savefig(f'../../../Figures/Ablation_results_K_model_{measure}.png')

    measure_values = eval(f'df_sp[f"{measure}"]')
    mean_sp = np.mean(measure_values)
    std_sp = np.std(measure_values)
    z_min_sp = (min_sp-mean_sp)/std_sp
    print(z_min_sp)

    measure_values = eval(f'df_ps[f"{measure}"]')
    mean_ps = np.mean(measure_values)
    std_ps = np.std(measure_values)
    z_min_ps = (min_ps-mean_ps)/std_ps
    print(z_min_ps)
