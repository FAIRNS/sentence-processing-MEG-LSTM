#!/usr/bin/env python
import sys
import math
import os
import torch
import argparse
import json
sys.path.append(os.path.abspath('../src/word_language_model'))
import data
import numpy as np
import h5py
import pickle
import pandas

# Paths
script = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py'
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model.tab'
agreement_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model_sentences.txt'
vocab = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_'
eos = '"<eos>"'
format = 'pkl'

# Which unit to kill + a random subset of g-1 more units
units_to_kill = [1]
g = 10
add_random_subset = np.random.permutation(651)
add_random_subset = [i for i in add_random_subset if i not in units_to_kill]
units_to_kill = units_to_kill + add_random_subset[0:(g-1)]

# Update output file name
output = output + str(units_to_kill)

# Vocabulary
vocab = data.Dictionary(vocab)

# Sentences
agreement_test_data = pandas.read_csv(agreement_data, sep='\t')
sentences_prefix = [s[7] for s in agreement_test_data._values]
correct_wrong = [s[5] for s in agreement_test_data._values]
verbs = [s[4] for s in agreement_test_data._values]
len_context = [s[11] for s in agreement_test_data._values]
len_prefix = [s[12] for s in agreement_test_data._values]
log_p = [s[14] for s in agreement_test_data._values]

# Save to file
with open(agreement_sentences, 'wb') as f:
    for s in sentences_prefix:
        f.write("%s\n" % s)

sentences_prefix = [s.split() for s in sentences_prefix]
sentence_length = [len(s) for s in sentences_prefix]
max_length = max(*sentence_length)

# Load model
print('Loading models...')
import lstm
model = torch.load(model)
model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)

# output buffers
fixed_length_arrays = False
if fixed_length_arrays:
    vectors = np.zeros((len(sentences_prefix), 2 * model.nhid * model.nlayers, max_length))
    log_probabilities =  np.zeros((len(sentences_prefix), max_length))
    gates = {k: np.zeros((len(sentences_prefix), model.nhid * model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}
else:
    vectors = [np.zeros((2*model.nhid*model.nlayers, len(s))) for s in sentences_prefix] #np.zeros((len(sentences), 2 *model.nhid*model.nlayers, max_length))
    log_probabilities = [np.zeros(len(s)) for s in sentences_prefix] # np.zeros((len(sentences), max_length))
    gates = {k: [np.zeros((model.nhid*model.nlayers, len(s))) for s in sentences_prefix] for k in ['in', 'forget', 'out', 'c_tilde']} #np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}
    log_p_targets = np.zeros((len(sentences_prefix), 1))

# Compare performamce w/o killing units (set to zero the corresponding weights in model):

units_to_kill = [u-1 for u in units_to_kill] # Change counting to from-zero
for ablation in [False, True]:
    output_fn = output + '_' + str(ablation) + '.pkl' # output file name
    if ablation:
        model.rnn.weight_hh_l0.data[:, units_to_kill] = 0
        model.rnn.weight_hh_l1.data[:, units_to_kill] = 0
        model.rnn.weight_ih_l0.data[:, units_to_kill] = 0
        model.rnn.weight_ih_l1.data[:, units_to_kill] = 0
        model.rnn.bias_hh_l0.data[units_to_kill] = 0
        model.rnn.bias_hh_l1.data[units_to_kill] = 0
        model.rnn.bias_ih_l0.data[units_to_kill] = 0
        model.rnn.bias_ih_l1.data[units_to_kill] = 0

    # Test: present prefix sentences and calculate probability of target verb.
    for i, s in enumerate(sentences_prefix):
        sys.stdout.write("{}% complete ({} / {})\r".format(int(i / len(sentences_prefix) * 100), i, len(sentences_prefix)))
        out = None
        # reinit hidden
        hidden = model.init_hidden(1)
        # intitialize with end of sentence
        inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx['<eos>']]]))
        out, hidden = model(inp, hidden)
        out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
        for j, w in enumerate(s):
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            out, hidden = model(inp, hidden)
            out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
        # Store surprisal of target word
        log_p_targets[i] = out[0, 0, vocab.word2idx[verbs[i]]].data[0]
    # Split to correct (odd) and wrong (even) sentences
    log_p_targets_correct = log_p_targets[::2]
    log_p_targets_wrong = log_p_targets[1::2]
    # Score the performance of the model w/o ablation
    score_on_task = np.sum(log_p_targets_correct > log_p_targets_wrong)

    out = {
        'log_p_targets_correct': log_p_targets_correct,
        'log_p_targets_wrong': log_p_targets_wrong,
        'score_on_task': score_on_task,
        'sentences_prefix': sentences_prefix,
        'sentence_length': np.array(sentence_length)
    }

    # Save to file
    if format == 'npz':
        np.savez(output, **out)
    elif format == 'hdf5':
        with h5py.File("{}.h5".format(output), "w") as hf:
            for k,v in out.items():
                dset = hf.create_dataset(k, data=v)
    elif format == 'pkl':
        with open(output_fn, 'wb') as fout:
            pickle.dump(out, fout, -1)
