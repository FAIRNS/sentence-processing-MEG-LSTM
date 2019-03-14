from functions.get_model_perplexity import get_model_perplexity
import argparse
import os, glob

parser = argparse.ArgumentParser(description='PyTorch Wikitext-2 RNN/LSTM Language Model')
parser.add_argument('--val-data', type=str, default='../lm-training/data/en/wikitext-2/valid.txt', help='location of the data corpus')
parser.add_argument('--path2models', type=str, default='../../../../../LSTM_training/word_language_model/output/', help='path to model')
parser.add_argument('--bptt', type=int, default=35, help='sequence length')
parser.add_argument('--ntokens', type=int, default=50001, help='Vocabulary size (default for English)')
parser.add_argument('--cuda', action='store_true', help='use CUDA')
args = parser.parse_args()

epochs = []; batches = []; perps = []
models_files = sorted(glob.glob(os.path.join(args.path2models, 'epoch*.pt')))
for i, model_fn in enumerate(models_files):
    info = model_fn.split('-')
    epoch = int(info[1])
    batch = int(info[3])
    perp = get_model_perplexity(model_fn, args.val_data, args.bptt, args.ntokens, args.cuda)
    epochs.append(epoch)
    batches.append(batch)
    perps.append(perp)
    print('Perplexity for epoch %i, batch %i: %f' % (epoch, batch, perp))
