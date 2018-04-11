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
from tqdm import tqdm

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
parser.add_argument('--cuda', action='store_true', default=False)
parser.add_argument('--format', default='npz', choices=['npz', 'hdf5', 'pkl'])
parser.add_argument('-g', '--get-representations', choices=['lstm', 'word'],
        action='append', required=True)


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
#model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)


out = {}

if 'word' in args.get_representations:
    print('Extracting bow representations')
    bow_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    word_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    for i, s in enumerate(tqdm(sentences)):
        bow_h = np.zeros(model.encoder.embedding_dim)
        for j, w in enumerate(s):
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if args.cuda:
                inp = inp.cuda()
            w_vec = model.encoder.forward(inp).view(-1).data.cpu().numpy()
            word_vectors[i,:,j] = w_vec
            bow_h += w_vec
            bow_vectors[i,:,j] = bow_h / (j+1)
    out['word_vectors'] = word_vectors
    out['bow_vectors'] = bow_vectors

if 'lstm' in args.get_representations:
    print('Extracting LSTM representations')
    # output buffers
    if args.fixed_length_arrays:
        log_probabilities =  np.zeros((len(sentences), max_length))
        vectors = {k: np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde', 'hidden', 'cell']}
    else:
        log_probabilities = [np.zeros(len(s)) for s in tqdm(sentences)] # np.zeros((len(sentences), max_length))
        vectors = {k: [np.zeros((model.nhid*model.nlayers, len(s))) for s in tqdm(sentences)] for k in ['in', 'forget', 'out', 'c_tilde', 'hidden', 'cell']} #np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}

    for i, s in enumerate(tqdm(sentences)):
        #sys.stdout.write("{}% complete ({} / {})\r".format(int(i/len(sentences) * 100), i, len(sentences)))
        out = None
        # reinit hidden
        hidden = model.init_hidden(1) 
        # intitialize with end of sentence
        inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[args.eos_separator]]]))
        if args.cuda:
            inp = inp.cuda()
        out, hidden = model(inp, hidden)
        out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
        for j, w in enumerate(s):
            # store the surprisal for the current word
            log_probabilities[i][j] = out[0,0,vocab.word2idx[w]].data[0]

            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if args.cuda:
                inp = inp.cuda()
            out, hidden = model(inp, hidden)
            out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)

            vectors['hidden'][i][:,j] = h[0].data.view(1,1,-1).cpu().numpy()
            vectors['cell'][i][:,j] = h[1].data.view(1,1,-1).cpu().numpy()
            # we can retrieve the gates thanks to the hacked function
            for k, gates_k in vectors.items():
                gates_k[i][:,j] = torch.cat([g[k].data for g in model.rnn.last_gates],1).cpu().numpy()
        # save the results
        out['log_probabilities'] = log_probabilities

        if args.format != 'hdf5':
            out['sentences'] = sentences

        for k, g in vectors.items():
            out['gates.{}'.format(k)] = g
        out['sentence_length'] = np.array(sentence_length)

if args.perplexity:
    print ("{}".format(log_probabilities.shape))
    print ("{}".format(
            math.exp(-log_probabilities.sum()/(log_probabilities!=0).sum())))
else:
    #print ("DONE. Perplexity: {}".format(
    #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))


    if args.format == 'npz':
        np.savez(args.output, **out)
    elif args.format == 'hdf5':
        with h5py.File("{}.h5".format(args.output), "w") as hf:
            for k,v in out.items():
                dset = hf.create_dataset(k, data=v)
    elif args.format == 'pkl':
        with open(args.output + '.pkl', 'wb') as fout:
            pickle.dump(out, fout, -1)

