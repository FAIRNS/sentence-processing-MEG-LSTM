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
    for subject in args.subjects:
        lines = []
        for sess in range(1, 3):
            base_fn = 'logLocalGlobalParadigm_*_Subj_%02d_sess_%i.csv' % (subject, sess)
            fn_session = glob.glob(os.path.join(args.path2logs, base_fn))
            if len(fn_session) == 1:
                with open(fn_session[0], 'r') as f_log:
                    lines.extend(f_log.readlines())
            else:
                print('subject %i, session %i:' % (subject, sess))
                raise ('Log file was not found or subject file is repeated for several dates')


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
                if curr_dict['condition'][0] == curr_dict['condition'][1]:
                    curr_dict['congruent_subjects'] = True
                else:
                    curr_dict['congruent_subjects'] = False
                if len(curr_dict['condition']) > 2:
                    if curr_dict['condition'][1] == curr_dict['condition'][2]:
                        curr_dict['congruent_attractor'] = True
                    else:
                        curr_dict['congruent_attractor'] = False
                    curr_dict['congruent_subjects_attractor'] = '_'.join(map(str, [curr_dict['congruent_subjects'], curr_dict['congruent_attractor']]))
                else:
                    curr_dict['congruent_attractor'] = np.nan
                    curr_dict['congruent_subjects_attractor'] = np.nan


                curr_dict['violation_type'] = fields[10]
                if curr_dict['violation_type'] == 'NaN':
                    curr_dict['violation_type'] = 'None'
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


def get_outlier_subjects(df):
    outlier_subjects = []
    df_performace_all_subjects = []
    easy_sentence_type = ['embedding_mental_SR', 'embedding_mental_LR']#, 'objrel', 'objrel_nounpp']
    easy_trial_type = ['Filler', 'Violation']
    violation_type = 'V2'
    for subject in df.subject.unique():
        print('Subject %i' % subject)
        # for trial_type in df.trial_type.unique():

            # for condition in df.loc[df['sentence_type']==easy_sentence_type].condition.unique():
        curr_dict = {}
        df_curr_condition = df.loc[(df['subject']==subject) & (df['sentence_type'].isin(easy_sentence_type)) & (df['trial_type'].isin(easy_trial_type)) & (df['violation_type']==violation_type)]
        num_trials = len(df_curr_condition)
        num_errors = len(df_curr_condition.loc[(df_curr_condition['valid_answer']=='WRONG')])
        if num_trials > 0:
            curr_dict['error_rate'] = num_errors/num_trials
        else:
            curr_dict['error_rate'] = np.nan
        curr_dict['subject'] = subject
        # curr_dict['trial_type'] = trial_type

        df_performace_all_subjects.append(curr_dict)
    df = pd.DataFrame(df_performace_all_subjects)

    import matplotlib.pyplot as plt
    import seaborn as sns
    fig, ax = plt.subplots(figsize=(10, 10))

    # df = df_error_rates.loc[
    #     (df_error_rates['sentence_type'] == s_type) & (df_error_rates['trial_type'] == 'Violation') & (
    #         df_error_rates['violation_position'].isin(['inner', 'outer']))]
    # df.hist(column='error_rate')#, by='trial_type')
    # sns.barplot(x='subject', y='error_rate', data=df, ax=ax)
    # ax.set_ylim([0, 1])
    # ax.set_ylabel('Error rate')
    # plt.tight_layout()
    # sns.distplot(df['error_rate'])
    # plt.show()

    q25, q75 = df.quantile(0.25)[0], df.quantile(0.75)[0]
    iqr = q75 - q25
    cut_off = iqr * 1.5
    upper = q75 + cut_off
    print('upper outlier threshold for error-rate:', upper)
    df_outliers = df.loc[(df['error_rate']>=upper)]

    return list(df_outliers['subject'])

def get_error_rates(df_all_trials):
    df_error_rates = []
    for subject in df_all_trials.subject.unique():
        print('Subject %i' % subject)
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
                        if curr_dict['condition'][0] == curr_dict['condition'][1]:
                            curr_dict['congruent_subjects'] = True
                        else:
                            curr_dict['congruent_subjects'] = False
                        if len(curr_dict['condition']) > 2:
                            if curr_dict['condition'][1] == curr_dict['condition'][2]:
                                curr_dict['congruent_attractor'] = True
                            else:
                                curr_dict['congruent_attractor'] = False
                            curr_dict['congruent_subjects_attractor'] = '_'.join(map(str, [curr_dict['congruent_subjects'], curr_dict['congruent_attractor']]))
                        else:
                            curr_dict['congruent_attractor'] = np.nan
                            curr_dict['congruent_subjects_attractor'] = np.nan
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

    return pd.DataFrame(df_error_rates)
