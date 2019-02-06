
for seed in list(range(10)) + [1110]:
    seed += 1
    cmd = 'python main.py --cuda --seed ' + str(seed) + ' --batch_size 128 --emsize 650 --nhid 650 --nlayers 2 --dropout 0.2 --epochs 200 --save /volatile/FAIRNS/LSTM_training/model_%i.pt --data data/wiki_kristina/ > train_%i.log ' % (seed, seed)
    print(cmd)