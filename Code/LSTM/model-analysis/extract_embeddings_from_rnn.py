#!/usr/bin/env python
import sys, os
import torch
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/word_language_model')))
import data
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Extract and plot LSTM weights')
parser.add_argument('-model', type=str, help='Meta file stored once finished training the corpus')
parser.add_argument('-v', '--vocabulary', default='Data/LSTM/english_vocab.txt')
parser.add_argument('-o', '--output', default='Figures/verbs.png', help='Destination for the output figure')
parser.add_argument('-u', '--units', nargs='+', help='Which units to plot')
parser.add_argument('-c', '--colors', nargs='+', help='corresponding colors for each unit')
parser.add_argument('-i', '--input', default='Data/Stimuli/singular_plural_verbs.txt',
					help='Text file with two tab delimited columns with the lists of output words to contrast with the PCA')
args = parser.parse_args()

if args.colors is not None:
	assert len(args.units) == len(args.colors), "!!!---Number of colors is not equal to number of units---!!!"

gate_names = ['Input', 'Forget', 'Cell', 'Output']
# Parse output dir and file names:
# os.makedirs(os.path.dirname(args.output), exist_ok=True)
dirname = os.path.dirname(args.output)
filename = os.path.basename(args.output)

# Load model
print('Loading models...')
print('\nmodel: ' + args.model+'\n')
model = torch.load(args.model)
model.rnn.flatten_parameters()
embeddings = model.decoder.weight.data.numpy()
vocab = data.Dictionary(args.vocabulary)

# Read list of contrasted words (e.g., singular vs. plural verbs).
with open(args.input, 'r') as f:
	lines=f.readlines()
verbs_singular = [l.split('\t')[0].strip() for l in lines]
verbs_plural = [l.split('\t')[1].strip() for l in lines]
verbs_all = verbs_singular + verbs_plural
print(verbs_all)

# Get index in the vocab for all words and extract embeddings
idx_verbs_singular = [vocab.word2idx[w] for w in verbs_singular]
idx_verbs_plural = [vocab.word2idx[w] for w in verbs_plural]
idx_verbs_all = idx_verbs_singular + idx_verbs_plural
embeddings_verbs_singular = embeddings[idx_verbs_singular, :]
embeddings_verbs_plural = embeddings[idx_verbs_plural, :]
embeddings_verbs_all = embeddings[idx_verbs_singular + idx_verbs_plural ,:]

#### Plot verb embeddings
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(embeddings_verbs_all)
pca_score = pca.explained_variance_ratio_
V = pca.components_
X_transformed = pca.fit_transform(embeddings_verbs_all)
PC1 = V[0, :]
PC2 = V[1, :]
print(650 + np.argsort(np.negative(np.abs(PC1))))
print(650 + np.argsort(np.negative(np.abs(PC2))))

fig, ax = plt.subplots(1, figsize = (40, 30))
for i in tqdm(range(X_transformed.shape[0])):
	# if w % 10 == 1:
	ax.text(X_transformed[i, 0], X_transformed[i, 1], verbs_all[i], size=30)

lim_max = np.max(X_transformed)
lim_min = np.min(X_transformed)
ax.set_xlim((lim_min, lim_max))
ax.set_ylim((lim_min, lim_max))
ax.axis('off')
fig.savefig(os.path.join(dirname, 'PCA_'+filename))
print('Saved to: ' + os.path.join(dirname, 'PCA_'+filename))
plt.close(fig)

units = [int(u) for u in args.units]
bar_width = 0.2
## Extract weights from number units to verbs
fig, ax = plt.subplots(1, figsize = (10,10))
for u, from_unit in enumerate(units):
	if u == 0:
		label_sing = 'Singular form of verb'; label_plur = 'Plural form of verb'
	else:
		label_sing = ''; label_plur = ''
	from_unit = from_unit - 650
	output_weights_singular = embeddings[idx_verbs_singular, from_unit]
	ax.scatter(u + np.random.random(output_weights_singular.size) * bar_width - bar_width/2, output_weights_singular, s=30, color=args.colors[u], label=label_sing, marker='.')
	output_weights_plural = embeddings[idx_verbs_plural, from_unit]
	ax.scatter(u + np.random.random(output_weights_plural.size) * bar_width - bar_width/2, output_weights_plural, s=30, color=args.colors[u], label=label_plur, marker='_')


plt.legend()
plt.xticks(range(len(units)), [str(u) for u in units])
ax.set_ylabel('Size of output weight', fontsize = 16)
ax.set_xlabel('Unit', fontsize = 16)
ax.axhline(linewidth=2, color='k', ls = '--')
fig.savefig(os.path.join(dirname, 'weight_dists_'+filename))
print('saved to: ' + os.path.join(dirname, 'weight_dists_'+filename))
plt.close(fig)

