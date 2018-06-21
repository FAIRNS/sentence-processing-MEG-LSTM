#!/usr/bin/env python
import argparse
import fileinput
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', nargs='*')
    args = ap.parse_args()

    xs = np.array([float(l) for l in fileinput.input(args.input)])

    qs = np.arange(10, 100, 10)

    ps = np.percentile(xs, qs)

    for k,v in zip(qs, ps):
        print(k, v)


main()

