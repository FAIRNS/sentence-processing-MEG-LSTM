#!/usr/bin/env python
import sys
import math
import os
import torch
sys.path.append(os.path.abspath('../src/word_language_model'))
import data
import numpy as np
import pickle
from tqdm import tqdm

# French
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/model2-500-2-0.5-SGD-10-tied.False-300/LSTM-corpora~frwac_random_100M_subset-500-2-0.5-SGD-10-tied.False-300/model.cpu.pt/model.cpu.pt' # French
input_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/NP_VP_transition.txt'
input_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/relative_clauses_pos_French.txt'
vocabulary = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/reduced-vocab.txt' # French
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/model2-500-2-0.5-SGD-10-tied.False-300/relative_clauses_pos_French.pkl'

# English
# model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt' # English
# input_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/relative_clause_English.txt'
# vocabulary = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt' # English
# output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/english/relative_clauses_English.pkl'

# German's use for French
eos_separator = '</s>'
unk = '_UNK_'
# -----------------------

# # Kristina's for English
# eos_separator = '<eos>'
# unk = '<unk>'
# # ------------------

format = 'pkl'
get_representations = ['word', 'lstm']
cuda = False
use_unk = True
perplexity = False

vocab = data.Dictionary(vocabulary)
sentences = []
for l in open(input_data, 'r'):
    sentence = l.rstrip().split(" ")
    sentence = [s.lower() for s in sentence]
    sentences.append(sentence)
sentences = np.array(sentences)
# sentences = sentences[0:1000]

print('Loading models...')
sentence_length = [len(s) for s in sentences]
max_length = max(*sentence_length)
import lstm
model = torch.load(model)
#model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)


saved = {}
unk_words = []

if 'word' in get_representations:
    print('Extracting bow representations')#, file=sys.stderr)
    bow_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in tqdm(sentences)]
    word_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in tqdm(sentences)]
    for i, s in enumerate(tqdm(sentences)):
        bow_h = np.zeros(model.encoder.embedding_dim)
        for j, w in enumerate(s):
            if w not in vocab.word2idx and use_unk:
                unk_words.append(w)
                w = unk
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if cuda:
                inp = inp.cuda()
            w_vec = model.encoder.forward(inp).view(-1).data.cpu().numpy()
            word_vectors[i][:,j] = w_vec
            bow_h += w_vec
            bow_vectors[i][:,j] = bow_h / (j+1)
    saved['word_vectors'] = word_vectors
    saved['bow_vectors'] = bow_vectors

print(set(unk_words))

if 'lstm' in get_representations:
    print('Extracting LSTM representations')#, file=sys.stderr)
    # output buffers
    fixed_length_arrays = False
    if fixed_length_arrays:
        log_probabilities =  np.zeros((len(sentences), max_length))
        if not perplexity:
            vectors = {k: np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']}
    else:
        log_probabilities = [np.zeros(len(s)) for s in tqdm(sentences)] # np.zeros((len(sentences), max_length))
        if not perplexity:
            vectors = {k: [np.zeros((model.nhid*model.nlayers, len(s))) for s in tqdm(sentences)] for k in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']} #np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}

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
            if w not in vocab.word2idx and use_unk:
                w = unk
            # store the surprisal for the current word
            log_probabilities[i][j] = out[0,0,vocab.word2idx[w]].data[0]
            inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
            if cuda:
                inp = inp.cuda()
            out, hidden = model(inp, hidden)
            out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
            if not perplexity:
                vectors['hidden'][i][:,j] = hidden[0].data.view(1,1,-1).cpu().numpy()
                vectors['cell'][i][:,j] = hidden[1].data.view(1,1,-1).cpu().numpy()
                # we can retrieve the gates thanks to the hacked function
                for k, gates_k in vectors.items():
                    if 'gates' in k:
                        k = k.split('.')[1]
                        gates_k[i][:,j] = torch.cat([g[k].data for g in model.rnn.last_gates],1).cpu().numpy()
        # save the results
        saved['log_probabilities'] = log_probabilities

        if format != 'hdf5':
            saved['sentences'] = sentences

        saved['sentence_length'] = np.array(sentence_length)

        if not perplexity:
            for k, g in vectors.items():
                saved[k] = g

    print ("Perplexity: {:.2f}".format(
            math.exp(
                    sum(-lp.sum() for lp in log_probabilities)/
                    sum((lp!=0).sum() for lp in log_probabilities))))
# if not perplexity:
#     #print ("DONE. Perplexity: {}".format(
#     #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))
#
#
#     if format == 'npz':
#         np.savez(output, **saved)
#     elif format == 'hdf5':
#         with h5py.File("{}.h5".format(output), "w") as hf:
#             for k,v in saved.items():
#                 dset = hf.create_dataset(k, data=v)
#     elif format == 'pkl':

with open(output, 'wb') as fout:
    pickle.dump(saved, fout, -1)

