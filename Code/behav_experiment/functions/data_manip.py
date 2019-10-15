import os, glob
import pandas as pd
import numpy as np


def read_logs(args, valid_correct, valid_wrong):
    '''
    Load all logs from all selected subjects in args and generate a dataframe with all results
    :param args:
    :param valid_correct: (list) of strings 'CORRECT'/'CORRECT_INC'/'CORRECT_DDC'
    :param valid_wrong: (list)
    :return: df_all_trials (Pandas DataFrame)
    '''
    df_all_trials = []
    for subject, session in zip(args.subjects, args.sessions):
        base_fn = 'logLocalGlobalParadigm_*_Subj_%02d_sess_%i.csv' % (subject, session)
        fn = glob.glob(os.path.join(args.path2logs, base_fn))
        if len(fn) == 1:
            fn = fn[0]
        else:
            raise ('Log file was not found or subject file is repeated for several dates')

        with open(fn, 'r') as f_log:
            lines = f_log.readlines()

        for l in lines:
            fields = l.split('\t')
            if fields[0] == 'END_TRIAL':
                curr_dict = {}
                curr_dict['subject'] = subject
                curr_dict['block'] = fields[1]
                curr_dict['trial_num'] = fields[2]
                if fields[7] == 'objrel_that':
                    s_type = 'objrel'
                elif fields[7] == 'embedding_mental':
                    s_type = 'embedding_mental_LR'
                else:
                    s_type = fields[7]
                curr_dict['sentence_type'] = s_type
                curr_dict['condition'] = fields[8]
                curr_dict['violation_type'] = fields[10]
                curr_dict['slide_num_of_viol'] = int(fields[9])
                curr_dict['correct_wrong'] = fields[5]
                curr_dict['RT'] = fields[6]
                # Add trial_type based on slide sign
                if curr_dict['slide_num_of_viol'] > 0:
                    curr_dict['trial_type'] = 'Violation'
                elif curr_dict['slide_num_of_viol'] < 0:
                    curr_dict['trial_type'] = 'Filler'
                elif curr_dict['slide_num_of_viol'] == 0:
                    curr_dict['trial_type'] = 'Acceptable'
                # Add valid answer based on choice of valid_correct and wrong
                if curr_dict['correct_wrong'] in valid_correct:
                    curr_dict['valid_answer'] = 'CORRECT'
                elif curr_dict['correct_wrong'] in valid_wrong:
                    curr_dict['valid_answer'] = 'WRONG'
                else:
                    curr_dict['valid_answer'] = 'REJECTED'
                # Add violation position
                if (curr_dict['sentence_type'] in ['objrel', 'objrel_nounpp']) and (curr_dict['violation_type'] == 'V1'):
                    curr_dict['violation_position'] = 'inner'
                elif (curr_dict['sentence_type'] in ['objrel', 'objrel_nounpp']) and (curr_dict['violation_type'] == 'V2'):
                    curr_dict['violation_position'] = 'outer'
                elif (curr_dict['sentence_type'] in ['embedding_mental_SR', 'embedding_mental_LR']) and (curr_dict['violation_type'] == 'V2'):
                    curr_dict['violation_position'] = 'inner'
                else:
                    curr_dict['violation_position'] = 'other'

                df_all_trials.append(curr_dict)

    return pd.DataFrame(df_all_trials)


