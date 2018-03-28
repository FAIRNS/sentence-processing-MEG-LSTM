import pickle
import numpy as np
<<<<<<< HEAD
from tqdm import tqdm

# Params
seeds = [0] #list(range(20))
groupsize = 1#10
units = list(range(1,1000+1))

# Paths
output = '/private/home/germank/projects/neurospin/sentence-processing-MEG-LSTM/Output/ablation-results/ablation_results_killing_unit_'
results_fn = '/private/home/germank/projects/neurospin/sentence-processing-MEG-LSTM/Output/ablation-results/ablation_results_all_units_{}'.format(groupsize)
=======

# Paths
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_'
results_fn = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_all_units'

# Params
seeds = [1]
groupsize = 1
units = [1,2]
>>>>>>> 785e2221a14e0c430a5b4cb64127e1753d1546fd

# init arrays
scores_diff = np.zeros((len(units), len(seeds)))
score_with_ablation = np.zeros((len(units), len(seeds)))
score_without_ablation = np.zeros((len(units), len(seeds)))

# Collect data from all units/seeds/ablation
<<<<<<< HEAD
for s, seed in enumerate(tqdm(seeds)):
    for u, unit in enumerate(tqdm(units)):
        output_fn = output + str(unit) + '_groupsize_' + str(groupsize) + '_seed_' + str(seed) # Update output file name
        for ablation in [False, True]:
            output_fn1 = output_fn + '_' + str(ablation) + '.pkl'  # output file name
            with open(output_fn1, 'rb') as fout:
=======
for s, seed in enumerate(seeds):
    for u, unit in enumerate(units):
        output_fn = output + str(unit) + '_groupsize_' + str(groupsize) + '_seed_' + str(seed) # Update output file name
        for ablation in [False, True]:
            output_fn1 = output_fn + '_' + str(ablation) + '.pkl'  # output file name
            with open(output_fn1, 'r') as fout:
>>>>>>> 785e2221a14e0c430a5b4cb64127e1753d1546fd
                results = pickle.load(fout)
            if not ablation: score_without_ablation[u, s] = results['score_on_task']
            if ablation: score_with_ablation[u, s] = results['score_on_task']
        scores_diff[u, s] = score_with_ablation[u, s] - score_without_ablation[u, s]

# Average across seeds and sort units in descending order
scores_diff_ave_across_seeds = np.mean(scores_diff, axis=1)
IX_units = (-scores_diff_ave_across_seeds).argsort() + 1 # add one to start counting from 1

# Save sorted units to text file
<<<<<<< HEAD
with open(results_fn + '.txt', 'w') as fout:
=======
with open(results_fn + '.txt', 'wb') as fout:
>>>>>>> 785e2221a14e0c430a5b4cb64127e1753d1546fd
    for unit in IX_units:
        fout.write("%s\n" % unit)

# Save collected results to pkl
out = {
    'units': units,
    'seeds': seeds,
    'groupsize': groupsize,
    'output_filename': output,
<<<<<<< HEAD
    'score_without_ablation': score_without_ablation,
    'score_with_ablation': score_with_ablation,
    'scores_diff': scores_diff,
    'IX_units': IX_units
}
from pprint import pprint
pprint(out)
=======
    'score_without_ablation': scores_diff,
    'score_with_ablation': scores_diff,
    'scores_diff': scores_diff,
    'IX_units': IX_units
}
>>>>>>> 785e2221a14e0c430a5b4cb64127e1753d1546fd

with open(results_fn + '.pkl', 'wb') as fout:
    pickle.dump(out, fout, -1)
