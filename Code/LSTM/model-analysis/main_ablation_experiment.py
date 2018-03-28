import os, pickle
import numpy as np
import pandas as pd
import sys
sys.path.append(os.path.abspath('../src/word_language_model'))
import data

script = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py'
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model.tab'
agreement_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model_sentences.txt'
vocab = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/test_output'
eos = '"<eos>"'
format = 'pkl'


agreement_test_data = pd.read_csv(agreement_data, sep='\t')
test_sentences = [s[13] for s in agreement_test_data._values]
test_sentences = [s for i,s in enumerate(test_sentences) if i%2==1]
vocab = data.Dictionary(vocab)
IX_bad_sentences = []
for i, s in enumerate(test_sentences):
    for w in s.split():
        try:
            ix = vocab.word2idx[w]
            print ix
        except:
            IX_bad_sentences.append(i)
            break
test_sentences = [s for i,s in enumerate(test_sentences) if not (i in IX_bad_sentences)]

with open(agreement_sentences, 'wb') as f:
    for s in test_sentences:
        f.write("%s\n" % s)



cmd = script + ' ' + model + ' --input ' + agreement_sentences + ' --vocabulary ' + vocab + ' --output ' + output + ' --eos-separator ' + eos + ' --format ' + format
print cmd
os.system(cmd)


if format == 'pkl':
    with open(output + '.' + format, 'r') as f:
        curr = pickle.load(f)
elif format == 'npz':
    curr = np.load(output + '.' + format)

print curr
#
# # Omit sentences with words outside the vocab
# IX_bad_sentences = []
# for i, s in enumerate(sentences_prefix):
#     print i
#     for w in s.split():
#         # if w not in vocab.word2idx.keys():
#         try:
#             ix = vocab.word2idx[w]
#             print ix
#         except:
#             IX_bad_sentences.append(i)
#             break
# sentences_prefix = [s for i, s in enumerate(sentences_prefix) if not (i in IX_bad_sentences)]
# correct_wrong = [s for i, s in enumerate(correct_wrong) if not (i in IX_bad_sentences)]
# verbs = [s for i, s in enumerate(verbs) if not (i in IX_bad_sentences)]
# len_context = [s for i, s in enumerate(len_context) if not (i in IX_bad_sentences)]
# len_prefix = [s for i, s in enumerate(len_prefix) if not (i in IX_bad_sentences)]
# log_p = [s for i, s in enumerate(log_p) if not (i in IX_bad_sentences)]