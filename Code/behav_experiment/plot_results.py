import os
import pandas as pd
from tabulate import tabulate
import seaborn as sns
from statsmodels.formula.api import ols
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
from functions.get_behav_results import get_behav_LSTM_italian

path2figures = os.path.join('..', '..', 'Figures')
path2results = os.path.join('..', '..', 'Paradigm', 'Results')

#######################################################
### LOAD RESULTS DATAFRAMES
######################################################
# ALL TRIALS
fn = 'dataframe_results_all_trials.csv'
fn = os.path.join(path2results, fn)
df_all_trials = pd.read_csv(fn)

# ERROR RATES
fn = 'dataframe_results_errorrate.csv'
fn = os.path.join(path2results, fn)
df_error_rates = pd.read_csv(fn)


#######################################################
### PER SUBJECT PER ANSWER ACROSS CONDITIONS
######################################################
# Plot examples are taken from here:
# https://github.com/mwaskom/seaborn/issues/1027
# ----------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    ax = axes[i//2, i%2]
    df = df_all_trials[df_all_trials['sentence_type'] == s_type]
    props = df.groupby('subject')['valid_answer'].value_counts(normalize=True).unstack()
    props.plot(kind='bar', stacked='True', ax=ax, rot=0, legend=False)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Performance rate')

axes[0,1].legend(loc='center left', bbox_to_anchor=(1.0, 0.8))
plt.subplots_adjust(right=0.8)

fn = 'performance_rate_per_subject_per_answer_across_conditions.png'
plt.savefig(os.path.join(path2figures, fn))
plt.close(fig)

#######################################################
### PER SUBJECT PER POSITION ACROSS CONDITIONS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    ax = axes[i // 2, i % 2]
    df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='subject', y='error_rate', hue='violation_position', data=df, ax=ax)
    ax.set_title('%s' % (s_type))
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate')
plt.tight_layout()

fn = 'error_rate_per_subject_per_position_across_conditions.png'
plt.savefig(os.path.join(path2figures, fn))


