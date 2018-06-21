#!/usr/bin/env python
import argparse
import pickle
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('activations', help='pkl file with the activations')
    args = ap.parse_args()

    pkl = pickle.load(open(args.activations, 'rb'))

    log_probs = pkl['log_probabilities']

    for sent_log_probs in log_probs:
        print(np.exp(-sent_log_probs.mean()))


main()
