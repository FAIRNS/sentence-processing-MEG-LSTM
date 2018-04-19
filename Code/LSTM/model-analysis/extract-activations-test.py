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

model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
input_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/NP_VP_transition.txt'
vocabulary = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/NP_VP_transition.pkl'
eos_separator = '<eos>'
format = 'pkl'
get_representations = 'lstm'
cuda = False

vocab = data.Dictionary(vocabulary)
sentences = []
for l in open(input_data):
    sentence = l.rstrip('\n').split(" ") 
    sentences.append(sentence)
sentences = np.array(sentences)


print('Loading models...')
sentence_length = [len(s) for s in sentences]
max_length = max(*sentence_length)
import lstm
model = torch.load(model)
#model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)


out = {}

if 'word' in get_representations:
    print('Extracting bow representations')
    bow_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    word_vectors = np.zeros((len(sentences), model.encoder.embedding_dim, max_length))
    for i, s in enumerate(tqdm(sentences)):
        bow_h = np.zeros(model.encoder.embedding_dim)
        for j, w in enumerate(s):
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if cuda:
                inp = inp.cuda()
            w_vec = model.encoder.forward(inp).view(-1).data.cpu().numpy()
            word_vectors[i,:,j] = w_vec
            bow_h += w_vec
            bow_vectors[i,:,j] = bow_h / (j+1)
    out['word_vectors'] = word_vectors
    out['bow_vectors'] = bow_vectors

if 'lstm' in get_representations:
    print('Extracting LSTM representations')
    # output buffers
    fixed_length_arrays = False
    if fixed_length_arrays:
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
        inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[eos_separator]]]))
        if cuda:
            inp = inp.cuda()
        out, hidden = model(inp, hidden)
        out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
        for j, w in enumerate(s):
            # store the surprisal for the current word
            log_probabilities[i][j] = out[0,0,vocab.word2idx[w]].data[0]

            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if cuda:
                inp = inp.cuda()
            out, hidden = model(inp, hidden)
            out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)

            vectors['hidden'][i][:,j] = hidden[0].data.view(1,1,-1).cpu().numpy()
            vectors['cell'][i][:,j] = hidden[1].data.view(1,1,-1).cpu().numpy()
            # we can retrieve the gates thanks to the hacked function
            # for k, gates_k in vectors.items():
            for k, gates_k in vectors.items():
                if k in ['in', 'forget', 'out', 'c_tilde']:
                    gates_k[i][:,j] = torch.cat([g[k].data for g in model.rnn.last_gates],1).cpu().numpy()
        # save the results
        out['log_probabilities'] = log_probabilities

        if format != 'hdf5':
            out['sentences'] = sentences

        for k, g in vectors.items():
            out['gates.{}'.format(k)] = g
        out['sentence_length'] = np.array(sentence_length)

perplexity = False
if perplexity:
    print ("{}".format(log_probabilities.shape))
    print ("{}".format(
            math.exp(-log_probabilities.sum()/(log_probabilities!=0).sum())))
else:
    #print ("DONE. Perplexity: {}".format(
    #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))


    if format == 'npz':
        np.savez(output, **out)
    elif format == 'hdf5':
        with h5py.File("{}.h5".format(output), "w") as hf:
            for k,v in out.items():
                dset = hf.create_dataset(k, data=v)
    elif format == 'pkl':
        with open(output + '.pkl', 'wb') as fout:
            pickle.dump(out, fout, -1)

