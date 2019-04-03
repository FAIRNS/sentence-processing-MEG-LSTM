import os, sys, pickle, random
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('TKAgg',warn=False, force=True)

# inp
path = sys.path[0].split('/')
i = path.index('sentence-processing-MEG-LSTM')
base_folder = os.sep + os.path.join(*path[:i+1])

# number for filtering
variable = 'hidden'

# base_folder = '/home/yl254115/Projects/FAIRNS'
data_file = os.path.join(base_folder, 'Data/LSTM/activations/Italian/nounpp.pkl')

subject_position = 2 # counting from one (e.g., 'The BOY near the car greets..')
verb_position = 6    # counting from one (e.g., 'The boy near the car GREETS..')

# Load LSTM activations
LSTM_activations = pickle.load(open(data_file, 'rb'))

metric_all_units_all_sentences = []
for activation_pattern in LSTM_activations[variable]:
    curr_sentence_metric = np.ones(1300)

    # for pos in range(subject_position + 1, verb_position):

    for pos in range(subject_position):
        curr_sentence_metric = np.min(np.vstack((1-np.abs(activation_pattern[:, pos]), curr_sentence_metric)), axis=0)
    for pos in range(subject_position, verb_position):
        curr_sentence_metric = np.min(np.vstack((np.abs(activation_pattern[:, pos]), curr_sentence_metric)), axis=0)
    # curr_sentence_metric /= verb_position - subject_position - 1

    metric_all_units_all_sentences.append(curr_sentence_metric)

metric_all_units_average_across_sentences = np.average(np.asarray(metric_all_units_all_sentences), axis=0)
IX = np.argsort(-metric_all_units_average_across_sentences)
print(IX[0:10])
print(metric_all_units_average_across_sentences[IX][0:10])

# Plot dist metric across all sentences
fig, ax = plt.subplots(figsize=(10,10))
# ax.hist(np.asarray(metric_all_units_all_sentences)[:, 1149])
ax.hist(metric_all_units_average_across_sentences, 100)
ax.set_ylim((0, 10))
ax.set_ylabel('Number of units', fontsize = 16)
ax.set_xlabel('Subject-verb dependency encoding', fontsize = 16)
plt.savefig('../../../Figures/syntax_subject_verb_dependency_metric.png')
plt.show()
