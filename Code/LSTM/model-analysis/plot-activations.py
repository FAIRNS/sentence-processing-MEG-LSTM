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
from tqdm import tqdm

from collections import defaultdict
np.seterr(all='raise')


def main():
    ap = argparse.ArgumentParser(description="""
    Takes the network activations for a set of sentences and a reference gold
    standard description of these sentences and produces plots relating 
    individual units to the data in the gold standard.
    """)
    ap.add_argument('vectors')
    ap.add_argument('reference')
    ap.add_argument('--lock-vectors', help='Field of the reference file to '
            'align the activity vectors')
    ap.add_argument('-t', '--analysis-type', required=True, choices=[
        'categories', 'correlation'])
    ap.add_argument('-g', '--group', default='structure', help=
            'Field of the gold-standard reference file to be used in plots')
    ap.add_argument('-o', '--output', required=True, help='Directory where to '
            'output the figures')
    ap.add_argument('--sample-size', type=int, default=1000,
            help='Size of the sample for the correlation')
    ap.add_argument('-u', '--units', action='append', type=int,
            help='Just plot the selected units')
    ap.add_argument('--decorrelate', 
            help='Field to decorrelate the target group from')
    ap.add_argument('--differentiate', action='store_true', default=False,
            help='Compute finite differences of neural activity')

    args = ap.parse_args()

    print('Loading data...')
    if args.vectors.endswith('npz'):
        data_vectors = np.load(args.vectors, 'r')
    elif args.vectors.endswith('pkl'):
        data_vectors = pickle.load(open(args.vectors, 'rb'))
    nhid = int(data_vectors['vectors'][0].shape[0] / 2)
    vectors = {}
    for name in ['gates.in', 'gates.out', 'gates.forget', 'gates.c_tilde']:
        vectors[name] = data_vectors[name]
    if isinstance(data_vectors['vectors'], list):
        vectors['hidden'] = [v[:nhid, :] for v in data_vectors['vectors']]
        vectors['cell'] = [v[nhid:, :] for v in data_vectors['vectors']]
    else:
        vectors['hidden'] = data_vectors['vectors'][:,:nhid,:]
        vectors['cell'] = data_vectors['vectors'][:,nhid:,:]

    if args.differentiate:
        for k,v in tqdm(vectors.items(), desc="Differentiating activations"):
            for i in tqdm(range(len(v)), desc='Units in {}'.format(k)):
                for j in reversed(range(v[i].shape[1])):
                    if j > 0:
                        v[i][:,j] = v[i][:,j] - v[i][:,j-1] 
                    else:
                        v[i][:,0] = 0

    reference = pickle.load(open(args.reference, 'rb'))

    if args.lock_vectors:
        vectors, shift_begin = lock_vectors(vectors, 
                [x[args.lock_vectors] for x in reference])

    if args.analysis_type ==  'categories':
        class_indexes = defaultdict(list)
        # get the indexes of the trials for each class
        for i,t in enumerate(reference):
            class_indexes[t[args.group]].append(i)

        group_labels = {'structure':  {2: "2-6", 1: "4-4", 3: "6-2"}}
    elif args.analysis_type == 'correlation':
        series = []
        decorr_series = []
        vectors_series = defaultdict(list)
        # iterate over the data senteneces, up to the point for which we have
        # vectors
        for i,t in enumerate(tqdm(reference[:len(data_vectors['sentences'])])):
            sentence, meta, data = t
            data['sentence-length'] = list(range(len(sentence)))
            # remove void entries, the first one (always the same) and the last one (change of sentence confound)
            content = np.array([[j,x] 
                for j,x in enumerate(data[args.group][1:-1]) 
                if x != "-"])
            if args.decorrelate:
                decorr_content = np.array([[j,x] 
                    for j,x in enumerate(data[args.decorrelate][1:-1]) 
                    if x != "-"])
            assert len(data_vectors['sentences'][i]) == len(next(iter(data.values())))
            # we only use sentences of a given max length and having
            # a series with a minimum length, and there must be SOME variability
            # max length 60
            # min length 10
            # more than 6 non-null
            # S -> NP VP heads
            # has variance
            start = 5
            if len(data[args.group]) < 60 and \
                    len(data[args.group]) > 10 and \
                    content.shape[0] > 6 and \
                    meta['head-type'] =='S_NP_VP' and \
                    not (content[start:,1] == content[start,1]).all():
                valid_idxs = content[start:,0].astype(np.int)
                series.append(content[start:,1])
                for k, v in vectors.items():
                    vectors_series[k].append(v[i][start:,valid_idxs])
                if args.decorrelate:
                    decorr_series.append(decorr_content[start:,1])
        # keep track of the length-depth pairs that we keep in the dataset
        decorr_idxs = []
        if args.decorrelate:
            print("Pre-procedure correlation R={:.2f} p={:.2e}".format(
                    *scipy.stats.spearmanr(
                        np.concatenate(series), 
                        np.concatenate(decorr_series))))
            x1 = [np.max(vals) for vals in series]
            x2 = [np.max(vals) for vals in decorr_series]
            m_1, s_1, q10_1, q90_1 = np.mean(x1), 3*np.std(x1), \
                    np.percentile(x1, 10), np.percentile(x1, 90)
            m_2, s_2, q10_2, q90_2 = np.mean(x2), 3*np.std(x2), \
                    np.percentile(x2, 10), np.percentile(x2, 90)
            decorr = BivariateDecorrelationFilter(
                    m_1, s_1, (q10_1, q90_1),
                    m_2, s_2, (q10_2, q90_2),
                    int(0.1 * len(series)))
            for i in tqdm(range(len(x1))):
                if decorr.filter((x1[i],x2[i])):
                    decorr_idxs.append(i)
            series = [series[i] for i in decorr_idxs]
            decorr_series = [decorr_series[i] for i in decorr_idxs]
            for k in vectors_series:
                vectors_series[k] = [vectors_series[k][i] for i in decorr_idxs]
            print("Post-procedure correlation R={:.2f} p={:.2e}".format(
                    *scipy.stats.spearmanr(
                        np.concatenate(series), 
                        np.concatenate(decorr_series))))

        vectors = vectors_series
        # randomply sample sample_size sentences
        indexes = list(range(len(next(iter(vectors.values())))))
        random.shuffle(indexes)
        indexes = indexes[:args.sample_size]
        for k in vectors:
            vectors[k] = [vectors[k][i] for i in indexes]
        series = [series[i] for i in indexes]
        #series = np.concatenate(series)
        # for k,v in vectors_series.items():
        #     vectors_series[k] = np.concatenate(v, 1)

    os.makedirs(args.output, exist_ok=True)

    # get the units with the largest r^2
    if args.units:
        units = args.units
    else:
        print('Computing statistics...')
        if args.analysis_type == 'correlation':
            mean_correlations, statistic = get_correlations(vectors, series)
            sorted_statistics = (-np.abs(statistic[0])).argsort()
        elif args.analysis_type == 'categories':
            statistic = get_f_statistics(vectors, class_indexes)
            sorted_statistics = (-np.abs(statistic)).argsort()
        with open('{}/statistic.txt'.format(args.output), 'w') as f:
            for i in sorted_statistics:
                if args.analysis_type == 'correlation':
                    f.write("{}\t{:.2f} +- {:.2f}\t{:.2f}\n".format(i,statistic[0][i], statistic[1][i], statistic[-1][i]))
                elif args.analysis_type == 'categories':
                    f.write("{}\n".format(i,statistic[i]))
        # pickl the top N statistically relevant units to plot
        units = sorted_statistics[:200]
    for u in units:
        sys.stdout.write('{:d}\n'.format(u))
        if args.analysis_type == 'categories':
            plot_categorical(
                    {k: v[:,u,:] for k,v in vectors.items()}, 
                    class_indexes, 
                    group_labels.get(args.group, None), 
                    os.path.join(args.output, '{}.svg'.format(u)), 
                    shift_begin if args.lock_vectors else None)
        elif args.analysis_type == 'correlation':
            plot_correlation(
                    {k: [v2[u, :] for v2 in v] for k,v 
                        in vectors.items()}, 
                    series, 
                    {k: (v[0][u],v[1][u],v[2][u]) for k, v 
                        in mean_correlations.items()},
                    os.path.join(args.output, '{}.png'.format(u)))

    print()

