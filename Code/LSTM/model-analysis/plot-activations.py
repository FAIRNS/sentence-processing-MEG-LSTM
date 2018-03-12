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
import random
import operator 
import pickle

from collections import defaultdict


def main():
    ap = argparse.ArgumentParser(description="""
    Takes the network activations for a set of sentences and a reference gold
    standard description of these sentences and produces plots relating 
    individual units to the data in the gold standard.
    """)
    ap.add_argument('vectors')
    ap.add_argument('reference')
    ap.add_argument('-t', '--analysis-type', required=True, choices=[
        'categories', 'correlation'])
    ap.add_argument('-g', '--group', default='structure', help=
            'Field of the gold-standard reference file to be used in plots')
    ap.add_argument('-o', '--output', required=True, help='Directory where to '
            'output the figures')

    args = ap.parse_args()

    print('Loading data...')
    if args.vectors.endswith('npz'):
        vectors = np.load(args.vectors, 'r')
    elif args.vectors.endswith('pkl'):
        vectors = pickle.load(open(args.vectors, 'rb'))
    nhid = int(vectors['vectors'][0].shape[0] / 2)
    plot_vectors = {}
    for name in ['gates.in', 'gates.out', 'gates.forget', 'gates.c_tilde']:
        plot_vectors[name] = vectors[name]
    if isinstance(vectors['vectors'], list):
        plot_vectors['hidden'] = [v[:nhid, :] for v in vectors['vectors']]
        plot_vectors['cell'] = [v[nhid:, :] for v in vectors['vectors']]
    else:
        plot_vectors['hidden'] = vectors['vectors'][:,:nhid,:]
        plot_vectors['cell'] = vectors['vectors'][:,nhid:,:]

    reference = pickle.load(open(args.reference, 'rb'))

    if args.analysis_type ==  'categories':
        class_indexes = defaultdict(list)
        # get the indexes of the trials for each class
        for i,t in enumerate(reference):
            class_indexes[t[args.group]].append(i)

        group_labels = {'structure':  {2: "2-6", 1: "4-4", 3: "6-2"}}
    elif args.analysis_type == 'correlation':
        series = []
        plot_vectors_series = defaultdict(list)
        for i,t in enumerate(reference):
            # remove void entries, the first one (always the same) and the last one (change of sentence confound)
            content = np.array([[j,x] for j,x in enumerate(t[args.group][1:-1]) if x != "-"])
            assert len(vectors['sentences'][i]) == len(next(iter(t.values())))
            # we only use sentences of a given max length and having
            # a series with a minimum length, and there must be SOME variability
            if len(t[args.group]) < 60 and len(t[args.group]) > 10 and content.shape[0] > 1 and not (content[:,1] == content[0,1]).all():
                valid_idxs = content[:,0].astype(np.int)
                series.append(content[:,1])
                for k, v in plot_vectors.items():
                    plot_vectors_series[k].append(v[i][:,valid_idxs])
        #series = np.concatenate(series)
        # for k,v in plot_vectors_series.items():
        #     plot_vectors_series[k] = np.concatenate(v, 1)

    os.makedirs(args.output, exist_ok=True)
    print('Computting statistics...')
    mean_correlations = {}
    for i,(name, activations) in enumerate(plot_vectors_series.items()):
        print(name, len(activations), activations[0].shape)
        mean_correlations[name] = get_mean_correlation(activations, series)
    statistic = get_max_correlation(mean_correlations)
    sorted_statistics = (-np.abs(statistic[0])).argsort()
    with open('{}/statistic.txt'.format(args.output), 'w') as f:
        for i in sorted_statistics:
            f.write("{}\t{:.2f} +- {:.2f}\t{:.2f}\n".format(i,statistic[0][i], statistic[1][i], statistic[-1][i]))
    # get the units with the largest r^2
    units = sorted_statistics[:25]
    print('Plotting...')
    for u in units:
        sys.stdout.write('{:d}\n'.format(u))
        if args.analysis_type == 'categories':
            statistic[u] = plot_categorical({k: v[:,u,:] for k,v in plot_vectors.items()}, class_indexes, 
                    group_labels[args.group], os.path.join(args.output, '{}.svg'.format(u)))
        elif args.analysis_type == 'correlation':
            plot_correlation({k: [v2[u, :] for v2 in v] for k,v in plot_vectors_series.items()}, series, 
                    {k: (v[0][u],v[1][u],v[2][u]) for k, v in mean_correlations.items()},
                    os.path.join(args.output, '{}.png'.format(u)))

    print()


