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



args = parser.parse_args()

#with open(args.meta, 'r') as f:
#    meta = json.load(f)
#    args.__dict__.update(meta['args'])
#args.save = args.meta[:-len('.meta')]
#extra_args.__override_args__ = args


vocab = data.Dictionary(args.vocabulary)
sentences = []
for l in open(args.input):
    sentence = l.rstrip('\n').split(" ") 
    sentences.append(sentence)
sentences = np.array(sentences)


print('Loading models...')
sentence_length = [len(s) for s in sentences]
max_length = max(*sentence_length)
import lstm
model = torch.load(args.model)
model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)



# output buffers
if args.fixed_length_arrays:
    vectors = np.zeros((len(sentences), 2 *model.nhid*model.nlayers, max_length))
    log_probabilities =  np.zeros((len(sentences), max_length))
    gates = {k: np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}
else:
    vectors = [np.zeros((2*model.nhid*model.nlayers, len(s))) for s in sentences] #np.zeros((len(sentences), 2 *model.nhid*model.nlayers, max_length))
    log_probabilities = [np.zeros(len(s)) for s in sentences] # np.zeros((len(sentences), max_length))
    gates = {k: [np.zeros((model.nhid*model.nlayers, len(s))) for s in sentences] for k in ['in', 'forget', 'out', 'c_tilde']} #np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}

for i, s in enumerate(sentences):
    sys.stdout.write("{}% complete ({} / {})\r".format(int(i/len(sentences) * 100), i, len(sentences)))
    out = None
    # reinit hidden
    hidden = model.init_hidden(1) 
    # intitialize with end of sentence
    inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[args.eos_separator]]]))
    out, hidden = model(inp, hidden)
    out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
    for j, w in enumerate(s):
        # store the surprisal for the current word
        log_probabilities[i][j] = out[0,0,vocab.word2idx[w]].data[0]

        inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
        out, hidden = model(inp, hidden)
        out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)

        vectors[i][:,j] = torch.cat([h.data.view(1,1,-1) for h in hidden],2).cpu().numpy()
        # we can retrieve the gates thanks to the hacked function
        for k, gates_k in gates.items():
            gates_k[i][:,j] = torch.cat([g[k].data for g in model.rnn.last_gates],1).cpu().numpy()

if args.perplexity:
    print ("{}".format(log_probabilities.shape))
    print ("{}".format(
            math.exp(-log_probabilities.sum()/(log_probabilities!=0).sum())))
else:
    #print ("DONE. Perplexity: {}".format(
    #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))

    out = {
        'vectors': vectors,
        'log_probabilities': log_probabilities
        }
    if args.format != 'hdf5':
        out['sentences'] = sentences

    for k, g in gates.items():
        out['gates.{}'.format(k)] = g
    out['sentence_length'] = np.array(sentence_length)

    if args.format == 'npz':
        np.savez(args.output, **out)
    elif args.format == 'hdf5':
        with h5py.File("{}.h5".format(args.output), "w") as hf:
            for k,v in out.items():
                dset = hf.create_dataset(k, data=v)
    elif args.format == 'pkl':
        with open(args.output + '.pkl', 'wb') as fout:
            pickle.dump(out, fout, -1)



