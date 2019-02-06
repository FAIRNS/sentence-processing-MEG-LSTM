import os, pickle

seed = 1111
for epoch in range(1,50):
    ablation_script = 'Code/LSTM/model-analysis/ablation-experiment.py'
    filename_model = '/volatile/FAIRNS/LSTM_training/inter-%i-model_seed_%i.pt' % (epoch, seed)
    input = "--input Data/Stimuli/nounpp"
    vocab = "--vocabulary Data/LSTM/english_vocab.txt"
    output = "--output Output/nounpp_seed_%i_%i" % (epoch, seed)
    rest = '--eos-separator "<eos>" --format pkl -u 1 -u 750 -g 1 -s 1 --cuda'
    cmd = 'python3 ' + ' '.join([ablation_script, filename_model, input, vocab, output, rest])
    print(cmd)


perf = [0.5]
for epoch in range(1,51):
    filename = 'Output/nounpp_seed_%i_1111.abl' % epoch
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            results = pickle.load(f)
            perf.append(results['score_on_task']/results['num_sentences'])

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(range(len(perf)), perf)
ax.set_xlabel('Epoch', fontsize=16)
ax.set_ylabel('Performance on the nounPP NA-task', fontsize=16)
fig.savefig(os.path.join('Figures', 'English_network_development.png'))
#plt.show()