class BivariateDecorrelationFilter():
    def __init__(self, m1, s1, lim1, m2, s2, lim2, TARGET=150000):
        cv = np.array([[s1, 0], [0, s2]])
        mean = np.array([m1, m2])

        Z = 0
        bin_targets = {}
        for i in range(int(lim1[0]), int(lim1[1])):
            for j in range(int(lim2[0]), int(lim2[1])):
                bin_targets[(i,j)] = \
                        scipy.stats.multivariate_normal.pdf(
                                [i,j], mean=mean, cov=cv)

        Z = sum(bin_targets.values())

        for k,v in bin_targets.items():
            bin_targets[k] = v/Z * TARGET

        self.bin_targets = bin_targets

    def filter(self, vals):
        if vals in self.bin_targets and self.bin_targets[vals] > 0:
            self.bin_targets[vals] -= 1
            return True
        return False



def lock_vectors(vectors, positions, width=12):
    DUMMY = 0xbaadf00d
    locked_vectors = {}
    block_start = width // 2 - 2
    for name, activations in vectors.items():
        locked_vectors[name]  = np.full((len(activations), activations[0].shape[0],
            width), DUMMY, dtype=np.float32)
        for i, (sent_activations, pos) in enumerate(zip(activations, positions)):
            shift_begin = block_start - pos
            for j in range(sent_activations.shape[1]):
                if j+shift_begin < 0 or j+shift_begin >= width:
                    # remove parts of the sentence that don't fit in the array
                    continue
                locked_vectors[name][i,:,j+shift_begin] = sent_activations[:,j]
            # this position receives a constant value of 0 and all the rest
            # add or subtract to it
            align_pos = width // 2 - 2
            for j in range(width):
                locked_vectors[name][i,:,j] = locked_vectors[name][i,:,j] - \
                        locked_vectors[name][i,:,align_pos]
        locked_vectors[name] = np.ma.masked_values(locked_vectors[name], DUMMY)
    return locked_vectors, block_start


