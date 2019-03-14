#!/usr/bin/env python
import subprocess
import argparse
import itertools
import json
import sys

parser = argparse.ArgumentParser(description='Create a grid from json')
parser.add_argument('--grid-filename', help='Json or python that contains the grid parameters')
parser.add_argument('--lm-script', required=True)

args = parser.parse_args()
with open(args.grid_filename, 'r') as f:
    if args.grid_filename.endswith('.json'):
        grid = json.load(f)
    else:
        grid = eval(f.read())

namefmt = grid['name']
parameters = grid['parameters']

perms = list(itertools.product(*parameters.values()))

names = set()
for p in perms:
    argstr = ""
    name = namefmt.format(**dict(zip(parameters.keys(),
                          [str(p_i).replace('/', '~').replace('-', '_') for p_i in p])))
    for i,k in enumerate(parameters.keys()):
        if type(p[i]) == bool:
            if p[i]:
                argstr += " --" + str(k)
        else:
            argstr += " --" + str(k) + " " + str(p[i]).format(name=name)
    if name in names:
        sys.stderr.write('WARNING: {} already exists\n'.format(name))
    else:
        names.add(name)
    cmd = "python {script} {argstr}".format(
    script=args.lm_script,
    argstr=argstr)
    print(cmd)
