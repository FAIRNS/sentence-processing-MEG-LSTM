import os, argparse, glob
import pandas as pd
import numpy as np
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subjects', action='append', type=int, default=[2, 3, 5])
parser.add_argument('--sessions', action='append', type=int, default=[])
parser.add_argument('--path2logs', default='../../Paradigm/Logs')
args = parser.parse_args()


valid_corrects = ['CORRECT', 'CORRECT_INC', 'CORRECT_DDC']
valid_wrongs = ['WRONG', 'WRONG_INC', 'WRONG_DDC']
trial_types = ['V1', 'V2', 'acceptable', 'filler']


dict_per_struct_with_all_subject = {} # List of dicts (dict per subject)
for sentence_type in ['objrel_that', 'objrel_nounpp', 'embedding_mental', 'embedding_mental_SR']:
    dict_per_struct_with_all_subject[sentence_type] = {}
    for tt in trial_types:
        dict_per_struct_with_all_subject[sentence_type][tt] = []

if not args.sessions: # set default session 1 to all subjects
    args.sessions = [1 for _ in args.subjects]

summary_all_trials_all_subject = []
for subject, session in zip(args.subjects, args.sessions):
    base_fn = 'logLocalGlobalParadigm_*_Subj_%02d_sess_%i.csv' % (subject, session)
    fn = glob.glob(os.path.join(args.path2logs, base_fn))
    if len(fn)==1:
        fn = fn[0]
    else:
        raise('Log file was not found or subject file is repeated for several dates')

    with open(fn, 'r') as f_log:
        lines = f_log.readlines()

    summary_all_trials = [] # List of dicts with keys: 'trial_num', 'violation_type', 'block', 'correct_wrong', 'RT', 'sentence_type', 'condition', 'slide_num_of_viol'

    cnt_trials = 0
    for l in lines:
        fields = l.split('\t')
        if fields[0] == 'END_TRIAL':
            cnt_trials += 1
            curr_dict = {}
            curr_dict['subject'] = subject
            curr_dict['block'] = fields[1]
            curr_dict['trial_num'] = fields[2]
            curr_dict['sentence_type'] = fields[7]
            curr_dict['condition'] = fields[8]
            curr_dict['violation_type'] = fields[10]
            curr_dict['slide_num_of_viol'] = int(fields[9])
            curr_dict['correct_wrong'] = fields[5]
            curr_dict['RT'] = fields[6]
            summary_all_trials.append(curr_dict)

    # print(cnt_trials)
    summary_all_trials_all_subject.extend(summary_all_trials)
    #########################################
    #### CALC ERROR RATES FOR CURR SUBJ #####
    #########################################


    for sentence_type in ['objrel_that', 'objrel_nounpp', 'embedding_mental', 'embedding_mental_SR']:
        conditions = list(set([d['condition'] for d in summary_all_trials if d['sentence_type']==sentence_type]))
        for trial_type in trial_types:
            curr_subj_dict = {}
            for condition in conditions:
                if trial_type in ['V1', 'V2']:
                    num_valid_correct_responses = sum([1 for d in summary_all_trials if (d['correct_wrong'] in valid_corrects and d['sentence_type']==sentence_type and d['condition']==condition and d['violation_type']==trial_type) and int(d['slide_num_of_viol'])>0])
                    num_valid_wrong_responses = sum([1 for d in summary_all_trials if (d['correct_wrong'] in valid_wrongs and d['sentence_type']==sentence_type and d['condition']==condition and d['violation_type']==trial_type and int(d['slide_num_of_viol'])>0)])
                elif trial_type == 'acceptable':  # Nan is acceptable in logs
                    num_valid_correct_responses = sum([1 for d in summary_all_trials if (
                                d['correct_wrong'] in valid_corrects and d['sentence_type'] == sentence_type and d[
                            'condition'] == condition and d['violation_type'] == 'NaN') and int(
                        d['slide_num_of_viol']) == 0])
                    num_valid_wrong_responses = sum([1 for d in summary_all_trials if (
                                d['correct_wrong'] in valid_wrongs and d['sentence_type'] == sentence_type and d[
                            'condition'] == condition and d['violation_type'] == 'NaN' and int(
                            d['slide_num_of_viol']) == 0)])
                elif trial_type == 'filler':
                    num_valid_correct_responses = sum([1 for d in summary_all_trials if (d['correct_wrong'] in valid_corrects and d['sentence_type'] == sentence_type and d['condition'] == condition and int(d['slide_num_of_viol'])) < 0])
                    num_valid_wrong_responses = sum([1 for d in summary_all_trials if (d['correct_wrong'] in valid_wrongs and d['sentence_type'] == sentence_type and d['condition'] == condition and int(d['slide_num_of_viol']) < 0)])

                num_valid_responses_total = num_valid_correct_responses + num_valid_wrong_responses
                # Store in dict
                curr_subj_dict['subject'] = subject
                # curr_subj_dict['sentence_type'] = sentence_type
                # curr_subj_dict['conditions'] = conditions
                if num_valid_responses_total > 0:
                    curr_subj_dict[condition] = num_valid_wrong_responses/num_valid_responses_total
                else:
                    curr_subj_dict[condition] = np.nan

            dict_per_struct_with_all_subject[sentence_type][trial_type].append(curr_subj_dict)

