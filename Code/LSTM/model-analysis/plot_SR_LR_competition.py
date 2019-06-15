import pickle, sys, os
import matplotlib.pyplot as plt
import numpy as np
import torch
import argparse
from tqdm import tqdm
from sklearn import svm
from sklearn.model_selection import cross_val_score
import re
import pandas

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/word_language_model')))
import data


def parseNumList(string):
    m = re.match(r'(\d+)(?:-(\d+))?$', string)
    # ^ (or use .split('-'). anyway you like.)
    if not m:
        raise argparse.ArgumentTypeError("'" + string + "' is not a range of number. Expected forms like '0-5' or '2'.")
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start,10), int(end,10)))



parser = argparse.ArgumentParser(description='Find short-range (SR) units')
parser.add_argument('--model', type=str, default='../../../Data/LSTM/models/english/hidden650_batch128_dropout0.2_lr20.0.pt', help='pytorch model')
parser.add_argument('-i', '--input', default='../../../Data/Stimuli/nounpp', help='Filename without extension for Tal\'s setup (text, gold and info)')
parser.add_argument('-v', '--verbs', default='../../../Data/Stimuli/singular_plural_verbs.txt',
					help='Text file with two tab delimited columns with the lists of output words to contrast with the PCA')
parser.add_argument('--lr-units', default=[769, 987, 775], nargs='+', help='Long-range unit numbers - counting from ZERO!')
parser.add_argument('--sr-units', default=[1282, 1283, 772, 905, 1035, 1167, 1295, 655, 1042, 1171, 916, 661, 1052, 796, 925, 671, 1055, 1058, 1065, 681, 682, 684, 939, 1199, 1202, 1203, 950, 952, 1210, 699, 1214, 702, 831, 833, 714, 972, 847, 975, 978, 1235, 851, 853, 856, 857, 1115, 745, 1006, 1264, 884], nargs='+', help='Short-range unit numbers - counting from ZERO!')
parser.add_argument('-c', '--conditions', default=[['singular', 'singular'], ['singular', 'plural'], ['plural', 'singular'], ['plural', 'plural']], nargs='+', help='Short-range unit numbers - counting from ZERO!')
parser.add_argument('--vocabulary', default='../../../Data/LSTM/english_vocab.txt')
parser.add_argument('-o', '--output-file-name', type=str, default='../../../Figures/SR_LR_interplay.png', help='Path to final figure')
parser.add_argument('--cuda', action='store_true', default=False)
parser.add_argument('--use-unk', action='store_true', default=True)
parser.add_argument('--lang', default='en')
parser.add_argument('--unk-token', default='<unk>')
args = parser.parse_args()
print(args)

SR_units = [u-650 for u in args.sr_units]
LR_units = [u-650 for u in args.lr_units]

metadata = pickle.load(open(args.input + '.info', 'rb'))

gold = pandas.read_csv(args.input + '.gold', sep='\t', header=None, names=['verb_pos', 'correct', 'wrong', 'nattr'])

vocab = data.Dictionary(args.vocabulary)
sentences = []
for l in open(args.input + '.text'):
    sentences.append(l.rstrip('\n').split(" "))
sentences = np.array(sentences)

with open(args.verbs, 'r') as f:
    lines = f.readlines()
verbs_singular = [l.split('\t')[0].strip() for l in lines]
IX_verbs_singular = [vocab.word2idx[w] for w in verbs_singular]
verbs_plural = [l.split('\t')[1].strip() for l in lines]
IX_verbs_plural = [vocab.word2idx[w] for w in verbs_plural]
verbs_all = verbs_singular + verbs_plural
print('\nWords used (group 1):')
print(verbs_singular)
print('\nWords used (group 2):')
print(verbs_plural)

print('Loading models...', file=sys.stderr)
sentence_length = [len(s) for s in sentences]
max_length = max(*sentence_length)
import lstm
model = torch.load(args.model, lambda storage, loc: storage)
model.rnn.flatten_parameters()
# hack the forward function to send an extra argument containing the model parameters
model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)
embeddings_out = model.decoder.weight.data.cpu().numpy()
bias_out = model.decoder.bias.data.cpu().numpy()

def feed_sentence(model, h, sentence):
    outs = []
    for w in sentence:
        out, h = feed_input(model, h, w)
        outs.append(torch.nn.functional.log_softmax(out[0]).unsqueeze(0))
    return outs, h

def feed_input(model, hidden, w):
    if w not in vocab.word2idx and args.use_unk:
        print('unk word: ' + w)
        w = args.unk_token
    inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
    if args.cuda:
        inp = inp.cuda()
    out, hidden = model(inp, hidden)
    return out, hidden

print('Extracting LSTM representations', file=sys.stderr)
# output buffers
a_plural_minus_singular_SR_all_sentences = [np.zeros(len(s)) for s in tqdm(sentences)] # np.zeros((len(sentences), max_length))
a_plural_minus_singular_LR_all_sentences = [np.zeros(len(s)) for s in tqdm(sentences)]