def get_error_rates(df_all_trials):
    df_error_rates = []
    for subject in df_all_trials.subject.unique():
        for sentence_type in df_all_trials.sentence_type.unique():
            for trial_type in df_all_trials.trial_type.unique():
                for violation_type in df_all_trials.violation_type.unique():
                    for condition in df_all_trials.loc[df_all_trials['sentence_type']==sentence_type].condition.unique():
                        curr_dict = {}
                        df_curr_condition = df_all_trials.loc[(df_all_trials['subject']==subject) & (df_all_trials['sentence_type']==sentence_type) & (df_all_trials['trial_type']==trial_type) & (df_all_trials['violation_type']==violation_type) & (df_all_trials['condition']==condition)]
                        num_trials = len(df_curr_condition)
                        num_errors = len(df_curr_condition.loc[(df_curr_condition['valid_answer']=='WRONG')])
                        if num_trials > 0:
                            curr_dict['error_rate'] = num_errors/num_trials
                        else:
                            curr_dict['error_rate'] = np.nan
                        curr_dict['subject'] = subject
                        curr_dict['sentence_type'] = sentence_type
                        curr_dict['trial_type'] = trial_type
                        curr_dict['violation_type'] = violation_type
                        curr_dict['condition'] = condition
                        # Add violation position
                        if (curr_dict['sentence_type'] in ['objrel', 'objrel_nounpp']) and (curr_dict['violation_type'] == 'V1'):
                            curr_dict['violation_position'] = 'inner'
                        elif (curr_dict['sentence_type'] in ['objrel', 'objrel_nounpp']) and (curr_dict['violation_type'] == 'V2'):
                            curr_dict['violation_position'] = 'outer'
                        elif (curr_dict['sentence_type'] in ['embedding_mental_SR', 'embedding_mental_LR']) and (curr_dict['violation_type'] == 'V2'):
                            curr_dict['violation_position'] = 'inner'
                        else:
                            curr_dict['violation_position'] = 'other'


                        df_error_rates.append(curr_dict)

    #         curr_subj_dict = {}
    #         curr_count_trials = {}
    #         for condition in conditions:
    #
    #             if trial_type in ['V1', 'V2']:
    #                 num_valid_correct_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_corrects and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and d['violation_type'] == trial_type and int(
    #                     d['slide_num_of_viol']) > 0)])
    #                 num_valid_wrong_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_wrongs and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and d['violation_type'] == trial_type and int(
    #                     d['slide_num_of_viol']) > 0)])
    #                 curr_count_trials[condition] = sum([1 for d in summary_all_trials if (
    #                         d['sentence_type'] == sentence_type and d['condition'] == condition and d[
    #                     'violation_type'] == trial_type and int(d['slide_num_of_viol']) > 0)])
    #             elif trial_type == 'acceptable':  # Nan is acceptable in logs
    #                 num_valid_correct_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_corrects and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and d['violation_type'] == 'NaN' and int(
    #                     d['slide_num_of_viol']) == 0)])
    #                 num_valid_wrong_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_wrongs and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and d['violation_type'] == 'NaN' and int(
    #                     d['slide_num_of_viol']) == 0)])
    #                 curr_count_trials[condition] = sum([1 for d in summary_all_trials if (
    #                         d['sentence_type'] == sentence_type and d['condition'] == condition and d[
    #                     'violation_type'] == 'NaN' and int(d['slide_num_of_viol']) == 0)])
    #             elif trial_type == 'filler':
    #                 num_valid_correct_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_corrects and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and int(d['slide_num_of_viol']) < 0)])
    #                 num_valid_wrong_responses = sum([1 for d in summary_all_trials if (
    #                         d['correct_wrong'] in valid_wrongs and d['sentence_type'] == sentence_type and d[
    #                     'condition'] == condition and int(d['slide_num_of_viol']) < 0)])
    #                 curr_count_trials[condition] = sum([1 for d in summary_all_trials if (
    #                         d['sentence_type'] == sentence_type and d['condition'] == condition and int(
    #                     d['slide_num_of_viol']) < 0)])
    #             else:
    #                 raise ('unknown trial type: %s' % trial_type)
    #
    #             num_valid_responses_total = num_valid_correct_responses + num_valid_wrong_responses
    #             if curr_count_trials[condition] > 0:
    #                 error_rate = num_valid_wrong_responses / curr_count_trials[condition]
    #
    #             else:
    #                 if not ('embedding_mental' in sentence_type and trial_type in ['V1', 'filler']):
    #                     print('number of trials from this condition is zero: %i, %s, %s, %s' % (
    #                         subject, sentence_type, trial_type, condition))
    #                     raise ()
    #                 pass
    #             # Store in dict
    #             curr_count_trials['subject'] = subject
    #             curr_subj_dict['subject'] = subject
    #             if num_valid_responses_total > 0:
    #                 curr_subj_dict[condition] = error_rate
    #             else:
    #                 curr_subj_dict[condition] = np.nan
    #
    #             dict_error_rate['subject'].append(subject)
    #             dict_error_rate['sentence_type'].append(sentence_type)
    #             dict_error_rate['violation_type'].append(trial_type)
    #             dict_error_rate['condition'].append(condition)
    #             dict_error_rate['error_rate'].append(error_rate)
    #
    #         dict_count_trials[sentence_type][trial_type].append(curr_count_trials)
    #         dict_per_struct_with_all_subject[sentence_type][trial_type].append(curr_subj_dict)
    #
    # # Append to subject list:
    # summary_all_trials_all_subject.extend(summary_all_trials)

    return pd.DataFrame(df_error_rates)
