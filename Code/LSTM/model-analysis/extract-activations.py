#!/usr/bin/env python
import sys
import math
import os
import torch
import argparse
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    '../src/word_language_model')))
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
parser.add_argument('--format', default='pkl', choices=['npz', 'hdf5', 'pkl'])
parser.add_argument('-g', '--get-representations', choices=['lstm', 'word'],
        action='append', default=[])
parser.add_argument('--use-unk', action='store_true', default=False)


args = parser.parse_args()

if args.perplexity and 'lstm' not in args.get_representations:
    args.get_representations.append('lstm')
elif not args.perplexity and len(args.get_representations) == 0:
    raise RuntimeError("Please specify at least one of -g lstm or -g word")

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


print('Loading models...', file=sys.stderr)
sentence_length = [len(s) for s in sentences]
max_length = max(*sentence_length)
import lstm
model = torch.load(args.model)
#model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)


saved = {}

if 'word' in args.get_representations:
    print('Extracting bow representations', file=sys.stderr)
    bow_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    word_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    for i, s in enumerate(tqdm(sentences)):
        bow_h = np.zeros(model.encoder.embedding_dim)
        for j, w in enumerate(s):
            if w not in vocab.word2idx and args.use_unk:
                w = '<unk>'
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if args.cuda:
                inp = inp.cuda()
            w_vec = model.encoder.forward(inp).view(-1).data.cpu().numpy()
            word_vectors[i,:,j] = w_vec
            bow_h += w_vec
            bow_vectors[i,:,j] = bow_h / (j+1)
    saved['word_vectors'] = word_vectors
    saved['bow_vectors'] = bow_vectors

if 'lstm' in args.get_representations:
    print('Extracting LSTM representations', file=sys.stderr)
    # output buffers
    if args.fixed_length_arrays:
        log_probabilities =  np.zeros((len(sentences), max_length))
        if not args.perplexity:
            vectors = {k: np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']}
    else:
        log_probabilities = [np.zeros(len(s)) for s in tqdm(sentences)] # np.zeros((len(sentences), max_length))
        if not args.perplexity:
            vectors = {k: [np.zeros((model.nhid*model.nlayers, len(s))) for s in tqdm(sentences)] for k in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']} #np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}

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
            if w not in vocab.word2idx and args.use_unk:
                w = '<unk>'
            # store the surprisal for the current word
            log_probabilities[i][j] = out[0,0,vocab.word2idx[w]].data[0]
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if args.cuda:
                inp = inp.cuda()
            out, hidden = model(inp, hidden)
            out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)

            if not args.perplexity:
                vectors['hidden'][i][:,j] = hidden[0].data.view(1,1,-1).cpu().numpy()
                vectors['cell'][i][:,j] = hidden[1].data.view(1,1,-1).cpu().numpy()
                # we can retrieve the gates thanks to the hacked function
                for k, gates_k in vectors.items():
                    if 'gates' in k:
                        k = k.split('.')[1]
                        gates_k[i][:,j] = torch.cat([g[k].data for g in model.rnn.last_gates],1).cpu().numpy()
        # save the results
        saved['log_probabilities'] = log_probabilities

        if args.format != 'hdf5':
            saved['sentences'] = sentences

        saved['sentence_length'] = np.array(sentence_length)

        if not args.perplexity:
            for k, g in vectors.items():
                saved[k] = g

    print ("Perplexity: {:.2f}".format(
            math.exp(
                    sum(-lp.sum() for lp in log_probabilities)/
                    sum((lp!=0).sum() for lp in log_probabilities))))
if not args.perplexity:
    #print ("DONE. Perplexity: {}".format(
    #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))


    if args.format == 'npz':
        np.savez(args.output, **saved)
    elif args.format == 'hdf5':
        with h5py.File("{}.h5".format(args.output), "w") as hf:
            for k,v in saved.items():
                dset = hf.create_dataset(k, data=v)
    elif args.format == 'pkl':
        with open(args.output + '.pkl', 'wb') as fout:
            pickle.dump(saved, fout, -1)

