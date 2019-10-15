import os, argparse, glob
import pandas as pd
import numpy as np
from tabulate import tabulate
from functions import data_manip


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subjects', action='append', type=int, default= [6, 7, 8, 9])
parser.add_argument('--sessions', action='append', type=int, default=[])
parser.add_argument('--path2logs', default='../../Paradigm/Logs')
parser.add_argument('-v', '--verbose', default=False, action='store_true')
args = parser.parse_args()


valid_correct = ['CORRECT', 'CORRECT_INC']
valid_wrong = ['WRONG', 'WRONG_INC']

trial_types = ['V1', 'V2', 'acceptable', 'filler']

if not args.sessions: # set default session 1 to all subjects
    args.sessions = [1 for _ in args.subjects]

# Init dicts
dict_per_struct_with_all_subject = {} # List of dicts (dict per subject)
dict_count_trials = {}
for sentence_type in ['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']:
    dict_per_struct_with_all_subject[sentence_type] = {}
    dict_count_trials[sentence_type] = {}
    for trial_type in trial_types:
        dict_per_struct_with_all_subject[sentence_type][trial_type] = []
        dict_count_trials[sentence_type][trial_type] = []


# Load data and generate dataframes:
df_all_trial = data_manip.read_logs(args, valid_correct, valid_wrong)
cols = ['subject', 'sentence_type', 'trial_type', 'violation_type', 'violation_position', 'condition', 'correct_wrong', 'valid_answer', 'block', 'trial_num', 'slide_num_of_viol', 'RT']
df_all_trial = df_all_trial[cols]
df_all_trial = df_all_trial.sort_values(['subject', 'sentence_type', 'trial_type', 'violation_type', 'condition', 'correct_wrong', 'block', 'trial_num'], ascending=[True, True, True, True, True, True, True, True])


df_error_rates = data_manip.get_error_rates(df_all_trial)
cols = ['subject', 'sentence_type', 'trial_type', 'violation_type', 'violation_position', 'condition', 'error_rate']
df_error_rates = df_error_rates[cols]
df_error_rates = df_error_rates.sort_values(['subject', 'sentence_type', 'trial_type', 'violation_type', 'condition'], ascending=[True, True, True, True, True])

# Save dataframes for down-stream analses
fn = 'dataframe_results_all_trials.csv'
fn = os.path.join('..', '..', 'Paradigm', 'Results', fn)
df_all_trial.to_csv(fn, index=False)

fn = 'dataframe_results_errorrate.csv'
fn = os.path.join('..', '..', 'Paradigm', 'Results', fn)
df_error_rates.to_csv(fn, index=False)

if args.verbose:
    print('\n'*3)
    print('ALL TRIALS')
    print('\n' + '-' * 150 + '\n' + '-' * 100)
    print(tabulate(df_all_trial, headers='keys', tablefmt="fancy_grid", numalign="center"))
    print('\n'*3)
    print('ERROR RATES')
    print('\n' + '-' * 150 + '\n' + '-' * 100)
    print(tabulate(df_error_rates, headers='keys', tablefmt="fancy_grid", numalign="center"))