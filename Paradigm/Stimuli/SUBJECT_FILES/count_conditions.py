import argparse
from pprint import pprint
import pandas as pd
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', default='Subj_1_dataset.txt')
parser.add_argument('-d', '--delim', default=',')
args = parser.parse_args()

viol_position = {}
viol_position['objrel_that'] = {}
viol_position['objrel_that'][1] = 4
viol_position['objrel_that'][2] = 5
viol_position['objrel_nounpp'] = {}
viol_position['objrel_nounpp'][1] = 7
viol_position['objrel_nounpp'][2] = 8
viol_position['embedding_mental_SR'] = {}
viol_position['embedding_mental_SR'][1] = 2
viol_position['embedding_mental_SR'][2] = 5
viol_position['embedding_mental'] = {}
viol_position['embedding_mental'][1] = 2
viol_position['embedding_mental'][2] = 7

with open(args.filename, 'r') as f:
    dataset = f.readlines()

dataset = dataset[1::] # remove first (header) line
sents = [s.split(args.delim)[0].strip() for s in dataset]
structs = [s.split(args.delim)[1].strip() for s in dataset]
conditions = [s.split(args.delim)[2].strip() for s in dataset]
slides = [int(s.split(args.delim)[3].strip()) for s in dataset]

struct_types = sorted(set(structs))
d = {s:{} for s in struct_types}
for i, (s, c, n) in enumerate(zip(structs, conditions, slides)):
    if c not in d[s].keys():
        d[s][c] = {}
        d[s][c]['correct'] = 0
        d[s][c]['viol'] = {}
        d[s][c]['viol']['V1'] = 0
        d[s][c]['viol']['V2'] = 0
        d[s][c]['viol']['filler'] = 0
    # Check if correct of violation trials
    if n == 0:
        d[s][c]['correct'] += 1
    else:
        # pos = None
        if n == viol_position[s][1]:
            # pos = 1
            d[s][c]['viol']['V1'] += 1
        elif n == viol_position[s][2]:
            # pos = 2
            d[s][c]['viol']['V2'] += 1
        else:
            d[s][c]['viol']['filler'] += 1
            # error_str = 'violation position must be one of the two possible values defined at the top of the script: %i, %s, %s' % (i, s, c)
            # print(error_str)
            # raise()
        # d[s][c]['viol'][pos]+=0


 # Print into tabulate
# -------------------
df = pd.DataFrame(columns=['structure', 'acceptable', 'V1_viol', 'V2_viol', 'filler_viol', 'Total'])
# print('-' * 50)
counts_dict = {}
cnt_total_v1, cnt_total_v2, cnt_total_filler, cnt_total_correct = [0, 0, 0, 0]
for s in sorted(d.keys()):
    cnt_correct, cnt_v1, cnt_v2, cnt_filler = [0, 0, 0, 0]
    for c in d[s].keys():
        cnt_correct += d[s][c]['correct']
        cnt_v1 += d[s][c]['viol']['V1']
        cnt_v2 += d[s][c]['viol']['V2']
        cnt_filler += d[s][c]['viol']['filler']
    cnt_total_correct += cnt_correct
    cnt_total_v1 += cnt_v1
    cnt_total_v2 += cnt_v2
    cnt_total_filler += cnt_filler
    cnt_total_struct = cnt_correct + cnt_v1 + cnt_v2 + cnt_filler
    df = df.append({'structure':s, 'acceptable':cnt_correct, 'V1_viol':cnt_v1, 'V2_viol':cnt_v2, 'filler_viol':cnt_filler, 'Total':cnt_total_struct}, ignore_index=True)

cnt_total_trials = cnt_total_correct + cnt_total_v1 + cnt_total_v2 + cnt_total_filler
df = df.append({'structure':'Total', 'acceptable':cnt_total_correct, 'V1_viol':cnt_total_v1, 'V2_viol':cnt_total_v2, 'filler_viol':cnt_total_filler, 'Total':cnt_total_trials}, ignore_index=True)
print(tabulate(df, headers='keys', tablefmt="fancy_grid", numalign="center"))
print('-'* 50)
pprint(d)


# print('%s (correct): %i' % (s, cnt_correct))
# print('%s (violations on inner verb): %i' % (s, cnt_v1))
# print('%s (violations on outer verb): %i' % (s, cnt_v2))
# print('%s (violations on filler): %i' % (s, cnt_filler))
# print('-' * 50)

# print('-'* 50)
# print('Total correct: %i' % cnt_total_correct)
# print('Total V1 violations: %i' % cnt_total_v1)
# print('Total V2 violations: %i' % cnt_total_v2)
# print('Total filler violations: %i' % cnt_total_filler)
# print('Total trials: %i' % cnt_total_trials)

# [print('%s - %s(correct): %i\n%s - %s(violation): %i\n%s - %s (total): %i\n------------------------'%(s, c, d[s][c]['correct'], s, c, d[s][c]['viol'], s, c, sum(d[s][c].values()))) for s in struct_types for c in sorted(d[s].keys())]
# [print('%s - %s(correct): %i\n%s - %s(violation): %i\n%s - %s (total): %i\n------------------------'%(s, c, d[s][c]['correct'], s, c, d[s][c]['viol'], s, c, sum(d[s][c].values()))) for s in struct_types for c in sorted(d[s].keys())]
# [print('%s: %i'%(s, sum(d[s].values()))) for s in struct_types ]

# df = df.sort_values(['structure'])




