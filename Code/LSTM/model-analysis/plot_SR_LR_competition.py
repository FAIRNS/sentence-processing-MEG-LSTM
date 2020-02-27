import pickle, sys, os
import matplotlib.pyplot as plt
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Plot decompositoin to SR and LR contributions')
parser.add_argument('--path2stimuli', default='../../../Data/Stimuli/')
parser.add_argument('--path2output', default='../../../Output/')
parser.add_argument('--model', type=str, default='../../../Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt', help='pytorch model')
parser.add_argument('--input', default='nounpp', help='Filename without extension for Tal\'s setup (text, gold and info)')
parser.add_argument('--verbs', default='singular_plural_verbs.txt', help='Text file with two tab delimited columns with the lists of output words')
parser.add_argument('--vocabulary', default='../../../Data/LSTM/models/english/english_vocab.txt')
#parser.add_argument('--lr-units', default=[769, 987, 775], nargs='+', help='Long-range unit numbers - counting from ZERO!')
parser.add_argument('--lr-units', default=[987, 775], nargs='+', help='Long-range unit numbers - counting from ZERO!')
parser.add_argument('--sr-units', default=[1282, 1283, 772, 905, 1035, 1167, 1295, 655, 1042, 1171, 916, 661, 1052, 796, 925, 671, 1055, 1058, 1065, 681, 682, 684, 939, 1199, 1202, 1203, 950, 952, 1210, 699, 1214, 702, 831, 833, 714, 972, 847, 975, 978, 1235, 851, 853, 856, 857, 1115, 745, 1006, 1264, 884], nargs='+', help='Short-range unit numbers - counting from ZERO!')
parser.add_argument('--conditions', default=[], nargs='+', help='Short-range unit numbers - counting from ZERO!')
#parser.add_argument('-c', '--conditions', default=[['singular', 'singular'], ['singular', 'plural'], ['plural', 'singular'], ['plural', 'plural']], nargs='+', help='Short-range unit numbers - counting from ZERO!')
parser.add_argument('--save2', type=str, default=[], help='Path to output')
args = parser.parse_args()
print(args)

if not args.conditions:
    if args.input == 'nounpp':
        for n1 in ['singular', 'plural']:
            for n2 in ['singular', 'plural']:
                args.conditions.append([n1, n2])
        xlabels = ['Det', 'N1', 'P', 'Det', 'N2', 'V1', 'Det', 'N']
    elif 'English_objrel_nounpp_' in args.input:
        for n1 in ['singular', 'plural']:
            for n2 in ['singular', 'plural']:
                for n3 in ['singular', 'plural']:
                    args.conditions.append([n1, n2, n3])
        xlabels = ['Det', 'N1', 'that', 'det', 'N2', 'P', 'Det', 'N3', 'V2', 'V1', 'Det', 'N']
else:
    xlabels = []

print('Conditions: ', args.conditions)
print(xlabels)

fn = 'SR_LR_%s%s.pkl' % (os.path.basename(args.model), args.input)
decomposition = pickle.load(open(os.path.join(args.path2output, fn), 'rb'))


#plt.rc('text', usetex=True)

#with open('AUC_all_units.pkl', 'rb') as f:
#    scores_from_embeddings_per_unit = pickle.load(f)
#    scores = [float(s) for s in scores_from_embeddings_per_unit.values()]
#fig = plt.subplots(figsize=(10, 10))
#plt.hist(scores, 100)
#print(np.average(scores), np.std(scores))
# plt.show()


#with open('results.pkl', 'rb') as f:
#    results_dict_per_condition = pickle.load(f)



#conditions = ['singular_singular','singular_plural', 'plural_singular', 'plural_plural']
unit_types = ['LR', 'SR', 'others']
line_colors = ['g', 'r', 'b']
line_widths = [3, 3, 1]
line_styles = ['-', '-', '--']

unit_types = ['LR', 'SR']
line_colors = ['g', 'r']
line_widths = [3, 3]
line_styles = ['-', '-']


num_conditions = len(args.conditions)
d = int(np.ceil(np.sqrt(num_conditions)))
fig, axs = plt.subplots(d, d, figsize=(10, 10))
for c, cond in enumerate(args.conditions):
    cond = '_'.join(cond)
    for ut, unit_type in enumerate(unit_types):
        results = decomposition[cond][unit_type]
        e_results = [np.exp(1)**l for l in decomposition[cond][unit_type]]
        e_results = [np.log10(e) for e in e_results]
        cond_ave = np.average(e_results, axis=0)
        cond_std = np.std(e_results, axis=0)
        axs[c % d, int(np.floor(c / d))].errorbar(range(len(cond_ave)), cond_ave, yerr=cond_std, label=unit_type, lw=line_widths[ut], color=line_colors[ut], ls=line_styles[ut])
        axs[c % d, int(np.floor(c / d))].set_xticks(range(len(xlabels)))
        axs[c % d, int(np.floor(c / d))].set_xticklabels(xlabels, fontsize=12)
        #axs[c % d, int(np.floor(c / d))].set_title(cond.replace('_', '\_'), fontsize=14)
        title = ''.join([s[0].upper() for s in cond.split('_')])
        axs[c % d, int(np.floor(c / d))].set_title(title, fontsize=14)
        axs[c % d, int(np.floor(c / d))].set_ylim([-1, 1])
        axs[c % d, int(np.floor(c / d))].axhline(0, color='k', ls='--', lw=1)
        if c < d:
            axs[c % d, int(np.floor(c / d))].set_ylabel('$\\alpha_{correct/wrong}$', fontsize=30)

plt.legend(fontsize=30)
fname = 'SR_LR_interplay_%s.png' % (args.input)
plt.savefig(os.path.join('..', '..', '..', 'Figures', fname))
print('Figure saved to: ', os.path.join('..', '..', '..', 'Figures', fname)) 
