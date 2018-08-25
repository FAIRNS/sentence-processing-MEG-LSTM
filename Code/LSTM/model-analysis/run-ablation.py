# Paths
import random
import os.path
# script = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py"
# model = "/checkpoint/germank/neurospin/data/trained-english-models/hidden650_batch128_dropout0.2_lr20.0.pt"
# #agreement_data = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Data/agreement-data/subj_agr_filtered"
# agreement_data = "/private/home/germank/projects/neurospin/shared-data/agreement/marco-relative_clauses/temp_adv_sentences_for_german"
# vocab = "$HOME/projects/neurospin/data/trained-english-models/vocab.txt"
# sample_size = 19
# #output = "$HOME/projects/neurospin/shared-data/ablation/random_units_{}/ablation_results_killing_unit_".format(sample_size)
# output = "$HOME/projects/neurospin/shared-data/ablation/temp_adv_sentences_for_german/ablation_results_killing_unit_"
# # units sorted by their regression weights
# regression_units_fn=os.path.expanduser('~/projects/neurospin/shared-data/ablation/regression-weights.txt')
# eos = '"<eos>"'
# format = 'pkl'
# unit_to_kill_from = 1
# unit_to_kill_to = 1300
# total_samples = 1000

base_folder = '/home/yl254115/Projects/'
base_folder = '/neurospin/unicog/protocols/intracranial/'

script         = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py'
model          = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/colorlessgreenRNNs-master/data/linzen_testset/subj_agr_filtered'
vocab          = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output         = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_group_'
regression_units_fn=os.path.expanduser(base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Output/num_open_nodes/Ridge_regression_number_of_open_nodes_n=300.txt')
eos = '"<eos>"'
format = 'pkl'

# units sorted by their regression weights
unit_to_kill_from = 1
unit_to_kill_to = 1300
sample_size = 19
total_samples = 1000

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
        output_fn = output + '%i_seed_%i' % (sg, seed) + '.pkl'
        units = map(str, units)
        # cmd = "$HOME/.conda/envs/localconda/bin/python " + script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output +\
        #                     ' --eos-separator ' + eos + ' --format ' + format +  ' -u ' + ' -u ' .join(units) + ' -g '\
        #       + str(g) + ' -s ' + str(seed) + ' --cuda --use-unk'

        cmd = 'python3 ' + script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output_fn + \
              ' --eos-separator ' + eos + ' --format ' + format + ' -u ' + ' -u '.join(units) + ' -g ' \
              + str(g) + ' -s ' + str(seed) + ' --cuda --use-unk'

        print(cmd)