#######################################################
### PER SUBJECT PER CONDITION ACROSS SUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['SSS', 'SSP', 'PPP', 'PPS', 'SPP', 'SPS', 'PSS', 'PSP']
        palette = ['b', 'c', 'b', 'c', 'r', 'm', 'r', 'm']
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = ['SS', 'PP', 'SP', 'PS']
        palette = ['b', 'b', 'r', 'r']

    ax = axes[i // 2, i % 2]
    df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'] == 'inner')]
    sns.barplot(x='subject', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
    # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()

fn = 'error_rate_per_subject_per_condition_inner_verb.png'
plt.savefig(os.path.join(path2figures, fn))


#######################################################
### PER POSITION PER CONDITION ACROSS SUBJECTS (two congruencies)
######################################################
# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
#     if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
#         hue_order = ['congruent', 'congruent_attractor', 'incongruent', 'incongruent_attractor']
#         palette = ['b', 'c', 'r', 'm']
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         df1 = df.loc[(df['condition'].isin(['SSS', 'PPP']))].mean()['error_rate']
#         df1 = df.loc[(df['condition'].isin(['SSP', 'PPS']))].mean()['error_rate']
#         df1 = df.loc[(df['condition'].isin(['SPP', 'PSS']))].mean()['error_rate']
#         df1 = df.loc[(df['condition'].isin(['SPS', 'PSP']))].mean()['error_rate']
#
#     elif s_type in ['objrel', 'embedding_mental_SR']:
#         hue_order = ['congruent', 'incongruent']
#         palette = ['b', 'r']
#
#     ax = axes[i // 2, i % 2]
#     sns.barplot(x='violation_position', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
#     # sns.set(font_scale=2)
#     ax.tick_params(labelsize=20)
#     ax.set_title(s_type)
#     ax.set_ylim([0, 1])
#     ax.set_ylabel('Error rate', fontsize=20)
#
# plt.tight_layout()
#
# fn = 'error_rate_per_position_per_condition_across_subjects.png'
# plt.savefig(os.path.join(path2figures, fn))


#######################################################
### PER POSITION PER CONDITION ACROSS SUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['SSS', 'SSP', 'PPP', 'PPS', 'SPP', 'SPS', 'PSS', 'PSP']
        palette = ['b', 'c', 'b', 'c', 'r', 'm', 'r', 'm']
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = ['SS', 'PP', 'SP', 'PS']
        palette = ['b', 'b', 'r', 'r']

    ax = axes[i // 2, i % 2]
    df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='violation_position', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
    # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()

fn = 'error_rate_per_position_per_condition_across_subjects.png'
plt.savefig(os.path.join(path2figures, fn))


#######################################################
### INTERACTION PLOT FOR INNER VERB
######################################################

def generate_interaction_plot(dict_conditions, y_name):
    '''
    :param y_name: name of dependent variable (e.g., mean_error_rate/mean_error_rate_norm)
    :param dict_conditions: keys level 1 are for first interaction dim, level 2 for second dim, and 3rd-level key is the ylabel. values are dataframes
    :return:
    '''
    first_dim = list(dict_conditions.keys())
    second_dim = list(dict_conditions[first_dim[0]].keys())

    fix, ax = plt.subplots(figsize=(20, 10))
    ls = ['-', '--']
    markers = ['+', '.']
    colors = ['c', 'r']
    x = [0, 1]
    for i, first_dim_val in enumerate(first_dim):
        y = [dict_conditions[first_dim[i]][second_dim[0]][y_name].mean(), dict_conditions[first_dim[i]][second_dim[1]][y_name].mean()]
        yerr = [dict_conditions[first_dim[i]][second_dim[0]][y_name].std()/np.sqrt(num_subjects), dict_conditions[first_dim[i]][second_dim[1]][y_name].std()/np.sqrt(num_subjects)]
        ax.errorbar(x=x, y=y, yerr=yerr, marker=markers[i], ls=ls[i], color=colors[i], label=first_dim_val, lw=2)

    ax.set_xticks((0,1))
    ax.set_xticklabels((second_dim[0], second_dim[1]), fontsize=26)
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.set_xlim((-0.2, 1.2))
    ax.set_ylim((0, 1))
    ax.set_ylabel('Error rate', fontsize=30)
    ax.axhline(0.5, ls=':', color='k', label='Chance')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
    ax.set_title('Humans', fontsize=30)
    plt.subplots_adjust(right=0.8)

    fn = 'Interaction_Italian_humans_' + '_vs_'.join(first_dim) + '_' + '_vs_'.join(second_dim) + '_' + y_name + '.png'
    plt.savefig(os.path.join(path2figures, fn))


fig, axes = plt.subplots(1, 1, figsize=(10, 10))
df_interaction = []

for subject in df_error_rates.subject.unique():
    for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
        curr_dict = {}
        if s_type == 'objrel':
            test_conditions = ['SP', 'PS']
            control_conditions = ['SS', 'PP']
            SR_LR = 'SR'
            succ_nested = 'Nested'
        elif s_type == 'objrel_nounpp':
            test_conditions = ['SPS', 'SPP', 'PSP', 'PSS']
            control_conditions = ['SSS', 'SSP', 'PPP', 'PPS']
            SR_LR = 'LR'
            succ_nested = 'Nested'
        elif s_type == 'embedding_mental_SR':
            test_conditions = ['SP', 'PS']
            control_conditions = ['SS', 'PP']
            SR_LR = 'SR'
            succ_nested = 'Succesive'
        elif s_type == 'embedding_mental_LR':
            test_conditions = ['SPS', 'SPP', 'PSP', 'PSS']
            control_conditions = ['SSS', 'SSP', 'PPP', 'PPS']
            SR_LR = 'LR'
            succ_nested = 'Succesive'

        df = df_error_rates.loc[(df_error_rates['subject'] == subject) & (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner']))]
        assert len(df.loc[(df['condition'].isin(test_conditions))]['error_rate']) in [2, 4]
        curr_dict['mean_error_rate'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean()
        curr_dict['mean_error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()

        curr_dict['subject'] = subject
        curr_dict['sentence_type'] = s_type
        curr_dict['SR_LR'] = SR_LR
        curr_dict['succ_nested'] = succ_nested
        df_interaction.append(curr_dict)

df_interaction = pd.DataFrame(df_interaction)

dict_SR_LR_succesive_nested = {}
dict_SR_LR_succesive_nested['Succesive'] = {}
dict_SR_LR_succesive_nested['Nested'] = {}
dict_SR_LR_succesive_nested['Succesive']['SR'] = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['succ_nested']=='Succesive')]
dict_SR_LR_succesive_nested['Succesive']['LR'] = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['succ_nested']=='Succesive')]
dict_SR_LR_succesive_nested['Nested']['SR'] = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['succ_nested']=='Nested')]
dict_SR_LR_succesive_nested['Nested']['LR'] = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['succ_nested']=='Nested')]

import numpy as np
num_subjects = len(df_error_rates.subject.unique())

generate_interaction_plot(dict_SR_LR_succesive_nested, 'mean_error_rate')
generate_interaction_plot(dict_SR_LR_succesive_nested, 'mean_error_rate_norm')


################
### STATS ######
################

result = ols(formula='mean_error_rate ~ SR_LR + succ_nested + SR_LR * succ_nested', data=df_interaction).fit()
print(result.summary())

