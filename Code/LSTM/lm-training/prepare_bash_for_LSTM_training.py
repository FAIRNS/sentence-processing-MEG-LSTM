
print('python3 main.py --cuda --emsize 650 --nhid 650 --nlayers 2 --dropout 0.2 --epochs 10 --save /neurospin/unicog/protocols/Yair/LSTM_training/output/model_.pt --data /neurospin/unicog/protocols/Yair/LSTM_training/word_language_mode/data/wiki_kristina/')

for seed in list(range(1)) + [1110]:
    seed += 1
    cmd = 'python3 main.py --cuda --seed ' + str(seed) + ' --emsize 650 --nhid 650 --nlayers 2 --dropout 0.2 --epochs 10 --save /volatile/FAIRNS/LSTM_training/model_%i.pt --data data/wiki_kristina/ > train_%i.log ' % (seed, seed)
    print(cmd)
