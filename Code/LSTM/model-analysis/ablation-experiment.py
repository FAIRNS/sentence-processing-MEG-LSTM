#!/usr/bin/env python
import sys
import os
import torch
import argparse
sys.path.append(os.path.abspath('../src/word_language_model'))
import data
import numpy as np
import h5py
import pickle
import pandas

parser = argparse.ArgumentParser(
    description='PyTorch PennTreeBank RNN/LSTM Language Model')
parser.add_argument('model', type=str, default='model.pt',
                    help='Meta file stored once finished training the corpus')
parser.add_argument('-i', '--input', required=True,
                    help='Input sentences')
parser.add_argument('-v', '--vocabulary', default='reduced_vocab.txt')
parser.add_argument('-o', '--output', help='Destination for the output vectors')
parser.add_argument('--perplexity', action='store_true', default=False)
parser.add_argument('--eos-separator', default='</s>')
parser.add_argument('--fixed-length-arrays', action='store_true', default=False,
        help='Save the result to a single fixed-length array')
parser.add_argument('--format', default='npz', choices=['npz', 'hdf5', 'pkl'])
parser.add_argument('-u', '--unit', default=False, help='Which test unit to ablate')
parser.add_argument('-s', '--seed', default=1, help='Random seed when adding random units')
parser.add_argument('-g', '--groupsize', default=1, help='Group size of units to ablate, including test unit and random ones')
args = parser.parse_args()


# Which unit to kill + a random subset of g-1 more units
np.random.seed(int(args.seed))
add_random_subset = np.random.permutation(1301)
add_random_subset = [i for i in add_random_subset if i not in [int(args.unit)]] # omit current test unit from random set
units_to_kill = [int(args.unit)] + add_random_subset[0:(int(args.groupsize)-1)] # add g-1 random units
units_to_kill = [u-1 for u in units_to_kill] # Change counting to zero
units_to_kill_l0 = [u for u in units_to_kill if u <650] # units 1-650 (0-649) in layer 0 (l0)
units_to_kill_l1 = [u-650 for u in units_to_kill if u >649] # units 651-1300 (650-1299) in layer 1 (l1)
output = args.output + args.unit + '_groupsize_' + args.groupsize + '_seed_' + args.seed # Update output file name

# Vocabulary
vocab = data.Dictionary(args.vocabulary)

# Sentences
agreement_test_data = pandas.read_csv(args.input, sep='\t')
sentences_prefix = [s[7] for s in agreement_test_data._values]
correct_wrong = [s[5] for s in agreement_test_data._values]
verbs = [s[4] for s in agreement_test_data._values]
len_context = [s[11] for s in agreement_test_data._values]
len_prefix = [s[12] for s in agreement_test_data._values]
log_p = [s[14] for s in agreement_test_data._values]

sentences_prefix = [s.split() for s in sentences_prefix]
sentence_length = [len(s) for s in sentences_prefix]
max_length = max(*sentence_length)

# Load model
print('Loading models...')
import lstm
model = torch.load(args.model)
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

for ablation in [False, True]:
    output_fn = output + '_' + str(ablation) + '.pkl' # update output file name
    if ablation:
        # Kill corresponding weights if list is not empty
        if units_to_kill_l0: model.rnn.weight_hh_l0.data[:, units_to_kill_l0] = 0 # l0: w_hi, w_hf, w_hc, w_ho
        if units_to_kill_l1: model.rnn.weight_hh_l1.data[:, units_to_kill_l1] = 0 # l0: w_hi, w_hf, w_hc, w_ho
        if units_to_kill_l0: model.rnn.weight_ih_l0.data[:, units_to_kill_l0] = 0 # l1: w_ii, w_if, w_ic, w_io
        if units_to_kill_l1: model.rnn.weight_ih_l1.data[:, units_to_kill_l1] = 0 # l1: w_ii, w_if, w_ic, w_io
        if units_to_kill_l0: model.rnn.bias_hh_l0.data[units_to_kill_l0] = 0
        if units_to_kill_l1: model.rnn.bias_hh_l1.data[units_to_kill_l1] = 0
        if units_to_kill_l0: model.rnn.bias_ih_l0.data[units_to_kill_l0] = 0
        if units_to_kill_l1: model.rnn.bias_ih_l1.data[units_to_kill_l1] = 0

    # Test: present prefix sentences and calculate probability of target verb.
    for i, s in enumerate(sentences_prefix):
        print
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
    if args.format == 'npz':
        np.savez(output, **out)
    elif args.format == 'hdf5':
        with h5py.File("{}.h5".format(output), "w") as hf:
            for k,v in out.items():
                dset = hf.create_dataset(k, data=v)
    elif args.format == 'pkl':
        with open(output_fn, 'wb') as fout:
            pickle.dump(out, fout, -1)