if args.lang == 'en':
    init_sentence = " ".join(["In service , the aircraft was operated by a crew of five and could accommodate either 30 paratroopers , 32 <unk> and 28 sitting casualties , or 50 fully equipped troops . <eos>",
                    "He even speculated that technical classes might some day be held \" for the better training of workmen in their several crafts and industries . <eos>",
                    "After the War of the Holy League in 1537 against the Ottoman Empire , a truce between Venice and the Ottomans was created in 1539 . <eos>",
                    "Moore says : \" Tony and I had a good <unk> and off-screen relationship , we are two very different people , but we did share a sense of humour \" . <eos>",
                    "<unk> is also the basis for online games sold through licensed lotteries . <eos>"])
elif args.lang == 'it':
    init_sentence = " ".join(['Ma altre caratteristiche hanno fatto in modo che si <unk> ugualmente nel contesto della musica indiana ( anche di quella \" classica \" ) . <eos>',
    'Il principio di simpatia non viene abbandonato da Adam Smith nella redazione della " <unk> delle nazioni " , al contrario questo <unk> allo scambio e al mercato : il <unk> produce pane non per far- ne dono ( benevolenza ) , ma per vender- lo ( perseguimento del proprio interesse ) . <eos>'])
else:
    # init_sentence = " ".join([
    # "hier , considéré avec scepticisme du fait de la présence du minitel , le réseau connaît aujourd'hui un véritable engouement . </s>",
    # "le débat est ouvert . </s>",
    # "précise le guardian . </s>",
    # "c' est plus ou moins ce que fait actuellement honda au japon avec leur série de robots humanoïdes . </s>",
    # "| alstom mise sur l' automotrice à grande vitesse pour remplacer le tgv ! </s>",
    # "je ne vois donc plus la vie de la même façon . </s>",
    # "a vierzon , rendez -vous le 20 novembre à 10h30 , forum république appels à mobilisation pas de commentaire \" dimanche , 18 . </s>",
    # "faut -il avoir la nationalité française pour adhérer ? </s>",
    # "- sauf que là c' est pas en colombie , c' est en russie . </s>"])
    init_sentence = "</s>"
hidden = model.init_hidden(1)
init_sentence = [s.lower() for s in init_sentence.split(" ")]
_, init_h = feed_sentence(model, hidden, init_sentence)

# init dict for conditions

results_dict_per_condition = {}
for condition in args.conditions:
    results_dict_per_condition['_'.join(condition)] = {'SR':[], 'LR':[], 'others':[], 'bias':[]}


# Loop over sentences
for i, (s, info) in enumerate(tqdm(zip(sentences, metadata))):
    curr_condition = info['number_1'] + '_' + info['number_2']
    verb_correct, verb_wrong = gold.loc[i,'correct'], gold.loc[i,'wrong']
    hidden = init_h
    curr_SR = []; curr_LR = []; curr_others = []
    for j, w in enumerate(s):
        if w not in vocab.word2idx and args.use_unk:
            print('unk word: ' + w)
            w = args.unk_token
        inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
        if args.cuda:
            inp = inp.cuda()
        out, hidden = model(inp, hidden)
        h_2nd_layer = hidden[0].data.cpu().numpy()[1,:,:]

        a_words_SR = np.matmul(embeddings_out[:, SR_units], np.transpose(h_2nd_layer[0, SR_units]))
        a_words_LR = np.matmul(embeddings_out[:, LR_units], np.transpose(h_2nd_layer[0, LR_units]))
        other_units = list(set(range(650)) - set(SR_units + LR_units))
        a_words_others = np.matmul(embeddings_out[:, other_units], np.transpose(h_2nd_layer[0, other_units]))\
        #+ bias_out
        # print(a_words_LR + a_words_SR + a_words_others) # check that sum up to out

        a_correct_verb_from_SR = a_words_SR[vocab.word2idx[verb_correct]]
        a_correct_verb_from_LR = a_words_LR[vocab.word2idx[verb_correct]]
        a_correct_verb_from_other = a_words_others[vocab.word2idx[verb_correct]]

        a_wrong_verb_from_SR = a_words_SR[vocab.word2idx[verb_wrong]]
        a_wrong_verb_from_LR = a_words_LR[vocab.word2idx[verb_wrong]]
        a_wrong_verb_from_others = a_words_others[vocab.word2idx[verb_wrong]]

        # a_all_singular_verbs_from_SR = a_words_SR[IX_verbs_singular]
        # a_all_singular_verbs_from_LR = a_words_LR[IX_verbs_singular]
        #
        # a_all_plural_verbs_from_SR = a_words_SR[IX_verbs_plural]
        # a_all_plural_verbs_from_LR = a_words_LR[IX_verbs_plural]

        curr_SR.append(a_correct_verb_from_SR - a_wrong_verb_from_SR)
        curr_LR.append(a_correct_verb_from_LR - a_wrong_verb_from_LR)
        curr_others.append(a_correct_verb_from_other - a_wrong_verb_from_others)

    results_dict_per_condition[curr_condition]['SR'].append(curr_SR)
    results_dict_per_condition[curr_condition]['LR'].append(curr_LR)
    results_dict_per_condition[curr_condition]['others'].append(curr_others)

        # a_plural_minus_singular_SR_all_sentences[i][j] = a_plural_verbs_from_SR - a_singular_verbs_from_SR
        # a_plural_minus_singular_LR_all_sentences[i][j] = a_plural_verbs_from_LR - a_singular_verbs_from_LR
with open('results.pkl', 'wb') as f:
    pickle.dump(results_dict_per_condition, f)