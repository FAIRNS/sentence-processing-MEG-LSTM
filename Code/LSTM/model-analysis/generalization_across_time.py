import os, mne, argparse, pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from mne.decoding import GeneralizingEstimator
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Generalization across time')
parser.add_argument('-s', '--sentences', type=str, help='Path to text file containing the list of sentences to analyze')
parser.add_argument('-m', '--metadata', type=str, help='The corresponding meta data of the sentences')
parser.add_argument('-a', '--activations', '--LSTM-file-name', type=str, help='The corresponding sentence (LSTM) activations')
parser.add_argument('-g', '--gate', type=str, help='One of: gates.in, gates.forget, gates.out, gates.c_tilde, hidden, cell')
parser.add_argument('-o', '--output-file-name', type=str, help='Path to output folder for figures')
parser.add_argument('-l', '--omit-units', nargs = '+', action = 'append', type=str, default = [], help='Which units to omit from the model')
parser.add_argument('-k', '--keep-units', nargs='+', action='append', type=str, default = [], help='Which units to keep in the model')
args = parser.parse_args()


def generate_events_object(metadata):
    events = np.empty((0, 3), dtype = int)
    cnt = 0; IX = []
    for i, curr_info in enumerate(metadata):
        if curr_info['number_1'] == 'plural' and curr_info['number_2'] == 'singular' and curr_info['success'] == 'correct':
            curr_line = np.asarray([cnt, 0, 1])
            events = np.vstack((events, curr_line)); cnt += 1
            IX.append(i)
        elif curr_info['number_1'] == 'singular' and curr_info['number_2'] == 'plural' and curr_info['success'] == 'correct':
            curr_line = np.asarray([cnt, 0, 2])
            events = np.vstack((events, curr_line)); cnt += 1
            IX.append(i)

    event_id = dict(singlar = 1, plural=2)
    return events, event_id, IX


def generate_epochs_object(data, sampling_rate = 1):
    n_channels = data[0].shape[0]
    info = mne.create_info(n_channels, sampling_rate)
    events, event_id, IX = generate_events_object(metadata)
    epochs = mne.EpochsArray(data[IX, :, :], info, events, 0, event_id)
    return epochs, events, IX


def get_scores_from_gat(epochs):
    X_train, X_test, y_train, y_test = train_test_split(epochs.get_data(), epochs.events[:, 2] == 2, test_size=0.2,
                                                        random_state=42)
    clf = make_pipeline(StandardScaler(), LogisticRegression())
    time_gen = GeneralizingEstimator(clf, scoring='roc_auc', n_jobs=1)
    time_gen.fit(X_train, y_train)
    scores = time_gen.score(X_train, y_train)
    return scores

def add_gat_matrix(ax1, ax2, data, omit_units, title, first_in_row=True, last_row=True):
    # Generalization across time
    data_reduced = np.delete(data, omit_units, 1)
    epochs, _, _ = generate_epochs_object(data_reduced)
    scores_reduced_model = get_scores_from_gat(epochs)
    # Add to 1d figure
    ax1.plot(scores_reduced_model[1, :], linewidth=3, label=title)
    # Add to 2d GAT matrix figure
    tmin = int(epochs.times[0])
    tmax = int(epochs.times[-1])+1
    extent = [tmin, tmax, tmin, tmax]
    ticks = [i+0.5 for i in range(tmin, tmax)]
    im = ax2.matshow(scores_reduced_model, vmin=0, vmax=1., cmap='RdBu_r', origin='lower', extent=extent)
    ax2.set_title(title, fontsize=12)
    ax2.xaxis.set_ticks_position('bottom')
    ax2.set_xlim([tmin, tmax])
    ax2.set_ylim([tmin, tmax])
    ax2.set_xticks(ticks)
    ax2.set_yticks(ticks)
    ax2.tick_params(axis=u'both', which=u'both', length=0)
    if last_row:  # Add xticks/labels only for last row
        ax2.set_xticklabels(sentences[0], rotation=90, fontsize=11)
    else:
        ax2.get_xaxis().set_visible(False)
    if first_in_row:
        ax2.set_yticklabels(sentences[0], fontsize=11)
    else:
        ax2.get_yaxis().set_visible(False)

    return im


