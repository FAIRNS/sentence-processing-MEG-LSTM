import argparse, os
from numpy import percentile

def intersect(list, n):
    intersect_list = []
    items = set([x for l in list for x in l])
    for item in items:
        in_all = len(list)
        for l in list:
            if not item in l:
                in_all -= 1
        if in_all >= n:
            intersect_list.append(item)
    return  intersect_list

d_cond = {'S': 'singular', 'P':'plural'}
NA_tasks = ['nounpp', 'subjrel', 'objrel']

SP_units = []
PS_units = []
for NA_task in NA_tasks:
    for condition in ['SS', 'SP', 'PS', 'PP']:
        filename = '_'.join([NA_task, d_cond[condition[0]], d_cond[condition[1]], 'accuracies'])
        path2ablation_results = os.path.join('..', '..', '..', 'Output', 'ablation_italian_stats', filename)

        with open(path2ablation_results, 'r') as f:
            results = f.readlines()
        results = [l.strip('\n').split('\t') for l in results]
        units = [int(l[0][len(d_cond[condition[0]]):l[0].find('_')]) for l in results]
        accuracies = [float(l[3]) for l in results]

        th = percentile(accuracies, 2)
        units_above_th = [u for (u, a) in zip(units, accuracies) if a < th]
        print(NA_task, condition, units_above_th)

        if condition == 'SP':
            SP_units.append(units_above_th)
        elif condition == 'PS':
            PS_units.append(units_above_th)

SP_units = intersect(SP_units, 3)
PS_units = intersect(PS_units, 3)
print('SP units:', SP_units)
print('PS units:', PS_units)