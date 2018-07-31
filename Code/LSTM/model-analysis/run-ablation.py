# Paths
import random
import os.path
script = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py"
model = "/checkpoint/germank/neurospin/data/trained-english-models/hidden650_batch128_dropout0.2_lr20.0.pt"
#agreement_data = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Data/agreement-data/subj_agr_filtered"
agreement_data = "/private/home/germank/projects/neurospin/shared-data/agreement/marco-relative_clauses/temp_adv_sentences_for_german"
vocab = "$HOME/projects/neurospin/data/trained-english-models/vocab.txt"
sample_size = 19
#output = "$HOME/projects/neurospin/shared-data/ablation/random_units_{}/ablation_results_killing_unit_".format(sample_size)
output = "$HOME/projects/neurospin/shared-data/ablation/temp_adv_sentences_for_german/ablation_results_killing_unit_"
# units sorted by their regression weights
regression_units_fn=os.path.expanduser('~/projects/neurospin/shared-data/ablation/regression-weights.txt')
eos = '"<eos>"'
format = 'pkl'
unit_to_kill_from = 1
unit_to_kill_to = 1300
total_samples = 1000
regression_units = list(map(lambda x: x+1, map(int, list(l for l in open(regression_units_fn))[:])))
sample = False
if sample:
    sample_regression_units = False
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

    for units in unit_sets:
        units = map(str, units)
        cmd = "$HOME/.conda/envs/localconda/bin/python " + script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                            ' --eos-separator ' + eos + ' --format ' + format +  ' -u ' + ' -u ' .join(units) + ' -g '\
              + str(g) + ' -s ' + str(seed) + ' --cuda --use-unk'
        print(cmd)
