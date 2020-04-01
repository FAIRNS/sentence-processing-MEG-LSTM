import matplotlib.pyplot as plt

path2results = '/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Pipeline/Italian_nounpp_results_19_models'

with open(path2results, 'r') as f:
    lines = f.readlines()

dict_results = {}
for l in lines:
    if l.startswith('Number-agreement'):
        curr_seed = int(l.split()[-1])
        dict_results[curr_seed] = {}
    if l.startswith('[['):
        fields = l.split("'")
        N1 = fields[3]
        N2 = fields[7]
        curr_cond = '%s%s' % (N1[0], N2[0])
    if l.startswith('0') or l.startswith('1'):
        dict_results[curr_seed][curr_cond] = float(l)

fig, ax = plt.subplots()
for s in dict_results.keys():
    sp = dict_results[s]['sp']
    ps = dict_results[s]['ps']
    ax.scatter(sp, ps, c='b')
ax.plot([0, 1], [0, 1], 'k-', alpha=0.75, zorder=0)
ax.set_aspect('equal')
ax.set_xlim([0.89, 1])
ax.set_ylim([0.89, 1])
ax.set_xlabel('SP', fontsize=14)
ax.set_ylabel('PS', fontsize=14)

plt.show()
