for seed in list(range(10)) + [1110]:
    seed += 1
    cmd = 'python main.py --cuda --seed ' + str(seed) + ' --emsize 650 --nhid 650 --nlayers 2 --dropout 0.2 --epochs 40 --batch_size 128 --save /volatile/FAIRNS/LSTM_training/model_seed_%i.pt --data data/wiki_kristina/ > train_%i.log ' % (seed, seed)
    print(cmd)
