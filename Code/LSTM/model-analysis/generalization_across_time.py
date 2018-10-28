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
parser.add_argument('--gat',  action='store_true', default=False, help='Plot also generalization across time matrices')
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

    from sklearn.svm import LinearSVC
    clf2 = LinearSVC(random_state=0, tol=1e-5, penalty='l2')
    clf2.fit(X_train[:, :, 1], y_train)
    print('Units with highest weights of a classifier trained to predict subject''s number:')
    print([(i, j) for (i, j) in zip(np.transpose(np.argsort(np.negative(np.abs(clf2.coef_))))[0:20], np.transpose(np.sort(np.negative(np.abs(clf2.coef_))))[0:20])])

    # ###### ALSO RUN RIDGE AND LASSO REGRESSION:
    # from sklearn import linear_model
    # from sklearn.model_selection import GridSearchCV
    #
    # alphas = [0.1, 0.5, 1, 10]
    # tuned_parameters = [{'alpha': alphas}]
    # model_ridge = GridSearchCV(linear_model.Ridge(), tuned_parameters, cv=5, refit=True, return_train_score=True)
    # model_ridge.fit(X_train[:,:,1], y_train)
    # model_ridge.alphas = alphas
    # print(np.transpose(np.argsort(np.negative(np.abs(model_ridge.best_estimator_.coef_))))[0:20],
    #       np.transpose(np.sort(np.negative(np.abs(model_ridge.best_estimator_.coef_))))[0:10])



    # alphas, coefs_lasso, _ = linear_model.lasso_path(X_train[:,:,1], y_train, fit_intercept=True)
    # # Grid search - calculate train/validation error for all regularization sizes
    # lasso = linear_model.Lasso()
    # tuned_parameters = [{'alpha': alphas}]
    # model_lasso = GridSearchCV(lasso, tuned_parameters, cv=5, return_train_score=True, refit=True)
    # model_lasso.fit(X_train[:,:,1], y_train)
    #
    # model_lasso.alphas = alphas
    # model_lasso.coefs = np.transpose(coefs_lasso)

    return scores

def add_gat_matrix(ax1, ax2, data, omit_units, title, first_in_row=True, last_row=True):
    # Generalization across time
    im = None
    # print(omit_units)
    if omit_units != 'non_number_units':
        data_reduced = np.delete(data, omit_units, 1)
        epochs, _, _ = generate_epochs_object(data_reduced)
        scores_reduced_model = get_scores_from_gat(epochs)
        # Add to 1d figure
        ax1.plot(range(scores_reduced_model.shape[1]), scores_reduced_model[1, :], linewidth=3, label=title)
        # Add to 2d GAT matrix figure
        tmin = int(epochs.times[0])
        tmax = int(epochs.times[-1])+1
        extent = [tmin, tmax, tmin, tmax]
        ticks = [i+0.5 for i in range(tmin, tmax)]
        if args.gat:
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
    else:
        scores_reduced_model_all = []
        number_units = [702, 769, 775, 847, 987, 1282]
        for unit in list(set(range(650, 1300)) - set(number_units)):
            print('unit ' + str(unit))
            omit_units = list(set(range(data.shape[1])) - set([unit]))
            data_reduced = np.delete(data, omit_units, 1)
            epochs, _, _ = generate_epochs_object(data_reduced)
            scores_reduced_model = get_scores_from_gat(epochs)
            scores_reduced_model_all.append(scores_reduced_model[1, :])
        scores_reduced_model_all = np.vstack(scores_reduced_model_all)
        # Add to 1d figure
        ax1.errorbar(x=range(scores_reduced_model.shape[1]), y=np.mean(scores_reduced_model_all, axis=0), yerr=np.std(scores_reduced_model_all, axis=0), linewidth=3, label=title, color='k')

    return im


#### Load data
metadata = pickle.load(open(args.metadata, 'rb'))
data = pickle.load(open(args.activations, 'rb'))
data = np.dstack(data[args.gate])
data = np.moveaxis(data, 2, 0) # num_trials X num_units X num_timepoints
with open(args.sentences, 'r') as f:
    sentences = f.readlines()
sentences = [s.split(' ') for s in sentences]

num_omits = len(args.omit_units); num_keeps = len(args.keep_units)
num_subplots_rows = int(np.floor(np.sqrt(num_keeps+num_omits+1)))
num_subplots_cols = int(np.ceil((num_keeps+num_omits+1)/num_subplots_rows))
#### Plot Full model
fig1, ax = plt.subplots(1)
axs = [None] * (num_keeps+num_omits+1)
if args.gat:
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
    first_in_row = True if (cnt % num_subplots_cols) == 0 else False
    last_row = True if np.ceil((cnt + 1) / num_subplots_cols) == num_subplots_rows else False
    if keep_units[0] == 'non_number_units':
        omit_units = keep_units[0]
        title = keep_units[0]
    else:
        omit_units = list(set(range(data.shape[1])) - set(map(int, keep_units)))
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
if args.gat:
    fig2.subplots_adjust(left=0.15, right=0.8, bottom = 0.18) #, wspace = 0.5)
    for a in range(cnt, len(axs)): axs[a].remove() # Omit empty plots from subplots figure
    cbar = plt.axes([0.85, 0.3, 0.05, 0.45])
    cbar1=plt.colorbar(im, cax=cbar)
    cbar1.set_label('AUC', fontsize=16, rotation=270, labelpad=20)
    fig2.text(0.5, 0.03, 'Testing Time (s)', ha='center')
    fig2.text(0.03, 0.5, 'Training Time (s)', va='center', rotation='vertical')
    fig2.savefig(os.path.join(path2figures, 'GAT2d_' + filename))

print('Figures were saved to: ' + os.path.join(path2figures, 'GAT?d_' + filename))