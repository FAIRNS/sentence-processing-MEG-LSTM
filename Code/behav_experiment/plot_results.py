import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from functions import plotting

path2figures = os.path.join('..', '..', 'Figures')
path2results = os.path.join('..', '..', 'Paradigm', 'Results')

################################
### LOAD RESULTS DATA FRAMES ###
################################
#  ALL TRIALS
fn = 'dataframe_results_all_trials.csv'
fn = os.path.join(path2results, fn)
df_all_trials = pd.read_csv(fn)

# ERROR RATES
fn = 'dataframe_results_errorrate.csv'
fn = os.path.join(path2results, fn)
df_error_rates = pd.read_csv(fn)

fn = 'dataframe_results_errorrate_LSTM.csv'
fn = os.path.join(path2results, fn)
df_error_rates_LSTM = pd.read_csv(fn)
df_error_rates_LSTM = df_error_rates_LSTM.sort_values(['sentence_type', 'violation_position', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition'], ascending=[True, True, True, True, True, True])
df_error_rates_LSTM = df_error_rates_LSTM[df_error_rates_LSTM['subject']==1111]

##################
### BAR PLOT #####
##################

##############
# SUCCESSIVE #
##############
fig_humans, fig_model, _ = plotting.generate_fig_humans_vs_RNNs(df_error_rates, [['!!!', 'ns', '!!!'], ['!!!', 'ns/*', '!!!']], df_error_rates_LSTM, [['!!!', 'ns', '!!!'], ['!!!', 'ns', '!!!']], 'successive')

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_humans.png'
plt.figure(fig_humans.number)
plt.savefig(os.path.join(path2figures, fn))

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_model.png'
plt.figure(fig_model.number)
plt.savefig(os.path.join(path2figures, fn))

##########
# NESTED #
##########
fig_humans, fig_model,fig_legend = \
    plotting.generate_fig_humans_vs_RNNs(df_error_rates, [['***', 'ns', '**'], ['***', 'ns', '***']],
                                         df_error_rates_LSTM, [['*', '***', '***'], ['***', '***', '***']], 'nested')
plt.figure(fig_humans.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_humans.png'
plt.savefig(os.path.join(path2figures, fn))

plt.figure(fig_model.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_model.png'
plt.savefig(os.path.join(path2figures, fn))

fn = 'error_rate_per_position_per_congruency_LSTM_legend.png'
plt.figure(fig_legend.number)
plt.savefig(os.path.join(path2figures, fn))

plt.close('all')


##########################################
# FILTER BY NUMBER OF FIRST SUBJECT
##########################################

df_error_rates_LSTM_S = df_error_rates_LSTM[df_error_rates_LSTM['condition'].str.startswith('S')]
df_error_rates_S = df_error_rates[df_error_rates['condition'].str.startswith('S')]
df_error_rates_LSTM_P = df_error_rates_LSTM[df_error_rates_LSTM['condition'].str.startswith('P')]
df_error_rates_P = df_error_rates[df_error_rates['condition'].str.startswith('P')]
################
# SUCCESSIVE P #
################
fig_humans, fig_model, _ = plotting.generate_fig_humans_vs_RNNs(df_error_rates_S, [['', '', ''], ['', '', '']], df_error_rates_LSTM_S, [['', '', ''], ['', '', '']], 'successive')

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_humans_S.png'
plt.figure(fig_humans.number)
plt.savefig(os.path.join(path2figures, fn))

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_model_S.png'
plt.figure(fig_model.number)
plt.savefig(os.path.join(path2figures, fn))

fig_humans, fig_model, _ = plotting.generate_fig_humans_vs_RNNs(df_error_rates_P, [['', '', ''], ['', '', '']], df_error_rates_LSTM_P, [['', '', ''], ['', '', '']], 'successive')

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_humans_P.png'
plt.figure(fig_humans.number)
plt.savefig(os.path.join(path2figures, fn))

fn = 'error_rate_per_position_per_congruency_LSTM_succesive_model_P.png'
plt.figure(fig_model.number)
plt.savefig(os.path.join(path2figures, fn))

##########
# NESTED #
##########
fig_humans, fig_model,fig_legend = \
    plotting.generate_fig_humans_vs_RNNs(df_error_rates_S, [['', '', ''], ['', '', '']],
                                         df_error_rates_LSTM_S, [['', '', ''], ['', '', '']], 'nested')
plt.figure(fig_humans.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_humans_S.png'
plt.savefig(os.path.join(path2figures, fn))

plt.figure(fig_model.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_model_S.png'
plt.savefig(os.path.join(path2figures, fn))


fig_humans, fig_model,fig_legend = \
    plotting.generate_fig_humans_vs_RNNs(df_error_rates_P, [['', '', ''], ['', '', '']],
                                         df_error_rates_LSTM_P, [['', '', ''], ['', '', '']], 'nested')
plt.figure(fig_humans.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_humans_P.png'
plt.savefig(os.path.join(path2figures, fn))

plt.figure(fig_model.number)
fn = 'error_rate_per_position_per_congruency_LSTM_nested_model_P.png'
plt.savefig(os.path.join(path2figures, fn))


plt.close('all')

#######################################

fig_objrel, ax_objrel = plotting.generate_scatter_incongruent_subjects_V1_vs_V2(df_error_rates_LSTM, 'objrel')
plt.figure(fig_objrel.number)
plt.savefig(os.path.join(path2figures,'scatter_objrel_NLMs.png'))
fig_objrel_nounpp, ax_objrel_nounpp = plotting.generate_scatter_incongruent_subjects_V1_vs_V2(df_error_rates_LSTM, 'objrel_nounpp')
plt.figure(fig_objrel_nounpp.number)
plt.savefig(os.path.join(path2figures,'scatter_objrel_nounpp_NLMs.png'))

fig_objrel, ax_objrel = plotting.generate_scatter_incongruent_subjects_V1_vs_V2(df_error_rates, 'objrel')
plt.figure(fig_objrel.number)
plt.savefig(os.path.join(path2figures,'scatter_objrel_humans.png'))
fig_objrel_nounpp, ax_objrel_nounpp = plotting.generate_scatter_incongruent_subjects_V1_vs_V2(df_error_rates, 'objrel_nounpp')
plt.figure(fig_objrel_nounpp.number)
plt.savefig(os.path.join(path2figures,'scatter_objrel_nounpp_humans.png'))

raise SystemExit(0)


#######################################################
### MODEL vs HUMANS: PER POSITION PER CONGRUENCY ACROSS AUBJECTS
### MENTAL EMBEDDING
######################################################
#
# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# for i, s_type in enumerate(['embedding_mental_SR', 'embedding_mental_LR']):
#     if s_type in ['embedding_mental_LR']:
#         hue_order = [True, False]
#         palette = ['b', 'r']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax, hue_order=hue_order, palette=palette)
#         ax.tick_params(labelsize=20)
#         # ax.set_ylim([0, 0.5])
#         ax.set_xlabel('', fontsize=20)
#         ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#     elif s_type in ['objrel', 'embedding_mental_SR']:
#         hue_order = [True, False]
#         palette = ['b', 'r']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[
#             (df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#         ax.tick_params(labelsize=20)
#         # ax.set_ylim([0, 0.5])
#         ax.set_xlabel('', fontsize=20)
#         ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#
#         # sns.set(font_scale=2)
#     ax.tick_params(labelsize=20)
#     ax.set_title(s_type)
#     ax.set_ylim([0, 0.5])
#     ax.set_ylabel('Error rate', fontsize=20)
#
#
#
#
# plt.tight_layout()
# fn = 'error_rate_per_position_per_congruency_LSTM_mental.png'
# plt.savefig(os.path.join(path2figures, fn))


#######################################################
### MODEL vs HUMANS: PER POSITION PER CONGRUENCY ACROSS AUBJECTS
### OBJREL
######################################################
#
# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# for i, s_type in enumerate(['objrel', 'objrel_nounpp']):
#     if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
#         hue_order = [True, False]
#         palette = ['b', 'r']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax, hue_order=hue_order, palette=palette)
#         ax.get_legend().set_visible(False)
#         ax.set_xlabel('')
#         ax.tick_params(labelsize=20)
#         ax.set_xticklabels(['Embedded', 'Main'])
#         ax.set_yticklabels([])
#         ax.set_ylim([0, 1.2])
#         ax.set_ylabel('')
#         plotting.add_significance(ax, '***', '**', 'ns')#, pad_y=0.03, pad_y_interaction=0.03)
#         # ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#         ax.set_yticklabels([])
#         plotting.add_significance(ax, 'ns', '*', '**')
#     elif s_type in ['objrel', 'embedding_mental_SR']:
#         hue_order = [True, False]
#         palette = ['b', 'r']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[
#             (df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#         ax.get_legend().set_visible(False)
#         ax.set_xlabel('')
#         ax.set_xticklabels(['Embedded', 'Main'])
#         ax.tick_params(labelsize=20)
#         ax.set_ylim([0, 1.2])
#         ax.set_ylabel('')
#         plotting.add_significance(ax, 'ns', '*', 'ns')
#         # ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#         plotting.add_significance(ax, '*', 'ns', '**')
#
#         # sns.set(font_scale=2)
#     ax.get_legend().set_visible(False)
#     ax.tick_params(labelsize=20)
#     # ax.set_title(s_type)
#     ax.set_ylim([0, 0.7])
#     ax.set_ylabel('Error rate', fontsize=20)
#     ax.set_xlabel('')
#     ax.set_xticklabels(['Embedded', 'Main'])
#     ax.set_ylabel('')
#
#
#
#
# # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=False, ncol=2)
#
# handles, labels = ax.get_legend_handles_labels()
# fig.legend(handles, ['Congruent Subjects', 'Incongruent Subjects'], loc='upper center', bbox_to_anchor=(0.5, 0.97), ncol=2, fontsize=16)
# plt.subplots_adjust(left=0.15, right=0.85, top=0.9)
#
# #
# fig.text(x=0.25, y=0.03, s='Succesive', fontsize=26)
# fig.text(x=0.65, y=0.03, s='Nested', fontsize=26)
# fig.text(x=0.03, y=0.75, s='Humans', fontsize=26, rotation=90)
# fig.text(x=0.03, y=0.3, s='RNNs', fontsize=26, rotation=90)



################################################
### PER SUBJECT PER ANSWER ACROSS CONDITIONS ###
################################################
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
### PER SUBJECT PER CONDITION ACROSS
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

fn = 'error_rate_violation_per_position_per_condition_across_subjects.png'
plt.savefig(os.path.join(path2figures, fn))

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
    df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Acceptable') & (df_error_rates['violation_type'].isin(['None', 'FI', 'FA']))]
    sns.barplot(x='violation_type', y='error_rate', hue='condition' , data=df, ax=ax, hue_order=hue_order, palette=palette)
    # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()

fn = 'error_rate_acceptable_per_position_per_condition_across_subjects.png'
plt.savefig(os.path.join(path2figures, fn))

#######################################################
### PER POSITION PER CONGRUENCY ACROSS SUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    ax = axes[i // 2, i % 2]
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['True_True', 'True_False', 'False_True', 'False_False']
        palette = ['b', 'c', 'r', 'm']
        df = df_error_rates.loc[(df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (df_error_rates['violation_position'].isin(['inner', 'outer']))]
        sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects_attractor', data=df, ax=ax, hue_order=hue_order, palette=palette)
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = [True, False]
        palette = ['b', 'r']
        df = df_error_rates.loc[
            (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
                df_error_rates['violation_position'].isin(['inner', 'outer']))]
        sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                    hue_order=hue_order, palette=palette)


        # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()

fn = 'error_rate_per_position_per_subject_congruency_across_subjects.png'
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
        # curr_dict['mean_error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()

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

num_subjects = len(df_error_rates.subject.unique())

generate_interaction_plot(dict_SR_LR_succesive_nested, 'mean_error_rate')
# generate_interaction_plot(dict_SR_LR_succesive_nested, 'mean_error_rate_norm')


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
            # curr_dict['mean_error_rate_norm'] = df.loc[(df['condition'].isin(test_conditions))]['error_rate'].mean() - df.loc[(df['condition'].isin(control_conditions))]['error_rate'].mean()
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
# generate_interaction_plot(dict_SR_LR_inner_outer, 'mean_error_rate_norm')




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

#######################################################
### LSTM: PER POSITION PER CONGRUENCY ACROSS AUBJECTS
######################################################
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
for i, s_type in enumerate(['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    ax = axes[i // 2, i % 2]
    if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
        hue_order = ['True_True', 'True_False', 'False_True', 'False_False']
        palette = ['b', 'c', 'r', 'm']
        df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
        sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects_attractor', data=df, ax=ax, hue_order=hue_order, palette=palette)
    elif s_type in ['objrel', 'embedding_mental_SR']:
        hue_order = [True, False]
        palette = ['b', 'r']
        df = df_error_rates_LSTM.loc[
            (df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
        sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                    hue_order=hue_order, palette=palette)


        # sns.set(font_scale=2)
    ax.tick_params(labelsize=20)
    ax.set_title(s_type)
    ax.set_ylim([0, 1])
    ax.set_ylabel('Error rate', fontsize=20)

plt.tight_layout()
fn = 'error_rate_per_position_per_congruency_LSTM.png'
plt.savefig(os.path.join(path2figures, fn))




# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# for i, s_type in enumerate(['objrel', 'objrel_nounpp']):
#     if s_type in ['objrel_nounpp', 'embedding_mental_LR']:
#         hue_order = ['True_True', 'True_False', 'False_True', 'False_False']
#         palette = ['b', 'c', 'r', 'm']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects_attractor', data=df, ax=ax, hue_order=hue_order, palette=palette)
#         ax.tick_params(labelsize=20)
#         ax.set_ylim([0, 1])
#         ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects_attractor', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#     elif s_type in ['objrel', 'embedding_mental_SR']:
#         hue_order = [True, False]
#         palette = ['b', 'r']
#         # MODEL
#         ax = axes[1, i]
#         df = df_error_rates_LSTM.loc[
#             (df_error_rates_LSTM['sentence_type'] == s_type) & (df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#         ax.tick_params(labelsize=20)
#         ax.set_ylim([0, 1])
#         ax.set_ylabel('Error rate', fontsize=20)
#         # HUMANS
#         ax = axes[0, i]
#         df = df_error_rates.loc[
#             (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
#                 df_error_rates['violation_position'].isin(['inner', 'outer']))]
#         sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
#                     hue_order=hue_order, palette=palette)
#
#         # sns.set(font_scale=2)
#     ax.tick_params(labelsize=20)
#     ax.set_title(s_type)
#     ax.set_ylim([0, 1])
#     ax.set_ylabel('Error rate', fontsize=20)
#
# plt.tight_layout()
# fn = 'error_rate_per_position_per_congruency_LSTM_objrel.png'
# plt.savefig(os.path.join(path2figures, fn))


#############################################
# from functions.get_behav_results import get_behav_LSTM_italian
# behav_LSTM_italian = get_behav_LSTM_italian()
# df_error_rates_LSTM = []
# for sentence_type in behav_LSTM_italian['error_rate'].keys():
#     for verb in behav_LSTM_italian['error_rate'][sentence_type].keys():
#         for condition in behav_LSTM_italian['error_rate'][sentence_type][verb].keys():
#             curr_dict = {}
#             curr_dict['error_rate'] = behav_LSTM_italian['error_rate'][sentence_type][verb][condition]
#             curr_dict['sentence_type'] = sentence_type
#             curr_dict['condition'] = condition
#             if curr_dict['condition'][0] == curr_dict['condition'][1]:
#                 curr_dict['congruent_subjects'] = True
#             else:
#                 curr_dict['congruent_subjects'] = False
#             if len(curr_dict['condition']) > 2:
#                 if curr_dict['condition'][1] == curr_dict['condition'][2]:
#                     curr_dict['congruent_attractor'] = True
#                 else:
#                     curr_dict['congruent_attractor'] = False
#                 curr_dict['congruent_subjects_attractor'] = '_'.join(
#                     map(str, [curr_dict['congruent_subjects'], curr_dict['congruent_attractor']]))
#             else:
#                 curr_dict['congruent_attractor'] = np.nan
#                 curr_dict['congruent_subjects_attractor'] = np.nan
#             curr_dict['violation_type'] = verb
#             # Add violation position
#             if verb == 'V1':
#                 curr_dict['violation_position'] = 'outer'
#             elif verb == 'V2':
#                 curr_dict['violation_position'] = 'inner'
#
#             df_error_rates_LSTM.append(curr_dict)
# df_error_rates_LSTM = pd.DataFrame(df_error_rates_LSTM)
