import os, argparse, glob
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subjects', action='append', type=int, default=[0])
parser.add_argument('--sessions', action='append', type=int, default=[0])
parser.add_argument('--violation-type', default='V2')
parser.add_argument('--path2logs', default='../../Paradigm/Logs')
args = parser.parse_args()

violation_type = args.violation_type

if not args.sessions: # set default session 1 to all subjects
    args.sessions = [1 for _ in args.subjects]


error_rastes = [] # List of dicts (dict per subject)
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

    for l in lines:
        fields = l.split('\t')
        if fields[0] == 'END_TRIAL':
            curr_dict = {}
            curr_dict['subject'] = subject
            curr_dict['block'] = fields[1]
            curr_dict['trial_num'] = fields[2]
            curr_dict['sentence_type'] = fields[7]
            curr_dict['condition'] = fields[8]
            curr_dict['violation_type'] = fields[10]
            curr_dict['slide_num_of_viol'] = fields[9]
            curr_dict['correct_wrong'] = fields[5]
            curr_dict['RT'] = fields[6]
            summary_all_trials.append(curr_dict)

    #########################################
    #### CALC ERROR RATES FOR CURR SUBJ #####
    #########################################
    curr_subj_dict = {}
    for sentence_type in ['objrel_that', 'objrel_nounpp', 'embedding_mental', 'embedding_mental_SR']:
        conditions = list(set([d['condition'] for d in summary_all_trials if d['sentence_type']==sentence_type]))
        for condition in conditions:
            num_valid_correct_responses = sum([1 for d in summary_all_trials if (d['correct_wrong']=='CORRECT' and d['sentence_type']==sentence_type and d['condition']==condition and d['violation_type']==violation_type)])
            num_valid_wrong_responses = sum([1 for d in summary_all_trials if (d['correct_wrong'] == 'WRONG' and d['sentence_type']==sentence_type and d['condition']==condition and d['violation_type']==violation_type)])
            num_valid_responses_total = num_valid_correct_responses + num_valid_wrong_responses
            # Store in dict
            curr_subj_dict['subject'] = subject
            if num_valid_responses_total > 0:
                curr_subj_dict['%s-%s' % (sentence_type, condition)] = num_valid_wrong_responses/num_valid_responses_total
            else:
                curr_subj_dict['%s-%s' % (sentence_type, condition)] = 0
    error_rastes.append(curr_subj_dict)

results_per_trial = pd.DataFrame(summary_all_trials)
cols = ['subject', 'sentence_type', 'condition', 'violation_type', 'block', 'trial_num', 'correct_wrong', 'slide_num_of_viol', 'RT']
results_per_trial = results_per_trial[cols]
results_per_trial = results_per_trial.sort_values(['subject', 'sentence_type', 'condition', 'violation_type', 'block', 'trial_num'], ascending=[True, True, True, True, True, True])
print(results_per_trial)

results_per_subject = pd.DataFrame(error_rastes)
cols = ['subject', 'objrel_that-SS', 'objrel_that-SP', 'objrel_that-PS', 'objrel_that-PP', 'objrel_nounpp-SSS', 'objrel_nounpp-SSP', 'objrel_nounpp-SPS', 'objrel_nounpp-SPP', 'objrel_nounpp-PSS', 'objrel_nounpp-PSP', 'objrel_nounpp-PPS', 'objrel_nounpp-PPP', 'embedding_mental-SS', 'embedding_mental-SP', 'embedding_mental-PS', 'embedding_mental-PP', 'embedding_mental_SR-SSS', 'embedding_mental_SR-SSP', 'embedding_mental_SR-SPS', 'embedding_mental_SR-SPP', 'embedding_mental_SR-PSS', 'embedding_mental_SR-PSP', 'embedding_mental_SR-PPS', 'embedding_mental_SR-PPP']
results_per_subject = results_per_subject[cols]
# results = results_per_subject.sort_values(['subject', 'sentence_type', 'condition', 'violation_type', 'block', 'trial_num'], ascending=[True, True, True, True, True, True])
print(results_per_subject)


