import os, argparse, glob
import pandas as pd
import numpy as np
from tabulate import tabulate
from functions import data_manip

path2results = os.path.join('..', '..', 'Paradigm', 'Results')

################################
### LOAD RESULTS DATA FRAMES ###
################################
#  ALL TRIALS
fn = 'dataframe_results_all_trials_LSTM.csv'
fn = os.path.join(path2results, fn)
df_all_trials = pd.read_csv(fn)

# Fix some stuff
# df_all_trials['valid_answer'] = df_all_trials['valid_answer'].replace({True:'CORRECT', False:'WRONG'})
# df_all_trials['correct_wrong'] = df_all_trials['correct_wrong'].replace({True:'CORRECT', False:'WRONG'})
df_all_trials.violation_type = df_all_trials.violation_type.fillna('None')
df_all_trials.trial_type = df_all_trials.trial_type.fillna('Violation')


# def outer2inner(row):
#     if (row['sentence_type'] in ['embedding_mental_SR', 'embedding_mental_LR']) and (row['violation_position'] == 'outer'):
#         return 'inner'
#     else:
#         return row['violation_position']
# df_all_trials['violation_position'] = df_all_trials.apply(lambda row: outer2inner(row), axis=1)

def process_row(row):
    if (row['sentence_type'] in ['objrel', 'objrel_nounpp']) and (row['violation_position'] == 'inner'):
        return 'V1'
    elif (row['sentence_type'] in ['objrel', 'objrel_nounpp']) and (row['violation_position'] == 'outer'):
        return 'V2'
    elif (row['sentence_type'] in ['embedding_mental_SR', 'embedding_mental_LR']) and (row['violation_position'] == 'inner'):
        return 'V2'


df_all_trials['violation_type'] = df_all_trials.apply(lambda row: process_row(row), axis=1)

fn = 'dataframe_results_all_trials_LSTM_fixed.csv'
fn = os.path.join(path2results, fn)
df_all_trials.to_csv(fn, index=False)

# ERR
print('Calculating error rates...')
df_error_rates = data_manip.get_error_rates(df_all_trials)
cols = ['subject', 'sentence_type', 'trial_type', 'violation_type', 'violation_position', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition', 'error_rate']
df_error_rates = df_error_rates[cols]
df_error_rates = df_error_rates.sort_values(['subject', 'sentence_type', 'trial_type', 'violation_type', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition'], ascending=[True, True, True, True, True, True, True, True])


fn = 'dataframe_results_errorrate_LSTM.csv'
fn = os.path.join('..', '..', 'Paradigm', 'Results', fn)
df_error_rates.to_csv(fn, index=False)