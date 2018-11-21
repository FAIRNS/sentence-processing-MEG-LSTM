import matplotlib.pyplot as plt
import numpy as np
import os

unigram_freq_filename = '../../../Data/Stimuli/nounpp_verb_unigram_freq.txt'
wrong_trials_filename = '../../../Data/Stimuli/wrong_nounpp.txt'
path2output_fig = '../../../Figures/scatter_singular_plural_verb_forms.png'


unigram_freqs = open(unigram_freq_filename, 'r').readlines()
wrong_trials = open(wrong_trials_filename, 'r').readlines()
all_problematic_verbs_SP = [l.split('\t')[1].split(' ')[-1] for l in wrong_trials if l.split('\t')[2] == 'singular' and l.split('\t')[3] == 'plural']
all_problematic_verbs_PS = [l.split('\t')[1].split(' ')[-1] for l in wrong_trials if l.split('\t')[2] == 'plural' and l.split('\t')[3] == 'singular']
problematic_verbs_SP = list(set(all_problematic_verbs_SP))
problematic_verbs_PS = list(set(all_problematic_verbs_PS))
number_of_occurence_of_prob_verb_SP = [all_problematic_verbs_SP.count(x) for x in problematic_verbs_SP]
number_of_occurence_of_prob_verb_PS = [all_problematic_verbs_PS.count(x) for x in problematic_verbs_PS]

verbs_form_1 = np.asarray([l.split('\t')[0] for l in unigram_freqs if len(l.split('\t'))==4])
verbs_freq_1 = np.asarray([int(l.split('\t')[1]) for l in unigram_freqs if len(l.split('\t'))==4])
verbs_form_2 =  np.asarray([l.split('\t')[2] for l in unigram_freqs if len(l.split('\t'))==4])
verbs_freq_2 = np.asarray([int(l.split('\t')[3]) for l in unigram_freqs if len(l.split('\t'))==4])
all_verb_pairs_freq = [[v1+'_'+v2, (f1, f2)] for (v1, v2, f1, f2) in zip(verbs_form_1, verbs_form_2, verbs_freq_1, verbs_freq_2) if v1[-1]=='s']
all_verb_pairs_freq = [list(x) for x in set(tuple(x) for x in all_verb_pairs_freq)]
pairs, freqs = zip(*all_verb_pairs_freq)
verbs_singular_freq, verbs_plural_freq = zip(*freqs)
pairs = list(pairs)

IX_problematic_singular = [True if v.split('_')[0] in problematic_verbs_SP else False for v in pairs]
IX_problematic_plural = [True if v.split('_')[1] in problematic_verbs_PS else False for v in pairs]

# Plot scatter
fig, ax = plt.subplots(1, figsize=(10, 10))
ax.scatter(verbs_singular_freq, verbs_plural_freq, s=1)
for i, pairs in enumerate(pairs):
    if IX_problematic_singular[i] and IX_problematic_plural[i]:
        ax.annotate(pairs, (verbs_singular_freq[i], verbs_plural_freq[i]), color='green')
    elif IX_problematic_plural[i]:
        ax.annotate(pairs.split('_')[1], (verbs_singular_freq[i], verbs_plural_freq[i]), color='blue')
    elif IX_problematic_singular[i]:
        ax.annotate(pairs.split('_')[0], (verbs_singular_freq[i], verbs_plural_freq[i]), color='red')
    else:
        ax.annotate(pairs, (verbs_singular_freq[i], verbs_plural_freq[i]), color='k')

# Cosmetics
ax.set_aspect('equal')
lims = [np.min([ax.get_xlim(), ax.get_ylim()]), np.max([ax.get_xlim(), ax.get_ylim()])]
ax.plot(lims, lims, 'k--', alpha=0.3, zorder=0)
ax.set_xlabel('Singular frequency', fontsize=20)
ax.set_ylabel('Plural frequency', fontsize=20)
fig.savefig(path2output_fig)
plt.close(fig)

# Distance from diagonal
freqs_SP = []
for v in problematic_verbs_SP:
    for (p, fs) in all_verb_pairs_freq:
        if p.find(v)>=0:
            freqs_SP.append(fs)
dist_from_y_eq_x = np.asarray([np.abs(x-y)/np.sqrt(2) for (x, y) in freqs_SP])
fig, ax = plt.subplots(1, figsize=(10, 10))
ax.scatter(number_of_occurence_of_prob_verb_SP, dist_from_y_eq_x)
for i, (n, d) in enumerate(zip(number_of_occurence_of_prob_verb_SP, dist_from_y_eq_x)):
    ax.annotate(problematic_verbs_SP[i], (n, d))
# Fit with polyfit
x = np.asarray(number_of_occurence_of_prob_verb_SP)
y = dist_from_y_eq_x
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
ax.plot(number_of_occurence_of_prob_verb_SP, intercept + slope * x, 'k:', alpha=0.3)
# Cosmetics
ax.set_xlabel('Occurence rate in error trials', fontsize=20)
ax.set_ylabel('Plural-Singualr bias', fontsize=20)
ax.annotate('rho = %1.2f' % r_value, (15, 1500), color='b')
folder_name, filename_fig = os.path.split(path2output_fig)
fig.savefig(os.path.join(folder_name, 'scatter_bias_vs_ocurrence_rate_SP.png'))
plt.close(fig)

# PS
freqs_PS = []
for v in problematic_verbs_PS:
    for (p, fs) in all_verb_pairs_freq:
        if p.find(v)>=0:
            freqs_PS.append(fs)

dist_from_y_eq_x = np.asarray([np.abs(x-y)/np.sqrt(2) for (x, y) in freqs_PS])
fig, ax = plt.subplots(1, figsize=(10, 10))
ax.scatter(number_of_occurence_of_prob_verb_PS, dist_from_y_eq_x)
for i, (n, d) in enumerate(zip(number_of_occurence_of_prob_verb_PS, dist_from_y_eq_x)):
    ax.annotate(problematic_verbs_PS[i], (n, d))
# Fit with polyfit
x = np.asarray(number_of_occurence_of_prob_verb_PS)
y = dist_from_y_eq_x
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
ax.plot(number_of_occurence_of_prob_verb_PS, intercept + slope * x, 'k:', alpha=0.3)
# Cosmetics
ax.set_xlabel('Occurence rate in error trials', fontsize=20)
ax.set_ylabel('Plural-Singualr bias', fontsize=20)
ax.annotate('rho = %1.2f' % r_value, (15, 1500), color='b')
folder_name, filename_fig = os.path.split(path2output_fig)
fig.savefig(os.path.join(folder_name, 'scatter_bias_vs_ocurrence_rate_PS.png'))
plt.close(fig)
