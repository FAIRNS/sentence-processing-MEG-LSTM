import os, glob, pickle
import numpy as np

num_trials_per_condition = 1000
num_units = 1300
acc_thres = 0.85
path2results = '../../../Output/ablation_outputs'
path2task = '../../../Data/Stimuli'
fn_task = 'Italian_nounpp_4000.txt'
with open(os.path.join(path2task, fn_task), 'r') as f:
    task = f.readlines()
    N1s = [l.split('\t')[3] for l in task]
    N2s = [l.split('\t')[5] for l in task]

fns = glob.glob(os.path.join(path2results, '*.abl'))


dict_results = {}
for fn in sorted(fns):
    str = os.path.basename(fn).split('Italian_nounpp_4000')
    train_seed = str[0]
    str = str[1].split('_')
    unit = int(str[0])

    print(train_seed, unit)
    try:
        curr_data = pickle.load(open(fn, 'rb'))
    except:
        print('pickle data corrupted for %s' % fn)

    results_curr_model = {}
    for N1 in ['singular', 'plural']:
        results_curr_model[N1] = {}
        for N2 in ['singular', 'plural']:
            results_curr_model[N1][N2] = {}
            for measure in ['accuracy', 'log_p_diff', 'normalized_p_diff']:
                results_curr_model[N1][N2][measure] = []
    for N1, N2, p_correct, p_wrong in zip(N1s, N2s, curr_data['log_p_targets_correct'], curr_data['log_p_targets_wrong']):
        results_curr_model[N1][N2]['accuracy'].append(int(p_correct>p_wrong))
        results_curr_model[N1][N2]['log_p_diff'].append(p_correct-p_wrong)
        results_curr_model[N1][N2]['normalized_p_diff'].append(np.exp(p_correct)/(np.exp(p_correct)+np.exp(p_wrong)))
    
    if train_seed not in dict_results.keys():
        dict_results[train_seed] = {}
    if unit not in dict_results[train_seed].keys():
        dict_results[train_seed][unit] = {}

    for N1 in ['singular', 'plural']:
        for N2 in ['singular', 'plural']:
            assert num_trials_per_condition == len(results_curr_model[N1][N2]['accuracy']) == len(results_curr_model[N1][N2]['log_p_diff'])
            condition = N1[0].upper() + N2[0].upper() # SS/SP/PS/PP
            dict_results[train_seed][unit][condition] = {} 
            dict_results[train_seed][unit][condition]['accuracy'] = sum(results_curr_model[N1][N2]['accuracy']) / num_trials_per_condition
            dict_results[train_seed][unit][condition]['log_p_diff'] = sum(results_curr_model[N1][N2]['log_p_diff']) / num_trials_per_condition
            dict_results[train_seed][unit][condition]['normalized_p_diff'] = sum(results_curr_model[N1][N2]['normalized_p_diff']) / num_trials_per_condition

with open('dict_ablation_results.pkl', 'wb') as f:
    pickle.dump(dict_results, f)

#print(dict_results)
for seed in dict_results.keys():
    units = dict_results[seed].keys()
    if len(units) == num_units:
        LR_units_S = [u for u in units if dict_results[seed][u]['SP']['accuracy'] < acc_thres]
        LR_units_P = [u for u in units if dict_results[seed][u]['PS']['accuracy'] < acc_thres]
        num_LR_units = len(set(LR_units_S+LR_units_P))
        print('Model %s: num_LR_units=%i, LR-units - S: %s, P: %s' % (seed, num_LR_units, LR_units_S, LR_units_P))
        for u in LR_units_S:
            print('%i, %1.2f' % (u, dict_results[seed][u]['SP']['accuracy']))
        for u in LR_units_P:
            print('%i, %1.2f' % (u, dict_results[seed][u]['PS']['accuracy']))
    else:
        print('Not all unit ablations exist for model %s (%i)' % (seed, len(units)))