def is_series_acceptable(xs):
    return len([x for x in xs if x!="-"]) > 1


def plot_categorical(unit_activations, class_indexes, class_labels, output):
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

def get_max_correlation(mean_correlations):
    '''
    takes a dictionary of names -> statistics and returns
    the statistics with the maximum value across names
    '''
    name_max = []
    for j in range(next(iter(mean_correlations.values()))[0].shape[0]):
        max_rho = None
        max_name = None
        for i,(name, correlations) in enumerate(mean_correlations.items()):
            rho = np.abs(correlations[0][j])
            if max_rho is None or rho >  max_rho:
                max_rho = rho
                max_name = name
        name_max.append(max_name)
    max_vals = []
    for j,name in enumerate(name_max):
        max_vals.append([s[j] for s in mean_correlations[name]])
    t_max_vals = tuple(np.array(s) for s in zip(*max_vals))
    return t_max_vals

def vcorrcoef(X,y):
    Xm = np.reshape(np.mean(X,axis=1),(X.shape[0],1))
    ym = np.mean(y)
    r_num = np.sum((X-Xm)*(y-ym),axis=1)
    r_den = np.sqrt(np.sum((X-Xm)**2,axis=1)*np.sum((y-ym)**2))
    r = r_num/r_den
    return r

def get_mean_correlation(activations, target_series):
    rs = []
    print("Computing mean correlation..")
    idxs = list(range(len(activations)))
    random.shuffle(idxs)
    idxs = idxs[:1000]
    approach = 1

    # just concatenating pearson approach
    pearsonr = vcorrcoef(np.concatenate(activations, axis=1), np.concatenate(target_series, axis=0))
    if approach == 1:
        stat = pearsonr
    # mean of spearmanr correlations
    elif approach == 2:
        for k,i in enumerate(idxs):
            sys.stdout.write("Sentence {} / {} ({:.0f}% complete)\r".format(k, len(idxs), k/len(idxs)*100))
            r = np.zeros(activations[i].shape[0]) 
            for j in range(r.shape[0]):
                r[j], p = scipy.stats.spearmanr(activations[i][j], target_series[i])
            rs.append(r)
        stat = np.mean(rs, axis=0)
    # mean of pearson correlations
    elif approach ==3:
        for k,i in enumerate(idxs):
            sys.stdout.write("Sentence {} / {} ({:.0f}% complete)\r".format(k, len(idxs), k/len(idxs)*100))
            r = vcorrcoef(activations[i], np.array([target_series[i]]))
            rs.append(r)
        stat = np.mean(rs, axis=0)

    return np.mean(rs, axis=0), np.std(rs, axis=0), pearsonr
    #return np.mean(rs, axis=0), np.std(rs, axis=0), rs, pearsonr

def plot_correlation(unit_activations, target_series, correlations, output):
    plt.figure(figsize=(12,8))
    max_r = 0
    for i,(name, activations) in enumerate(unit_activations.items()):
        plt.subplot(231+i)
        plt.title(name)
        #scatter here
        x = np.concatenate(target_series, 0)
        y = np.concatenate(activations, 0)
        #plt.scatter(x, y, alpha=0.01)
        plt.hist2d(x, y, bins=30, cmap=plt.cm.YlOrRd, norm=matplotlib.colors.LogNorm())
        #plt.hist2d(activations, target_series, bins=400, normed=matplotlib.colors.LogNorm)
        rho,rho_std,old_r = correlations[name] #get_mean_correlation([np.array([a]) for a in activations], target_series)
        # fit linear regession
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        xm = x.mean()
        xs = x.std()
        x_fit = np.linspace(x.min(), xm+2*xs)
        y_fit = p(x_fit)
        x2 = np.linspace(x.min(), x.max())
        # plot line of best fit
        plt.plot(x2,p(x2),'k-',label='$\\bar{{\\rho}}={:.2f} \\pm {:.2f}$ ($r={:.2f}$)'.format(rho, rho_std, old_r))
        plt.legend()
    plt.savefig(output)
    plt.clf()
    plt.close()
    return max_r


main()

