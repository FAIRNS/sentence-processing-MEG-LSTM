import os, glob, pickle

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

    acc_SP = []
    acc_PS = []
    acc_SS = []
    acc_PP = []
    for N1, N2, p_correct, p_wrong in zip(N1s, N2s, curr_data['log_p_targets_correct'], curr_data['log_p_targets_wrong']):
        if (N1 == 'singular') and (N2 == 'plural'):
            if p_correct > p_wrong:
                acc_SP.append(1)
            else:
                acc_SP.append(0)
        elif (N1 == 'plural') and N2 == ('singular'):
            if p_correct > p_wrong:
                acc_PS.append(1)
            else:
                acc_PS.append(0)
        elif (N1 == 'singular') and N2 == ('singular'):
            if p_correct > p_wrong:
                acc_SS.append(1)
            else:
                acc_SS.append(0)
        elif (N1 == 'plural') and N2 == ('plural'):
            if p_correct > p_wrong:
                acc_PP.append(1)
            else:
                acc_PP.append(0)
    if train_seed not in dict_results.keys():
        dict_results[train_seed] = {}
    if unit not in dict_results[train_seed].keys():
        dict_results[train_seed][unit] = {}

    assert num_trials_per_condition == len(acc_SP) == len(acc_PS) == len(acc_SS) == len(acc_PP)
    dict_results[train_seed][unit]['SP'] = sum(acc_SP) / num_trials_per_condition
    dict_results[train_seed][unit]['PS'] = sum(acc_PS) / num_trials_per_condition
    dict_results[train_seed][unit]['SS'] = sum(acc_SS) / num_trials_per_condition
    dict_results[train_seed][unit]['PP'] = sum(acc_PP) / num_trials_per_condition

with open('dict_ablation_results.pkl', 'wb') as f:
    pickle.dump(dict_results, f)

#print(dict_results)
for seed in dict_results.keys():
    units = dict_results[seed].keys()
    if len(units) == num_units:
        LR_units_S = [u for u in units if dict_results[seed][u]['SP'] < acc_thres]
        LR_units_P = [u for u in units if dict_results[seed][u]['PS'] < acc_thres]
        num_LR_units = len(set(LR_units_S+LR_units_P))
        print('Model %s: num_LR_units=%i, LR-units - S: %s, P: %s' % (seed, num_LR_units, LR_units_S, LR_units_P))
        for u in LR_units_S:
            print('%i, %1.2f' % (u, dict_results[seed][u]['SP']))
        for u in LR_units_P:
            print('%i, %1.2f' % (u, dict_results[seed][u]['PS']))
    else:
        print('Not all unit ablations exist for model %s (%i)' % (seed, len(units)))