def get_correlations(vectors, series):
    mean_correlations = {}
    for i,(name, activations) in enumerate(vectors.items()):
        mean_correlations[name] = get_mean_correlation(activations, series)
    statistic = get_max_correlation(mean_correlations)
    return mean_correlations, statistic


def is_series_acceptable(xs):
    return len([x for x in xs if x!="-"]) > 1


def get_f_statistics(vectors, class_indexes):
    stats = np.zeros(vectors['hidden'].shape[1])
    # repeat for every unit
    for u in tqdm(range(len(stats))):
        max_stat = None
        # iterate over all types of activations
        for name, activations in vectors.items():
            # iterate over the length of the sentence
            for x in range(activations.shape[2]):
                # compute the ratio of within and between variance for 
                # the different groups at time point x
                if (activations[:,u,x]== 0).all():
                    # skip the alignment position
                    continue
                stat = scipy.stats.f_oneway(
                        *[activations[cidx][:,u,x]
                            for c,cidx in class_indexes.items()]).statistic  
                stat = abs(math.log(stat))
                # remember the largest difference
                if not max_stat or stat > max_stat:
                    max_stat = stat
        stats[u] = max_stat
    return stats

def plot_categorical(unit_activations, class_indexes, class_labels, output, 
        shift_begin):
    plt.figure(figsize=(12,8))
    for i,(name, activations) in enumerate(unit_activations.items()):
        plt.subplot(231+i)
        plt.title(name)
        if class_labels is not None:
            sort_key = lambda t: class_labels[t[0]]
        else:
            sort_key = None
        for c, cidx in sorted(class_indexes.items(), key=None):
            np.seterr(all='warn')
            yerr = activations[cidx].std(0)
            np.seterr(all='raise')
            _,caps,_ = plt.errorbar(
                    np.arange(activations.shape[1]), 
                    activations[cidx].mean(0), 
                    yerr=yerr, 
                    label='{}'.format(class_labels[c] if class_labels else c), 
                    capsize=10, elinewidth=1)
            for cap in caps:
                cap.set_markeredgewidth(2)
        plt.legend()
        plt.tight_layout()
    plt.savefig(output)
    plt.clf()
    plt.close()

def get_max_correlation(mean_correlations):
    '''
    takes a dictionary of names -> statistics and returns
    the statistics with the maximum value across names
    '''
    name_max = []
    for j in tqdm(range(next(iter(mean_correlations.values()))[0].shape[0])):
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
    #idxs = list(range(len(activations)))
    #random.shuffle(idxs)
    #idxs = idxs[:1000]
    approach = 2

    # just concatenating pearson approach
    pearsonr = vcorrcoef(np.concatenate(activations, axis=1), np.concatenate(target_series, axis=0))
    if approach == 1:
        stat = pearsonr
        rs = [stat]
    # mean of spearmanr correlations
    elif approach == 2:
        for k,i in enumerate(tqdm(range(len(activations)))):
            r = np.zeros(activations[i].shape[0]) 
            for j in range(r.shape[0]):
                r[j], p = scipy.stats.spearmanr(activations[i][j], target_series[i])
            rs.append(r)
        stat = np.mean(rs, axis=0)
    # mean of pearson correlations
    elif approach ==3:
        for k,i in enumerate(tqdm(range(len(activations)))):
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

