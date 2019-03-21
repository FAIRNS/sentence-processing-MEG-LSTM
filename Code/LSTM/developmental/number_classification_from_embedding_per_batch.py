from functions.classification_from_embedding import get_classification_accuracy
import argparse
import os, glob

parser = argparse.ArgumentParser(description='PyTorch Wikitext-2 RNN/LSTM Language Model')
# parser.add_argument('--path2models', type=str, default='../../../../../LSTM_training/word_language_model/output/', help='path to pt models for all epochs/batches with filenames: "epoch-%i-batch-%i-*.pt"')
parser.add_argument('--path2models', type=str, default='../../../Data/LSTM/', help='path to pt models for all epochs/batches with filenames: "epoch-%i-batch-%i-*.pt"')
parser.add_argument('--path2nouns', type=str, default='../../../Data/Stimuli/singular_plural_nouns.txt', help='path to file containing singular and plural nouns (1st/2nd column sg/pl,tab delimted)')
parser.add_argument('--path2verbs', type=str, default='../../../Data/Stimuli/singular_plural_verbs.txt', help='path to file containing singular and plural verbs (1st/2nd column sg/pl,tab delimted)')
parser.add_argument('-v', '--vocabulary', default='../../../Data/LSTM/english_vocab.txt')
parser.add_argument('-o', '--output', default='Figures/verbs.png', help='Destination for the output figure')

args = parser.parse_args()

epochs = []; batches = []; accs_nouns = []; accs_verbs = []
models_files = sorted(glob.glob(os.path.join(args.path2models, 'epoch*.pt')))
for i, model_fn in enumerate(models_files):
    info = model_fn.split('-')
    epoch = int(info[1])
    batch = int(info[3])
    acc_nouns, acc_verbs = get_classification_accuracy(model_fn, args.vocabulary, args.path2nouns, args.path2verbs)
    epochs.append(epoch)
    batches.append(batch)
    accs_nouns.append(acc_nouns)
    accs_verbs.append(acc_verbs)
    print('Accuracy for nouns, epoch %i, batch %i: %f' % (epoch, batch, acc_nouns))
    print('Accuracy for verbs, epoch %i, batch %i: %f' % (epoch, batch, acc_verbs))
