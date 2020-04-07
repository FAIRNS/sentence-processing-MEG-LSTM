import matplotlib.pyplot as plt
import pickle
from matplotlib.legend import Legend
import seaborn as sns
import pandas as pd
import numpy as np
path2_fullmodel_results = '/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Pipeline/Italian_nounpp_results_19_models'
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
df['performance'] = []
for s in dict_ablation_results.keys():
    if s != 'K':
        ss = str(int(s) + 1)
    else:
        ss = s
    for u in dict_ablation_results[s].keys():
        df['seed'].append('Model ' + ss)
        df['unit'].append(u)
        df['Condition'].append('SP')
        df['performance'].append(dict_ablation_results[s][u]['SP'])
        df['seed'].append('Model ' + ss)
        df['unit'].append(u)
        df['Condition'].append('PS')
        df['performance'].append(dict_ablation_results[s][u]['PS'])

df = pd.DataFrame(df)
df['error'] = df.apply(lambda row: 1-row['performance'], axis=1)

fig, ax = plt.subplots(figsize=(20, 10))
list_order = []
for i in range(1, 20):
    list_order.append('Model %i' % i)
list_order.append('Model K')
sns.boxplot(x='seed', y="performance", hue="Condition", data=df, whis=1.5, order=list_order, ax=ax)
sns.stripplot(x='seed',y="performance", hue="Condition", data=df, dodge=True, jitter=0.05, order=list_order, ax=ax)

ax.get_legend().set_visible(False)
leg = Legend(ax, [ax.patches[0], ax.patches[1]], ['SP', 'PS'], loc='lower right', frameon=False, fontsize=20)
ax.add_artist(leg)

ax.set_xlabel('')
ax.set_ylabel('Accuracy', fontsize=30)
ax.tick_params(axis='both', which='major', labelsize=12)
plt.tight_layout()

plt.savefig('../../../Figures/Ablation_results_all_models.png')


# K's model
df_K = df.loc[df['seed'] == 'Model K']
fig, ax = plt.subplots(figsize=(10, 10))
# sns.boxplot(x='seed', y="performance", hue="condition", data=df_K, whis=1.5, ax=ax)
sns.stripplot(x='seed',y="performance", hue="Condition", data=df_K, dodge=True, jitter=0.05, ax=ax)
# ax.get_legend().set_visible(False)
# leg = Legend(ax, [ax.patches[0], ax.patches[1]], ['SP', 'PS'], loc='lower right', frameon=False, fontsize=20)
# ax.add_artist(leg)
ax.set_xlabel('')
ax.set_xticklabels('')
ax.set_ylabel('Accuracy', fontsize=30)
ax.tick_params(axis='both', which='major', labelsize=12)
plt.tight_layout()

df_sp = df_K.loc[df_K['Condition']=='SP']
min_sp = df_sp.loc[(df_sp['performance'] == df_sp.performance.min())]['performance']
min_sp_u = df_sp.loc[(df_sp['performance'] == df_sp.performance.min())]['unit'].values[0]
df_sp = df_K.loc[df_K['Condition']=='PS']
min_ps = df_sp.loc[(df_sp['performance'] == df_sp.performance.min())]['performance']
min_ps_u = df_sp.loc[(df_sp['performance'] == df_sp.performance.min())]['unit'].values[0]
plt.text(-0.18, min_sp, str(min_sp_u), fontsize=16)
plt.text(0.14, min_ps, str(min_ps_u), fontsize=16)

plt.savefig('../../../Figures/Ablation_results_K_model.png')
