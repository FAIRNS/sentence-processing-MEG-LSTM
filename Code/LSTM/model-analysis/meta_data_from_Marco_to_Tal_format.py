import sys, os
import argparse
import numpy as np
import pickle
import pandas
import time
import copy
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Switching from Marco files to Tal format')
parser.add_argument('-i', '--input', required=True, help='Input sentences in Marco\'s format')
parser.add_argument('-o', '--output', required=True, help='Output sentences in Tal\'s format')
args = parser.parse_args()


with open(args.input, 'r') as f:
    raw = f.readlines()

# Split each row to different fields and save separately the sentences and the info
sentences_plus_meta = [line.split('\t')[1]+ '\n' for line in raw]
info = []
for line in raw:
    curr_info = {}
    curr_line = line.split('\t')
    curr_info['RC_type'] = curr_line[0]
    curr_info['sentence_length'] = len(curr_line)
    curr_info['number_1'] = curr_line[2]
    curr_info['number_2'] = curr_line[3]
    if len(curr_line)>4:
        curr_info['number_3'] = curr_line[4]
    if len(curr_line) > 5:
        curr_info['verb_1'] = curr_line[5]
    if len(curr_line) > 6:
        curr_info['verb_2'] = curr_line[6]
    info.append(curr_info)
