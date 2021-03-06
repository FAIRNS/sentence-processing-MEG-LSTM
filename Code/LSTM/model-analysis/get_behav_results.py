import os
import numpy as np

# ------------------------------
# ---    ITALIAN     -----------
# ------------------------------
def get_behav_LSTM_italian():
    accuracy_LSTM_italian = {}
    # objrel_nounpp
    accuracy_LSTM_italian['objrel_nounpp'] = {}
    accuracy_LSTM_italian['objrel_nounpp']['SSS'] = 1.00
    accuracy_LSTM_italian['objrel_nounpp']['SSP'] = 0.99
    accuracy_LSTM_italian['objrel_nounpp']['SPS'] = 0.04
    accuracy_LSTM_italian['objrel_nounpp']['SPP'] = 0.12
    accuracy_LSTM_italian['objrel_nounpp']['PSS'] = 0.21
    accuracy_LSTM_italian['objrel_nounpp']['PSP'] = 0.04
    accuracy_LSTM_italian['objrel_nounpp']['PPS'] = 0.98
    accuracy_LSTM_italian['objrel_nounpp']['PPP'] = 1.00

    # objrel
    accuracy_LSTM_italian['objrel'] = {}
    accuracy_LSTM_italian['objrel']['SS'] = 1.00
    accuracy_LSTM_italian['objrel']['SP'] = 0.53
    accuracy_LSTM_italian['objrel']['PS'] = 0.64
    accuracy_LSTM_italian['objrel']['PP'] = 1.00

    # embedding_mental_LR
    accuracy_LSTM_italian['embedding_mental_LR'] = {}
    accuracy_LSTM_italian['embedding_mental_LR']['SSS'] = 1.00
    accuracy_LSTM_italian['embedding_mental_LR']['SSP'] = 0.98
    accuracy_LSTM_italian['embedding_mental_LR']['SPS'] = 0.92
    accuracy_LSTM_italian['embedding_mental_LR']['SPP'] = 0.99
    accuracy_LSTM_italian['embedding_mental_LR']['PSS'] = 1.00
    accuracy_LSTM_italian['embedding_mental_LR']['PSP'] = 0.99
    accuracy_LSTM_italian['embedding_mental_LR']['PPS'] = 0.93
    accuracy_LSTM_italian['embedding_mental_LR']['PPP'] = 0.99

    # embedding_mental_SR
    accuracy_LSTM_italian['embedding_mental_SR'] = {}
    accuracy_LSTM_italian['embedding_mental_SR']['SS'] = 1.00
    accuracy_LSTM_italian['embedding_mental_SR']['SP'] = 0.99
    accuracy_LSTM_italian['embedding_mental_SR']['PS'] = 1.00
    accuracy_LSTM_italian['embedding_mental_SR']['PP'] = 0.99

    # put accuracy and error rate in a single dict
    behav_LSTM_italian = {}
    behav_LSTM_italian['accuracy'] = accuracy_LSTM_italian.copy()
    # behav_LSTM_italian['error_rate'] = accuracy_LSTM_italian.copy()
    del accuracy_LSTM_italian
    # calc error_rate as 1-acc:
    behav_LSTM_italian['error_rate'] = {}
    for sentence_type in behav_LSTM_italian['accuracy'].keys():
        behav_LSTM_italian['error_rate'][sentence_type] = {}
        for cond in behav_LSTM_italian['accuracy'][sentence_type].keys():
            behav_LSTM_italian['error_rate'][sentence_type][cond] = 1 - behav_LSTM_italian['accuracy'][sentence_type][cond]
    return behav_LSTM_italian

def get_behav_human_italian(path2results='../../../Paradigm/Results', sentence_types=['objrel', 'objrel_nounpp', 'embedding_mental_SR', 'embedding_mental_LR']):
    behav_humans_italian = {}
    behav_humans_italian['error_rate'] = {}
    for sentence_type in sentence_types:
        behav_humans_italian['error_rate'][sentence_type] = {}
        fn = os.path.join(path2results, 'mean_error_rate_%s.behav_res' % sentence_type)
        with open(fn, 'r') as f_results:
            results = f_results.readlines()
        for l in results:
            cond, error_rate = l.strip('\n').split('\t')
            behav_humans_italian['error_rate'][sentence_type][cond.strip(' ')] =  float(error_rate)

    # calc accuracy as 1-error_rate:
    behav_humans_italian['accuracy'] = {}
    for sentence_type in behav_humans_italian['error_rate'].keys():
        behav_humans_italian['accuracy'][sentence_type] = {}
        for cond in behav_humans_italian['error_rate'][sentence_type].keys():
            behav_humans_italian['accuracy'][sentence_type][cond] = 1 - behav_humans_italian['error_rate'][sentence_type][cond]
    return behav_humans_italian



# diff_objrel_nounpp_SXS = perf_objrel_nounpp_SSS - perf_objrel_nounpp_SPS
# diff_objrel_nounpp_PXP = perf_objrel_nounpp_PPP - perf_objrel_nounpp_PSP

# diff_objrel_nounpp = np.mean([diff_objrel_nounpp_SXS, diff_objrel_nounpp_PXP])


# diff_objrel_nounpp_SX = perf_objrel_SS - perf_objrel_SP
# diff_objrel_nounpp_PX = perf_objrel_PP - perf_objrel_PS
# diff_objrel = np.mean([diff_objrel_nounpp_SX, diff_objrel_nounpp_PX])

# print(diff_objrel_nounpp, diff_objrel)

# diff_embedding_mental_LR_SXS = perf_embedding_mental_LR_SSS - perf_embedding_mental_LR_SPS
# diff_embedding_mental_LR_PXP = perf_embedding_mental_LR_PPP - perf_embedding_mental_LR_PSP
#
# diff_embedding_mental_LR = np.mean([diff_embedding_mental_LR_SXS, diff_embedding_mental_LR_PXP])


# diff_embedding_mental_SR_SX = perf_embedding_mental_SR_SS - perf_embedding_mental_SR_SP
# diff_embedding_mental_SR_PX = perf_embedding_mental_SR_PP - perf_embedding_mental_SR_PS
# diff_embedding_mental_SR = np.mean([diff_embedding_mental_SR_SX, diff_embedding_mental_SR_PX])

# print(diff_embedding_mental_LR, diff_embedding_mental_SR)
