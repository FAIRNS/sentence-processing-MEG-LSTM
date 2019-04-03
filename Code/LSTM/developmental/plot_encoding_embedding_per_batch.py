fn = '../../../Output/encoding_embedding_classification_per_batch.txt'
fn_NA_perf = '../../../Output/NA_performance_per_batch.txt'

with open(fn, 'r') as f:
    data = f.readlines()

epochs = []
batches = []
acc_nouns = []
acc_verbs = []
for line in data:
    epochs.append(int(line.split(',')[0]))
    batches.append(int(line.split(',')[1]))
    acc_nouns.append(float(line.split(',')[2]))
    acc_verbs.append(float(line.split(',')[3]))

import numpy as np
max_batch = np.max(batches)
abs_batches = []
for e, b in zip(epochs, batches):
    abs_batches.append((e-1)*max_batch+b)

IX = np.argsort(abs_batches)
abs_batches = np.asarray(abs_batches)[IX]
acc_nouns = np.asarray(acc_nouns)[IX]
acc_verbs = np.asarray(acc_verbs)[IX]


with open(fn_NA_perf, 'r') as f:
    data = f.readlines()

abs_batches_NA = []
acc_NA = []
for line in data:
    abs_batches_NA.append(int(line.split(',')[0]))
    acc_NA.append(float(line.split(',')[1]))
IX = np.argsort(abs_batches_NA)
abs_batches_NA = np.asarray(abs_batches_NA)[IX]
acc_NA = np.asarray(acc_NA)[IX]

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(abs_batches, acc_nouns, color='b', label='nouns')
ax.plot(abs_batches, acc_verbs, color='g', label='verbs')
ax.plot(abs_batches_NA, acc_NA, color='k', label='NA performance')
plt.legend()
plt.savefig('../../../Figures/develop_acc.png')
