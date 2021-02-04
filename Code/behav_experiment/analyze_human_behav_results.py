import os, argparse, glob
import pandas as pd
import numpy as np
from tabulate import tabulate
from functions import data_manip


parser = argparse.ArgumentParser()
# parser.add_argument('--subjects', action='append', type=int, default= list(range(6, 12)) + [13, 14] + list(range(21, 31)))
parser.add_argument('--subjects', action='append', type=int, default= list(range(21,47)) + list(range(48, 57)) + [58, 61, 62, 64] + list(range(66, 70)) + list(range(71, 83)))
# parser.add_argument('--subjects', action='append', type=int, default= list(range(21,23)))
parser.add_argument('--sessions', action='append', type=int, default=[])
parser.add_argument('--path2logs', default='../../Paradigm/Logs')
parser.add_argument('-v', '--verbose', default=False, action='store_true')
args = parser.parse_args()

print('Total number of subject: %i' % len(args.subjects))
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
print('Reading logs...')
df_all_trial = data_manip.read_logs(args, valid_correct, valid_wrong)
cols = ['subject', 'sentence_type', 'trial_type', 'violation_type', 'violation_position', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition', 'correct_wrong', 'valid_answer', 'block', 'trial_num', 'slide_num_of_viol', 'RT']
df_all_trial = df_all_trial[cols]
df_all_trial = df_all_trial.sort_values(['subject', 'sentence_type', 'trial_type', 'violation_type', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition', 'correct_wrong', 'block', 'trial_num'], ascending=[True, True, True, True, True, True, True, True, True, True, True])


outlier_subjects = data_manip.get_outlier_subjects(df_all_trial)
print('Outlier subjects: ', outlier_subjects)
def is_outlier(row):
    return True if row['subject'] in outlier_subjects else False
df_all_trial['is_outlier'] = df_all_trial.apply(lambda row: is_outlier(row), axis=1)

# df_all_trial_without_outliers = df_all_trial.loc[(~df_all_trial['subject'].isin(outlier_subjects))]
# print(df_all_trial_without_outliers.subject.unique())

# Save dataframes for down-stream analses
fn = 'dataframe_results_all_trials.csv'
fn = os.path.join('..', '..', 'Paradigm', 'Results', fn)
df_all_trial.to_csv(fn, index=False)


print('Calculating error rates...')
df_error_rates = data_manip.get_error_rates(df_all_trial)
cols = ['subject', 'sentence_type', 'trial_type', 'violation_type', 'violation_position', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition', 'error_rate']
df_error_rates = df_error_rates[cols]
df_error_rates = df_error_rates.sort_values(['subject', 'sentence_type', 'trial_type', 'violation_type', 'congruent_subjects', 'congruent_attractor', 'congruent_subjects_attractor', 'condition'], ascending=[True, True, True, True, True, True, True, True])


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