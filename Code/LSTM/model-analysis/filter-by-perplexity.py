#!/usr/bin/env python
import argparse
import pickle
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--threshold', type=float, required=True, help='perplexity cutoff')
    ap.add_argument('-o', '--output', help='filtered output pkl filename')
    ap.add_argument('-i', '--info', help='info pkl file')
    ap.add_argument('-io', '--info-output', help='info output pkl filename')
    ap.add_argument('-a', '--activations', help='pkl file with the activations')
    args = ap.parse_args()

    pkl = pickle.load(open(args.activations, 'rb'))
    if args.info:
        info = pickle.load(open(args.info, 'rb'))

    log_probs = pkl['log_probabilities']

    new_pkl = {k: [] for k in pkl}
    new_info = []

    for i in range(len(log_probs)):
        sent_log_probs = log_probs[i]
        ppl = np.exp(-sent_log_probs.mean())
        keep = ppl < args.threshold
        if keep:
            for k in pkl:
                new_pkl[k].append(pkl[k][i])
            print(" ".join(pkl['sentences'][i]))
            if args.info:
                new_info.append(info[i])

    if args.output:
        pickle.dump(new_pkl, open(args.output, 'wb'))
    if args.info_output:
        pickle.dump(new_info, open(args.info_output, 'wb'))
        

main()