#### Load data
metadata = pickle.load(open(args.metadata, 'rb'))
data = pickle.load(open(args.activations, 'rb'))
data = np.dstack(data[args.gate])
data = np.moveaxis(data, 2, 0) # num_trials X num_units X num_timepoints
with open(args.sentences, 'r') as f:
    sentences = f.readlines()
sentences = [s.split(' ') for s in sentences]

#### Plot Full model
fig1, ax = plt.subplots(1)
num_omits = len(args.omit_units); num_keeps = len(args.keep_units)
num_subplots_rows = int(np.floor(np.sqrt(num_keeps+num_omits+1)))
num_subplots_cols = int(np.ceil((num_keeps+num_omits+1)/num_subplots_rows))
fig2, axs = plt.subplots(num_subplots_rows, num_subplots_cols)
if num_subplots_cols > 1:
    axs = axs.flatten()
else:
    axs = [axs] # To make compatible with indexing of the case of many plots

omit_units = [] # Omit nothing (Full model)
title = 'Full model'
last_row = True if np.ceil(1/num_subplots_cols) == num_subplots_rows else False
im = add_gat_matrix(ax, axs[0], data, omit_units, title, first_in_row=True, last_row=last_row)

#### Reduced models (when omitting or keeping certain units from/in the model):
cnt = 1
for omit_units in args.omit_units: # When leaving out units
    omit_units = [int(u) for u in omit_units]
    first_in_row = True if (cnt % num_subplots_cols) == 0 else False
    last_row = True if np.ceil((cnt+1) / num_subplots_cols) == num_subplots_rows else False
    title = '-' + ','.join(map(str, omit_units))
    im = add_gat_matrix(ax, axs[cnt], data, omit_units, title, first_in_row=first_in_row, last_row=last_row)
    cnt += 1

for keep_units in args.keep_units: # When keeping only some units
    # Generalization across time (reduced model)
    omit_units = list(set(range(data.shape[1])) - set(map(int, keep_units)))
    first_in_row = True if (cnt % num_subplots_cols) == 0 else False
    last_row = True if np.ceil((cnt+1) / num_subplots_cols) == num_subplots_rows else False
    title = '+' + ','.join(map(str, keep_units))
    im = add_gat_matrix(ax, axs[cnt], data, omit_units, title, first_in_row=first_in_row, last_row=last_row)
    cnt += 1

#### Cosmetics and save figures
path2figures, filename = os.path.split(args.output_file_name)
# Fig 1d
fig1.subplots_adjust(right=0.6)
ax.axhline(0.5, color='k', ls = '--')
ax.axvline(4, color='r', ls = '-.')
ax.set_xticklabels(sentences[0], rotation=30, fontsize=11)
ax.set_ylabel('AUC', fontsize = 16)
ax.set_title('Training time - first noun')
ax.set_ylim((0, 1.05))
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig1.savefig(os.path.join(path2figures, 'GAT1d_' + filename))

# Fig 2d
fig2.subplots_adjust(left=0.15, right=0.8, bottom = 0.18) #, wspace = 0.5)
for a in range(cnt, len(axs)): axs[a].remove() # Omit empty plots from subplots figure
cbar = plt.axes([0.85, 0.3, 0.05, 0.45])
cbar1=plt.colorbar(im, cax=cbar)
cbar1.set_label('AUC', fontsize=16, rotation=270, labelpad=20)
fig2.text(0.5, 0.03, 'Testing Time (s)', ha='center')
fig2.text(0.03, 0.5, 'Training Time (s)', va='center', rotation='vertical')
fig2.savefig(os.path.join(path2figures, 'GAT2d_' + filename))

print('Figures were saved to: ' + os.path.join(path2figures, 'GAT?d_' + filename))