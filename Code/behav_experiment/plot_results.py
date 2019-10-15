import os
import pandas as pd
from tabulate import tabulate
import seaborn as sns
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
    props.plot(kind='bar', stacked='True', ax=ax)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Performance rate')

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
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate')
plt.tight_layout()

fn = 'error_rate_per_position_per_condition_across_subjects.png'
plt.savefig(os.path.join(path2figures, fn))


#######################################################
### INTERACTION PLOT FOR INNER VERB
######################################################
fig, axes = plt.subplots(1, 1, figsize=(10, 10))
curr_dict{}
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        test_conditions = ['SPS', 'PSP']
        control_conditions = ['SSS', 'PPP']
        SR_LR = 'LR'
    elif s_type in ['objrel', 'embedding_mental_SR']:
        test_conditions = ['SP', 'PS']
        control_conditions = ['SS', 'PP']
        SR_LR = 'SR'
    if s_type in ['objrel', 'objrel_nounpp']:
        succ_nested = 'Nested'
    elif s_type in ['embedding_mental_SR', 'embedding_mental_LR']:
        succ_nested = 'Succesive'


    df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner']))]
    df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()
    curr_dict['error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()
    curr_dict['error_rate'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean()
    curr_dict['sentence_type'] = s_type
    curr_dict['SR_LR'] = SR_LR
    curr_dict['succ_nested'] = succ_nested

#     sns.barplot(x='violation_position', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
#     ax.set_title(s_type)
#     ax.set_ylim([0, 1])
#     ax.set_ylabel('Error rate')
# plt.tight_layout()
#
# fn = 'error_rate_per_position_per_condition_across_subjects.png'
# plt.savefig(os.path.join(path2figures, fn))