#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
import argparse
import math
import numpy as np
import pickle
import matplotlib.pyplot as plt
import sys
import os
import scipy.stats
import operator 

from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('vectors')
    ap.add_argument('info')
    ap.add_argument('--group', default='structure')
    ap.add_argument('-o', '--output', required=True, help='Directory where to '
            'output the figures')

    args = ap.parse_args()

    print('Loading data...')
    vectors = np.load(args.vectors)
    nhid = 1000
    plot_vectors = {}
    for name in ['gates.in', 'gates.out', 'gates.forget', 'gates.c_tilde']:
        plot_vectors[name] = vectors[name]
    plot_vectors['hidden'] = vectors['vectors'][:,:nhid,:]
    plot_vectors['cell'] = vectors['vectors'][:,nhid:,:]

    info = pickle.load(open(args.info, 'rb'))
    # get the indexes of the trials for each class
    class_indexes = defaultdict(list)
    for i,t in enumerate(info):
        class_indexes[t[args.group]].append(i)

    group_labels = {'structure':  {2: "2-6", 1: "4-4", 3: "6-2"}}

    os.makedirs(args.output, exist_ok=True)
    print('Plotting...')
    pvalues = {}
    for u in range(nhid):
        sys.stdout.write('{}\r'.format(u))
        pvalues[u] = plot({k: v[:,u,:] for k,v in plot_vectors.items()}, class_indexes, 
                group_labels[args.group], os.path.join(args.output, '{}.svg'.format(u)))

    with open('{}/pvalues.txt'.format(args.output), 'w') as f:
        for x,p in sorted(pvalues.items(), key=operator.itemgetter(1)):
            f.write("{}\t{}\n".format(x,p))
    print()

def plot(unit_activations,  class_indexes, class_labels, output):
    plt.figure(figsize=(12,8))
    min_pvalue = 1
    for i,(name, activations) in enumerate(unit_activations.items()):
        plt.subplot(231+i)
        plt.title(name)
        for c, cidx in sorted(class_indexes.items(), key=lambda t: class_labels[t[0]]):
            _,caps,_ = plt.errorbar(np.arange(8), activations[cidx].mean(0), yerr=activations[cidx].std(0), label='{}'.format(class_labels[c]), capsize=10, elinewidth=1)
            for cap in caps:
                cap.set_markeredgewidth(2)
        for x in range(8):
            stat = scipy.stats.f_oneway(*[activations[cidx][:,x] for c,cidx in class_indexes.items()]).statistic  
            stat = abs(math.log(stat))
            if stat > min_pvalue:
                min_pvalue = stat
        plt.legend()
        plt.tight_layout()
    print(min_pvalue)
    plt.savefig(output)
    plt.clf()
    plt.close()
    return min_pvalue
main()

