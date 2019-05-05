import argparse

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-f', '--data-filename', default='subjrel.txt', type=str, help = 'filename of input dataset')
parser.add_argument('-n', default=250 , type=int, help = 'number of samples from each condition')
parser.add_argument('--max-iter', default=10 , type=int, help = 'maximal number of allowed iterations over the input text file')
parser.add_argument('-seed', default=1 , type=int, help = 'Random seed for replicability')
parser.add_argument('--IX-last', default=-2 , type=int, help = 'what is the last index for the features in the tab-delimited input file. default means that feature columns are in [2:-1]')
args = parser.parse_args()


def counter_fullfilled(counter, n):
    fullfilled = True
    for attractor2_gender in ['masculine', 'feminine']:
        for attractor2_number in ['singular', 'plural']:
            for attractor1_gender in ['masculine', 'feminine']:
                for attractor1_number in ['singular', 'plural']:
                    for gender in ['masculine', 'feminine']:
                        for number in ['singular', 'plural']:
                            if counter["_".join([gender, number, attractor1_gender, attractor1_number, attractor2_gender, attractor2_number])] < n:
                                fullfilled = False
    return fullfilled


# Create counter
counter = {}
for attractor2_gender in ['masculine', 'feminine']:
    for attractor2_number in ['singular', 'plural']:
        for attractor1_gender in ['masculine', 'feminine']:
            for attractor1_number in ['singular', 'plural']:
                for gender in ['masculine', 'feminine']:
                    for number in ['singular', 'plural']:
                        counter["_".join([gender, number, attractor1_gender, attractor1_number, attractor2_gender, attractor2_number])] = 0


import numpy as np
np.random.seed(args.seed)
finished = False
stimuli_filtered = []

with open(args.data_filename, 'r') as f:
    all_stimuli = f.readlines()
num_lines = len(all_stimuli)
features = all_stimuli[0].strip().split('\t')[2:args.IX_last] # N1_gender, N1_number, N2_gender, N2_number
num_features = len(features)
p = args.n*(2^num_features)/num_lines # sampling probability (=desired_num_stimuli/file_size)
for iter in range(args.max_iter):
    with open(args.data_filename, 'r') as f:
        while not finished:
            # read line
            line = f.readline()
            if not line:
                break
            features = line.strip().split('\t')[2:args.IX_last] # N1_gender, N1_number, N2_gender, N2_number
            if counter["_".join(features)] < args.n:
                if np.random.rand() < p:
                    curr_sentence = line.strip().split('\t')[1]
                    curr_sentence_was_already_sampled = any(curr_sentence==s[1] for s in stimuli_filtered)
                    if sum(counter.values()) == 0 or not curr_sentence_was_already_sampled:
                        stimuli_filtered.append(line.strip().split('\t'))
                        # print(line.strip())
                        counter["_".join(features)] += 1
        finished = counter_fullfilled(counter, args.n)

    if finished:
        # Sort based on:
        stimuli_filtered.sort(key=lambda x: x[1]) # first word
        stimuli_filtered.sort(key=lambda x: x[5], reverse=True) # feature 1
        stimuli_filtered.sort(key=lambda x: x[3], reverse=True) # feature 2

        [print('\t'.join(l)) for l in stimuli_filtered]
        exit()

print("ERROR: sub-sampling process did not complete - try to increase max-iter!")







