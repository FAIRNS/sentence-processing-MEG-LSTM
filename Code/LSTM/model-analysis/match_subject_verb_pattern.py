import os, sys, pickle, random
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import argparse
#matplotlib.use('TKAgg',warn=False, force=True)

parser = argparse.ArgumentParser(description='Identify subject-verb dependency patterns in unit activations')
parser.add_argument('-t', '--task', default='nounpp', help='NA-task (nounpp/subjrel_that/objrel_that')
parser.add_argument('-v', '--variable', default='hidden', help='Variable in activations (hidden/cell)')
parser.add_argument('-o', '--path2output', default='../../../Figures/', help='path to output figure (filename included)')
parser.add_argument('--lang', default='english', help='language: english/Italian')
parser.add_argument('--subject-pos', default=2, help='Subject position (counting from 1!) - e.g., "The BOY near the car greets"')
parser.add_argument('--verb-pos', default=6, help='Verb position (counting from 1!) - e.g., "The boy near the car GREETS"')
args = parser.parse_args()
print(args)

args.path2output = os.path.join(args.path2output, args.lang + '_' + args.variable + '_dependency_pattern.png')


# path
path = sys.path[0].split('/')
i = path.index('sentence-processing-MEG-LSTM')
base_folder = os.sep + os.path.join(*path[:i+1])
# base_folder = '/home/yl254115/Projects/FAIRNS'

# Input
data_file = os.path.join(base_folder, 'Data/LSTM/activations', args.lang, args.task + '.pkl')


# Load LSTM activations
LSTM_activations = pickle.load(open(data_file, 'rb'))

metric_all_units_all_sentences = []
for activation_pattern in LSTM_activations[args.variable]:
    curr_sentence_metric = np.ones(1300)

    # for pos in range(subject_position + 1, verb_position):

    #for pos in range(subject_position+1):
    #    curr_sentence_metric = np.min(np.vstack((1-np.abs(activation_pattern[:, pos]), curr_sentence_metric)), axis=0)
    for pos in range(args.subject_pos+1, args.verb_pos):
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
plt.savefig(args.path2output)
print('Figure saved to: ' + args.path2output)
#plt.show()
