import argparse
import os
import random

parser = argparse.ArgumentParser()

parser.add_argument('-k', help='sample_size', type=int, default=19)
parser.add_argument('-n_samples', help='number of samples', type=int, default=1000)
parser.add_argument('-base_folder', help='Location of folder sentence-processing-MEG-LSTM')

args = parser.parse_args()

base_folder = os.path.join(args.base_folder, 'sentence-processing-MEG-LSTM/')

script         = base_folder + 'Code/LSTM/model-analysis/ablation-experiment.py'
model          = base_folder + 'Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = base_folder + 'Data/agreement-data/colorlessgreenRNNs-master/data/linzen_testset/subj_agr_filtered'
vocab          = base_folder + 'Data/LSTM/english_vocab.txt'
output         = base_folder + 'Output/ablation_results_killing_unit_group_'
regression_units_fn=os.path.expanduser(base_folder + 'Output/num_open_nodes/Ridge_regression_number_of_open_nodes_n=300.txt')
eos = '"<eos>"'
format = 'pkl'

# units sorted by their regression weights
unit_to_kill_from = 1
unit_to_kill_to = 1300
sample_size = args.k
total_samples = args.n_samples

sample_regression_units = False # get syntax units from regression analysis and sample from them for the ablation exp
sample = True # sub-sample 'sample-size' (k) units from 'possible_killed_units' (either all-units/syntax-unit) for ablation exp

if sample_regression_units:
    regression_units = []
    with open(regression_units_fn, 'r') as f:
        for l in f.readlines():
            regression_units.append(int(l.rstrip().split(',')[1])+1) # !!!change from counting from 0 to counting from 1!!!
        # units = [int(u) for ]

# regression_units = list(map(lambda x: x+1, map(int, list(l for l in open(regression_units_fn))[:])))

if sample:
    if sample_regression_units:
        possible_killed_units = regression_units
    else:
        possible_killed_units = range(unit_to_kill_from, unit_to_kill_to+1)
else:
    units = range(unit_to_kill_from, unit_to_kill_to+1)

sampled_units = set()

for seed in range(1):
    random.seed(seed)
    g = 1 # group size of units to kill in including random ones

    unit_sets = []
    if sample:
        for _ in range(total_samples):
            if sample:
                units = None
                while units is None or units in sampled_units:
                    units = tuple(random.sample(possible_killed_units, sample_size))
                sampled_units.add(units)

                unit_sets.append(units)
    else:
        for u in units:
            unit_sets.append([u])

    for sg, units in enumerate(unit_sets):
        units = map(str, units)
        all_units = " -u ".join(units)
        output_fn = output + '%i_seed_%i_k_%i_units_%s' % (sg, seed, sample_size, '_'.join(units)) + '.pkl'
        cmd = 'python3 ' + script + " " + model + " --input " + agreement_data + " --vocabulary " + vocab + " --output " + output_fn + \
              " --eos-separator " + eos + " --format " + format + " -u " + all_units + " -g " \
              + str(g) + " -s " + str(seed) + " --cuda --use-unk"

        print(cmd)
