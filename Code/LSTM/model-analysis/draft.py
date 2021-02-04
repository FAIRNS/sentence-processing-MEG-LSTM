#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:18:24 2021

@author: yl254115
"""

import os,pickle
import numpy as np
import pandas as pd
path2sentences = '../../../Data/Stimuli/nounpp_Italian_4000.info'
path2sentences_txt = '../../../Data/Stimuli/nounpp_Italian_4000.txt'

# Load ablation results and sentence metadata (info)
info = pickle.load(open(path2sentences, 'rb'))
results = pickle.load(open('../../../Output/top_k_italian_hidden650_batch64_dropout0.2_lr20.0_seed_K.pt815_1119_1101_826_819_1092_1232_713_849_759_groupsize_1_seed_1.abl', 'rb'))

# Find indices of the incogruent conditions
IXs_SP = [i for (i, d) in enumerate(info) if (d['number_1'] == 'singular') and (d['number_2'] == 'plural')]
IXs_PS = [i for (i, d) in enumerate(info) if (d['number_1'] == 'plural') and (d['number_2'] == 'singular')]

acc_SP = np.sum((results['log_p_targets_correct'][IXs_SP] - results['log_p_targets_wrong'][IXs_SP]) > 0)/len(IXs_SP)
acc_PS = np.sum((results['log_p_targets_correct'][IXs_PS] - results['log_p_targets_wrong'][IXs_PS]) > 0)/len(IXs_PS)

print(f'Accuracy PS: {acc_PS}, accuracy SP {acc_SP}')

#####################
with open(os.path.join(path2sentences_txt), 'r') as f:
    task = f.readlines()
    N1s = [l.split('\t')[3] for l in task]
    N2s = [l.split('\t')[5] for l in task]

IX_SP = [i for i, (n1, n2) in enumerate(zip(N1s, N2s)) if (n1 == 'singular') and (n2 == 'plural')]
IX_PS = [i for i, (n1, n2) in enumerate(zip(N1s, N2s)) if (n1 == 'plural') and (n2 == 'singular')]



acc_SP = []
acc_PS = []
for N1, N2, p_correct, p_wrong in zip(N1s, N2s, results['log_p_targets_correct'], results['log_p_targets_wrong']):
    if (N1 == 'singular') and (N2 == 'plural'):
        if p_correct > p_wrong:
            acc_SP.append(1)
        else:
            acc_SP.append(0)
    elif (N1 == 'plural') and N2 == ('singular'):
        if p_correct > p_wrong:
            acc_PS.append(1)
        else:
            acc_PS.append(0)


print(sum(acc_SP)/len(IX_SP), sum(acc_PS)/len(IX_PS))


##########################
def load_ablation_results(path2results):
    
    dict_ablation_results = pickle.load(open(path2results, 'rb'))
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
    df['error'] = df.apply(lambda row: 1-row['performance']['accuracy'], axis=1)
    
    return df

##########################################

df = load_ablation_results('dict_ablation_results.pkl')
print(df)
for condition in ['SP', 'PS']:
    df_curr_model_condition = df.loc[(df.seed==f'Model 5') & (df.Condition == condition)]
    df_sorted = df_curr_model_condition.sort_values(by=['error'], ascending=False)
    top_k_units = df_sorted.head(10).unit.tolist()
    top_perf = df_sorted.head(10).performance.tolist()
    print(top_k_units, top_perf)
