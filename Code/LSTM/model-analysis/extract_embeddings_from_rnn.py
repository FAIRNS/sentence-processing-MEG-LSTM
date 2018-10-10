#!/usr/bin/env python
import sys, os
import torch
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/word_language_model')))
import data
import numpy as np
import pickle
import matplotlib.pyplot as plt
import lstm
import networkx as nx

parser = argparse.ArgumentParser(description='Extract and plot LSTM weights')
parser.add_argument('-model', type=str, help='Meta file stored once finished training the corpus')
parser.add_argument('-v', '--vocabulary', default='reduced_vocab.txt')
parser.add_argument('-o', '--output', default='Figures/embedding_PCA.png', help='Destination for the output weights')
parser.add_argument('--cuda', action='store_true', default=False)
args = parser.parse_args()

# os.makedirs(os.path.dirname(args.output), exist_ok=True)


gate_names = ['Input', 'Forget', 'Cell', 'Output']
# Load model
print('Loading models...')
print('\nmodel: ' + args.model+'\n')
model = torch.load(args.model)
model.rnn.flatten_parameters()
embeddings = model.encoder.weight.data.numpy()

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(embeddings)
pca_score = pca.explained_variance_ratio_
V = pca.components_
X_transformed = pca.fit_transform(embeddings)

fig, ax = plt.subplots(1, figsize = (8, 8))
ax.text(X_transformed[:, 0], X_transformed[:, 1])

fig.savefig(args.output)