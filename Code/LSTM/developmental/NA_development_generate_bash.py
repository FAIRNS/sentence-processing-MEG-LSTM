import os, pickle

#seed = 1111
for epoch in range(1,11):
    st = 22000 if epoch == 1 else 200
    for batch in range(st, 123000, 200):
        ablation_script = 'Code/LSTM/model-analysis/ablation-experiment.py'
        filename_model = '/neurospin/unicog/protocols/Yair/LSTM_training/word_language_model/output/epoch-%i-batch-%i-model.pt' % (epoch, batch)
        input = "--input Data/Stimuli/nounpp"
        vocab = "--vocabulary Data/LSTM/models/english_vocab.txt"
        output = "--output Output/english_nounpp_epoch_%i_batch_%i" % (epoch, batch)
        rest = '--eos-separator "<eos>" --format pkl -u 1 -u 750 -g 1 -s 1 --cuda'
        cmd = 'python3 ' + ' '.join([ablation_script, filename_model, input, vocab, output, rest])
        print(cmd)

