
import pickle, sys, os
import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
# plt.rc('font', family='serif')

with open('AUC_all_units.pkl', 'rb') as f:
    scores_from_embeddings_per_unit = pickle.load(f)
    scores = [float(s) for s in scores_from_embeddings_per_unit.values()]
fig = plt.subplots(figsize=(10, 10))
plt.hist(scores, 100)
print(np.average(scores), np.std(scores))
# plt.show()


with open('results.pkl', 'rb') as f:
    results_dict_per_condition = pickle.load(f)


fig, axs = plt.subplots(2, 2, figsize=(10, 10))
fname = 'SR_LR_interplay_nounpp.png'

xlabels = ['Det', 'N1', 'P', 'Det', 'N2', 'V1', 'Det', 'N']
conditions = ['singular_singular','singular_plural', 'plural_singular', 'plural_plural']
unit_types = ['LR', 'SR', 'others']
line_colors = ['g', 'r', 'b']
line_widths = [3, 3, 1]
line_styles = ['-', '-', '--']

unit_types = ['LR', 'SR']
line_colors = ['g', 'r']
line_widths = [3, 3]
line_styles = ['-', '-']

for c, cond in enumerate(conditions):
    for ut, unit_type in enumerate(unit_types):
        results = results_dict_per_condition[cond][unit_type]
        e_results = [np.exp(1)**l for l in results_dict_per_condition[cond][unit_type]]
        e_results = [np.log10(e) for e in e_results]
        cond_ave = np.average(e_results, axis=0)
        cond_std = np.std(e_results, axis=0)
        axs[c%2, int(np.floor(c/2))].errorbar(range(len(cond_ave)), cond_ave, yerr=cond_std, label=unit_type, lw=line_widths[ut], color=line_colors[ut], ls=line_styles[ut])
        axs[c % 2, int(np.floor(c / 2))].set_xticks(range(len(xlabels)))
        axs[c % 2, int(np.floor(c / 2))].set_xticklabels(xlabels, fontsize=18)
        axs[c % 2, int(np.floor(c / 2))].set_title(cond.replace('_', '\_'), fontsize=30)
        axs[c % 2, int(np.floor(c / 2))].set_ylim([-1, 1])
        axs[c % 2, int(np.floor(c / 2))].axhline(0, color='k', ls='--', lw=1)
        if c < 2:
            axs[c % 2, int(np.floor(c / 2))].set_ylabel('$\\alpha_{correct/wrong}$', fontsize=30)

plt.legend(fontsize=30)
plt.savefig(os.path.join('..', '..', '..', 'Figures', fname))
