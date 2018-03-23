import pickle
import numpy as np

# Paths
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_'
results_fn = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_all_units'

# Params
seeds = [1]
groupsize = 1
units = [1,2]

# init arrays
scores_diff = np.zeros((len(units), len(seeds)))
score_with_ablation = np.zeros((len(units), len(seeds)))
score_without_ablation = np.zeros((len(units), len(seeds)))

# Collect data from all units/seeds/ablation
for s, seed in enumerate(seeds):
    for u, unit in enumerate(units):
        output_fn = output + str(unit) + '_groupsize_' + str(groupsize) + '_seed_' + str(seed) # Update output file name
        for ablation in [False, True]:
            output_fn1 = output_fn + '_' + str(ablation) + '.pkl'  # output file name
            with open(output_fn1, 'r') as fout:
                results = pickle.load(fout)
            if not ablation: score_without_ablation[u, s] = results['score_on_task']
            if ablation: score_with_ablation[u, s] = results['score_on_task']
        scores_diff[u, s] = score_with_ablation[u, s] - score_without_ablation[u, s]

# Average across seeds and sort units in descending order
scores_diff_ave_across_seeds = np.mean(scores_diff, axis=1)
IX_units = (-scores_diff_ave_across_seeds).argsort() + 1 # add one to start counting from 1

# Save sorted units to text file
with open(results_fn + '.txt', 'wb') as fout:
    for unit in IX_units:
        fout.write("%s\n" % unit)

# Save collected results to pkl
out = {
    'units': units,
    'seeds': seeds,
    'groupsize': groupsize,
    'output_filename': output,
    'score_without_ablation': scores_diff,
    'score_with_ablation': scores_diff,
    'scores_diff': scores_diff,
    'IX_units': IX_units
}

with open(results_fn + '.pkl', 'wb') as fout:
    pickle.dump(out, fout, -1)