results_per_trial = pd.DataFrame(summary_all_trials_all_subject)
cols = ['subject', 'sentence_type', 'violation_type', 'condition', 'correct_wrong', 'block', 'trial_num', 'slide_num_of_viol', 'RT']
results_per_trial = results_per_trial[cols]
results_per_trial = results_per_trial.sort_values(['subject', 'sentence_type', 'violation_type', 'condition', 'correct_wrong', 'block', 'trial_num'], ascending=[True, True, True, True, True, True, True])
results_per_trial = results_per_trial[results_per_trial['slide_num_of_viol']>0]
# print(results_per_trial)


print('-' * 12)
print('ERROR RATES:')
print('-' * 12 + '\n')

for i, sentence_type in enumerate(['objrel_that', 'objrel_nounpp', 'embedding_mental', 'embedding_mental_SR']):
    print('%s:' % sentence_type.upper())
    print('-' * 100 + '\n' + '-' * 100)
    for violation_type in trial_types:
        print('%s - %s:' % (sentence_type, violation_type))

        results_per_subject = pd.DataFrame(dict_per_struct_with_all_subject[sentence_type][violation_type])
        cols = list(results_per_subject)
        cols = ['subject'] + cols[:-1]
        results_per_subject = results_per_subject[cols]
        results_per_subject.loc['mean'] = results_per_subject.mean()
        print(tabulate(results_per_subject, headers='keys', tablefmt="fancy_grid", numalign="center"))
        print('\n'*3)

        # WRITE MEAN ERROR RATE TO FILE IF V2
        if violation_type=='V2':
            if sentence_type == 'objrel_that':
                s_type = 'objrel'
            elif sentence_type == 'embedding_mental':
                s_type = 'embedding_mental_LR'
            else:
                s_type = sentence_type
            fn = 'mean_error_rate_' + s_type + '.behav_res'
            fn = os.path.join('..', '..', 'Paradigm', 'Results', fn)
            conditions = list(set([d['condition'] for d in summary_all_trials if d['sentence_type'] == sentence_type]))
            with open(fn, 'w') as f_sent_type:
                for cond in conditions:
                    str = '%s \t %1.2f\n' % (cond, results_per_subject.iloc[-1][cond])
                    f_sent_type.write(str)



print('\n'*3)
print('ALL TRIALS')
print('\n' + '-' * 150 + '\n' + '-' * 100)
print(tabulate(results_per_trial, headers='keys', tablefmt="fancy_grid", numalign="center"))
