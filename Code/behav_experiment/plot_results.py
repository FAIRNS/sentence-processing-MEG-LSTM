import os
import pandas as pd
from tabulate import tabulate
import seaborn as sns
from statsmodels.formula.api import ols
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt

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
### PER POSITION PER CONDITION ACROSS AUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['SSS', 'SSP', 'SPS', 'SPP', 'PPP', 'PPS', 'PSP', 'PSS']
        palette = ['r', 'm', 'm', 'r', 'b', 'c', 'c', 'b']
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = ['SS', 'SP', 'PS', 'PP']
        palette = ['r', 'm', 'c', 'b']

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
            test_conditions = ['SPS', 'PSP']
            control_conditions = ['SSS', 'PPP']
            SR_LR = 'LR'
            succ_nested = 'Nested'
        elif s_type == 'embedding_mental_SR':
            test_conditions = ['SP', 'PS']
            control_conditions = ['SS', 'PP']
            SR_LR = 'SR'
            succ_nested = 'Succesive'
        elif s_type == 'embedding_mental_LR':
            test_conditions = ['SPS', 'PSP']
            control_conditions = ['SSS', 'PPP']
            SR_LR = 'LR'
            succ_nested = 'Succesive'

        df = df_error_rates.loc[(df_error_rates['subject'] == subject) & (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner']))]
        assert len(df.loc[(df['condition'].isin(test_conditions))]['error_rate']) == 2
        curr_dict['mean_error_rate'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean()
        curr_dict['mean_error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()

        curr_dict['subject'] = subject
        curr_dict['sentence_type'] = s_type
        curr_dict['SR_LR'] = SR_LR
        curr_dict['succ_nested'] = succ_nested
        df_interaction.append(curr_dict)

df_interaction = pd.DataFrame(df_interaction)

SR_succesive = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['succ_nested']=='Succesive')]
LR_succesive = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['succ_nested']=='Succesive')]
SR_nested = df_interaction.loc[(df_interaction['SR_LR']=='SR') & (df_interaction['succ_nested']=='Nested')]
LR_nested = df_interaction.loc[(df_interaction['SR_LR']=='LR') & (df_interaction['succ_nested']=='Nested')]

import numpy as np
num_subjects = len(df_error_rates.subject.unique())
def generate_interaction_plot(y_name):
    fix, ax = plt.subplots(figsize=(20, 10))
    ax.errorbar([0, 1], [SR_succesive[y_name].mean(), LR_succesive[y_name].mean()], yerr=[SR_succesive[y_name].std()/np.sqrt(num_subjects), LR_succesive[y_name].std()/np.sqrt(num_subjects)], marker='.', ls='--', color='c', label='Succesive', lw=2)
    ax.errorbar([0, 1], [SR_nested[y_name].mean(), LR_nested[y_name].mean()], yerr=[SR_nested[y_name].std()/np.sqrt(num_subjects), LR_nested[y_name].std()/np.sqrt(num_subjects)], marker='+', ls='-', color='r', label='Nested', lw=2)
    ax.set_xticks((0,1))
    ax.set_xticklabels(('Short-range', 'Long-range'), fontsize=26)
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.set_xlim((-0.2, 1.2))
    ax.set_ylim((0, 1))
    ax.set_ylabel('Error rate on V2', fontsize=30)
    ax.axhline(0.5, ls=':', color='k', label='Chance')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
    ax.set_title('Humans', fontsize=30)
    plt.subplots_adjust(right=0.8)

    fn = 'Interaction_Italian_humans_' + y_name + '.png'
    plt.savefig(os.path.join(path2figures, fn))

generate_interaction_plot('mean_error_rate')
generate_interaction_plot('mean_error_rate_norm')


################
### STATS ######
################

result = ols(formula='mean_error_rate ~ SR_LR + succ_nested + SR_LR * succ_nested', data=df_interaction).fit()
print(result.summary())

result = ols(formula='mean_error_rate_norm ~ SR_LR + succ_nested + SR_LR * succ_nested', data=df_interaction).fit()
print(result.summary())


# interaction_plot(df_interaction.SR_LR, df_interaction.succ_nested, df_interaction.mean_error_rate, colors=['red','blue'], markers=['D','^'], ms=10)
# fn = 'interaction_inner_error_rate_humans.png'
# plt.savefig(os.path.join(path2figures, fn))
