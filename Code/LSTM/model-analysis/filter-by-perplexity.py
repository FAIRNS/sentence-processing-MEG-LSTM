#!/usr/bin/env python
import argparse
import pickle
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--threshold', type=float, required=True, help='perplexity cutoff')
    ap.add_argument('-o', '--output', help='filtered output pkl filename')
    ap.add_argument('activations', help='pkl file with the activations')
    args = ap.parse_args()

    pkl = pickle.load(open(args.activations, 'rb'))

    log_probs = pkl['log_probabilities']

    new_pkl = {k: [] for k in pkl}

    for i in range(len(log_probs)):
        sent_log_probs = log_probs[i]
        ppl = np.exp(-sent_log_probs.mean())
        keep = ppl < args.threshold
        if keep:
            for k in pkl:
                new_pkl[k].append(pkl[k][i])
            print(" ".join(pkl['sentences'][i]))

    if args.output:
        pickle.dump(new_pkl, open(args.output, 'wb'))

main()