result = ols(formula='mean_error_rate_norm ~ SR_LR + succ_nested + SR_LR * succ_nested', data=df_interaction).fit()
print(result.summary())



#######################################################
### INTERACTION PLOT FOR INNER VS OUTER VERB
######################################################
fig, axes = plt.subplots(1, 1, figsize=(10, 10))
df_interaction = []

for subject in df_error_rates.subject.unique():
    for i, s_type in enumerate(['objrel', 'objrel_nounpp']):
        if s_type == 'objrel':
            test_conditions = ['SP', 'PS']
            control_conditions = ['SS', 'PP']
            SR_LR = 'SR'
        elif s_type == 'objrel_nounpp':
            test_conditions = ['SPS', 'SPP', 'PSP', 'PSS']
            control_conditions = ['SSS', 'SSP', 'PPP', 'PPS']
            SR_LR = 'LR'

        for inner_outer in ['inner', 'outer']:
            curr_dict = {}
            df = df_error_rates.loc[(df_error_rates['subject'] == subject) & (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin([inner_outer]))]
            assert len(df.loc[(df['condition'].isin(test_conditions))]['error_rate']) in [2, 4]
            curr_dict['mean_error_rate'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean()
            curr_dict['mean_error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()
            curr_dict['subject'] = subject
            curr_dict['sentence_type'] = s_type
            curr_dict['SR_LR'] = SR_LR
            curr_dict['inner_outer'] = inner_outer
            df_interaction.append(curr_dict)

df_interaction = pd.DataFrame(df_interaction)

dict_SR_LR_inner_outer = {}
dict_SR_LR_inner_outer['SR'] = {}
dict_SR_LR_inner_outer['LR'] = {}
dict_SR_LR_inner_outer['SR']['inner'] = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['inner_outer']=='inner')]
dict_SR_LR_inner_outer['SR']['outer'] = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['inner_outer']=='outer')]
dict_SR_LR_inner_outer['LR']['inner'] = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['inner_outer']=='inner')]
dict_SR_LR_inner_outer['LR']['outer'] = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['inner_outer']=='outer')]


import numpy as np
num_subjects = len(df_error_rates.subject.unique())
generate_interaction_plot(dict_SR_LR_inner_outer, 'mean_error_rate')
generate_interaction_plot(dict_SR_LR_inner_outer, 'mean_error_rate_norm')


################
### STATS ######
################

print('-' * 100)
print('INNER vs OUTER')
print('-' * 100)

result = ols(formula='mean_error_rate ~ SR_LR + inner_outer + SR_LR * inner_outer', data=df_interaction).fit()
print(result.summary())

result = ols(formula='mean_error_rate_norm ~ SR_LR + inner_outer + SR_LR * inner_outer', data=df_interaction).fit()
print(result.summary())

#############################################

#############################################
behav_LSTM_italian = get_behav_LSTM_italian()
df_error_rates_LSTM = []
for sentence_type in behav_LSTM_italian['error_rate'].keys():
    for verb in behav_LSTM_italian['error_rate'][sentence_type].keys():
        for condition in behav_LSTM_italian['error_rate'][sentence_type][verb].keys():
            curr_dict = {}
            curr_dict['error_rate'] = behav_LSTM_italian['error_rate'][sentence_type][verb][condition]
            curr_dict['sentence_type'] = sentence_type
            curr_dict['condition'] = condition
            curr_dict['violation_type'] = verb
            # Add violation position
            if verb == 'V1':
                curr_dict['violation_position'] = 'outer'
            elif verb == 'V2':
                curr_dict['violation_position'] = 'inner'

            df_error_rates_LSTM.append(curr_dict)
df_error_rates_LSTM = pd.DataFrame(df_error_rates_LSTM)

#######################################################
### LSTM: PER POSITION PER CONDITION ACROSS AUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['SSS', 'SSP', 'PPP', 'PPS', 'SPP', 'SPS', 'PSS', 'PSP']
        palette = ['b', 'c', 'b', 'c', 'r', 'm', 'r', 'm']
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = ['SS', 'PP', 'SP', 'PS']
        palette = ['b', 'b', 'r', 'r']

    ax = axes[i // 2, i % 2]
    df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == s_type)]
    df = df.sort_values(by=['violation_position'])
    sns.barplot(x='violation_position', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
    # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()

fn = 'error_rate_per_position_per_condition_LSTM.png'
plt.savefig(os.path.join(path2figures, fn))


# interaction_plot(df_interaction.SR_LR, df_interaction.succ_nested, df_interaction.mean_error_rate, colors=['red','blue'], markers=['D','^'], ms=10)
# fn = 'interaction_inner_error_rate_humans.png'
# plt.savefig(os.path.join(path2figures, fn))
