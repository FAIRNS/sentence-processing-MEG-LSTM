import pickle
import random
import numpy as np
import itertools
from collections import defaultdict

class Data(object):

    def __init__(self):
        self.data = []
        self.activations = False

    def add_corpus(self, txt_file, separator='|', 
                   column_names=['sentence', 'structure', 
                                 'open_nodes_count', 
                                 'adjacent_boundary_count'],
                                  **kwargs):
        """
        Creates a list of dictionaries representing all sentences in
        the input corpus, as well as potential metadata provided.
        Additional features of the sentence may be computed using
        **compute
        List of dictionaries is set as attribute to self.
        Args:
            txt file:       txt file with data and meta data
            separator:      separator used for input data, by default 
                            set to \'|\', following Marco\'s script.
            column_names:   names of the colums in the input file, by default set
                            to the names of the columns in Marco\'s script
            **kwargs:       additional things that should be computed
                            can be provided via functions that operate
                            on the split input from the txt file.
        """
        f = open(txt_file, 'rb')

        for line in f:
            vals = str(line).split(separator)
            vals[0]=vals[0][2::]
            self.data.append(dict(zip(column_names, vals)))
            length = len(vals[0].split())
            self.data[-1]['length'] = length
            word_pos = [i for i in range(len(vals[0]))]
            self.data[-1]['word_pos'] = word_pos
            for key, val in kwargs.items():
                self.data[-1][key] = val(line)

        return

    def add_activation_data(self, model, vocab, eos, unk, use_unk, lang, get_representations):
        """
        Add activation data to the sentences, based on
        a given model.

        Args
            model:      a pytorch language model
            vocab:      a txt file with the vocabulary of the model
                        (each line containing a word, order corresponding
                        with the embedding matrix)
            eos:        the eos token of the model
            unk:        the unknown token of the model
            use_unk:    whether the unknown token should be used
            lang:       language of the model
            get_representations:
                        The type of representations to fetch for each word
        """
        sentences = [s_dict['sentence'] for s_dict in self.data]
        activations = self.compute_activations(input=sentences, model=model, vocabulary=vocab, perplexity=False,
                    eos_separator=eos, fixed_length_arrays=False, cuda=False,
                    get_representations=get_representations, use_unk=use_unk, lang=lang, unk_token=unk,
                    kbow_value=2)
        for c, s_dict in enumerate(self.data):
            for key in activations.keys():
                s_dict[key] = activations[key][c]

        return

    def add_word_frequency_counts(self, word_frequencies):
        """
        Add word frequencies for all words in the sentences,
        read from an input file with word frequencies.

        Args:
            word_freqs:     a file with word frequences, tab separated
        """
        freq_dict = self.get_word_freqs(word_frequencies)

        for sent_dict in self.data:
            sentence = sent_dict['sentence']
            freqs = ' '.join([freq_dict.get(w, '0') for w in sentence.split()])
            sent_dict['word_frequencies'] = freqs

        return

    def split_data(self, fold=5, split=0.1):
        """
        Simple method to split the data in n different
        folds, all containing validation and train data.
        Args:
            fold:       How many folds to split the data in
            split:      The percentage of data that should be used
                        for validation in each fold.

        Returns:
           all_folds:   list of n elements with (train, test) tuples  
                        where train and test are dictionaries

        """

        raise NotImplementedError

    def get_regression_data(self, fold, target):
        """
        Transform a list of dictionaries to data that can
        be given as input to the regression model
        
        Args:
            fold:       List of dictionaries with information
            target:     The dictionary key that should be 
                        used as target
        """
        raise NotImplementedError


    def filter_sentences(self, key='length', 
                         elements=range(8), n=50, 
                         set_as_attr=True):
        """
        Filter the data such that it contains 50 instances of each
        element in elements (or as many as present in the data), where
        each element should correspond to a potential value of 
        self.data[key].
        By default, this function picks 50 sentences from each length
        in the range 1-7.
        Args:
            key:        The key in self.data to use to get values
            elements    List with elements that should be selected from
                        self.data[key]
            n:          How many elements of each should be in the
                        filtered dataset

        Returns:
            filtered_data:  A list containing dictionaries, as the self.data
                            object, which overall requires the given conditions
                            (i.e., has uniform distribution over
        """
        # initialise list for filtered data
        filtered_data = []

        to_find = dict(zip(elements, [n] * len(elements)))
        found = dict(zip(elements, [0] * len(elements)))

        # create shuffled indices to loop through data
        indices = [i for i in range(len(self.data))]
        random.shuffle(indices)
        for index in indices:
            new_dict = self.data[index]
            val = new_dict[key]
            if val not in to_find:
                # check if value is still needed
                continue
            else:
                # add dict and subtract val in to_find
                filtered_data.append(new_dict)
                to_find[val] -= 1
                found[val] += 1
                if to_find[val] == 0:
                    del to_find[val]

            if not to_find:
                break

        print("Filtered %s" % 
                ' '.join(["\n%i sentences with %s %s" % 
                    (list(found.values())[i], key, list(found.keys())[i])
                        for i in range(len(found))])
                )

        if set_as_attr:
            self.data = filtered_data

        return filtered_data

    def decorrelation_matrix(self):
        """
        Create a dictionary mapping (pos, depth)
        to count in corpus.
        """
        c_dict = defaultdict(int)
        for s_dict in self.data:
            for c, word in enumerate(s_dict['sentence'].split()):
                pos = int(s_dict['word_pos'][c])
                depth = int(s_dict['open_nodes_count'].split()[c])
                c_dict[(pos, depth)] += 1

        return c_dict

    def decorrelate(self, pos_min, pos_max, 
                    depth_min, depth_max, n,
                    set_as_attr=True):
        """
        Filter the data such that there is no correlation between
        position and depth anymore.
        To do so, a minimal and maximal position and depth,
        respectively, need to be given. For any (pos, depth) tuple
        in the rectangle described by thes coordinates n activations
        will be selected. Raises an error if one of the tuples does
        not have enough datapoints.

        This function can only be ran after activations are computed
        Args:
            pos_min:    minimal position to consider
            pos_max:    maximal position to consider
            depth_min:  minimal depth to consider
            depth_max:  maximal depth to consider
            n:          How many elements of each should be in the
                        filtered dataset. If one of the 
            set_as_attr:    set to False to keep the original self.data
                            object

        Returns:
            filtered_data:  A list containing dictionaries, as the self.data
                            object, in which position and depth are decorrelated
        """
        # check if activations are computed
        if not self.activations:
            raise ValueError("Activations should be computed\
            before this function can be ran"
                 )

        # initialise list for filtered data
        filtered_data = []

        pos_range = [i for i in range(pos_min, pos_max+1)]
        depth_range = [i for i in range(depth_min, depth_max+1)]
        all_tuples = [p for p in itertools.product(pos_range, depth_range)]

        to_find = dict(zip(all_tuples, [n]*len(all_tuples)))
        found = dict(zip(all_tuples, [n]*len(all_tuples)))

        # create shuffled indices to loop through data
        indices = [i for i in range(len(self.data))]
        random.shuffle(indices)
        for index in indices:
            s_dict = self.data[index]
            positions = []
            for c, word in enumerate(s_dict['sentence'].split()):
                pos = int(s_dict['word_pos'][c])
                depth = int(s_dict['open_nodes_count'].split()[c])
                if (pos, depth) not in to_find:
                    continue
                else:
                    positions.append(c)
                    to_find[(pos, depth)] -= 1
                    if to_find[(pos, depth)] == 0:
                        del to_find[(pos, depth)]

                    if not to_find:
                        if positions:
                            filtered_dict = self.filter_dict(s_dict, positions)
                            filtered_data.append(filtered_dict)
                        break

            if positions:
                filtered_dict = self.filter_dict(s_dict, positions)
                filtered_data.append(filtered_dict)

        if to_find:
            tups = to_find.keys()
            tups.sort()
            raise ValueError("Insufficient datapoints for:\n%s" %
                    '\n'.join(['(%s, %s): %i datapoints' % 
                        (t[0], t[1], n - to_find[t]) for t in tups])
                    )

        if set_as_attr:
            self.data = filtered_data

        return filtered_data

    def omit_words(self, key='depth', elements=[0],
                         set_as_attr=True):
        """
        Omit words from the dataset that satisfy certain constraints.
        This function can only be called *after* sentence activations
        have already been computed.

        Args:
            key:            dictionary key to base filtering on
            elements:       which elements should be filtered
            set_as_attr:    set to False to keep the original self.data
                            object

        Return:
            A list of dictionaries similar to self.data, but with 
            the indicated words filtered out.
        """
        # initialise list for filtered data
        raise NotImplementedError

    def write_data(self, filename, data=None):
        """
        Store list of dictionaries in a pickled file.
        Args:
            filename:   name of file to write to
            data:       the data argument can be used if another
                        another object than self.data should be
                        written
        """
        f = open(filename, 'wb')
        data = data or self.data
        pickle.dump(data, f)
        f.close()
        return

    def compute_activations(self, input, model='model.pt', vocabulary='reduced_vocab.txt', perplexity=False,
                            eos_separator='</s>', fixed_length_arrays=False, cuda=False,
                            get_representations=['word', 'lstm'], use_unk=False, lang='en', unk_token='<unk>', kbow_value=2):

        # indicate that activations have been computed
        self.activations = True
        # !/usr/bin/env python
        import sys
        import math
        import os
        import torch
        import argparse
        import json
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     '../../src/word_language_model')))
        import data
        import numpy as np
        import h5py
        import pickle
        from tqdm import tqdm


        print(cuda)
        if perplexity and 'lstm' not in get_representations:
            get_representations.append('lstm')
        elif not perplexity and len(get_representations) == 0:
            raise RuntimeError("Please specify at least one of -g lstm or -g word")

        vocab = data.Dictionary(vocabulary)
        sentences = []
        for l in input:
            sentence = l.rstrip('\n').rstrip().split(" ")
            sentences.append(sentence)
        sentences = np.array(sentences)

        print('Loading models...', file=sys.stderr)
        sentence_length = [len(s) for s in sentences]
        max_length = max(*sentence_length)
        import lstm
        model = torch.load(model, map_location=lambda storage, loc: storage)
        # model.rnn.flatten_parameters()
        # hack the forward function to send an extra argument containing the model parameters
        model.rnn.forward = lambda input, hidden: lstm.forward(model.rnn, input, hidden)

        saved = {}
        print(get_representations)
        if 'word' in get_representations:
            print('Extracting bow representations', file=sys.stderr)
            bow_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            kbow_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            word_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            bow_norm_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            kbow_norm_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            word_norm_vectors = [np.zeros((model.encoder.embedding_dim, len(s))) for s in sentences]
            for i, s in enumerate(tqdm(sentences)):
                bow_h = np.zeros(model.encoder.embedding_dim)
                norm_bow_h = np.zeros(model.encoder.embedding_dim)
                for j, w in enumerate(s):
                    if w not in vocab.word2idx and use_unk:
                        print('unk word: ' + w)
                        w = unk_token
                    inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
                    if cuda:
                        inp = inp.cuda()
                    w_vec = model.encoder.forward(inp).view(-1).data.cpu().numpy()
                    word_vectors[i][:, j] = w_vec
                    bow_h += w_vec
                    bow_vectors[i][:, j] = bow_h / (j + 1)
                    word_norm_vectors[i][:, j] = w_vec / np.linalg.norm(w_vec)
                    norm_bow_h += w_vec / np.linalg.norm(w_vec)
                    bow_norm_vectors[i][:, j] = norm_bow_h / (j + 1)

                    j_kbow = np.arange(np.max([j - kbow_value + 1, 0]), j + 1)
                    kbow_vectors[i][:, j] = np.mean(word_vectors[i][:, j_kbow], axis=1)
                    kbow_norm_vectors[i][:, j] = np.mean(word_norm_vectors[i][:, j_kbow], axis=1)

            saved['word_vectors'] = word_vectors
            saved['bow_vectors'] = bow_vectors
            saved['kbow_vectors'] = kbow_vectors
            saved['norm_word_vectors'] = word_norm_vectors
            saved['norm_bow_vectors'] = bow_norm_vectors
            saved['norm_kbow_vectors'] = kbow_norm_vectors

        if 'lstm' in get_representations:
            def feed_sentence(model, h, sentence):
                outs = []
                for w in sentence:
                    out, h = feed_input(model, h, w)
                    outs.append(torch.nn.functional.log_softmax(out[0]).unsqueeze(0))
                return outs, h

            def feed_input(model, hidden, w):
                if w not in vocab.word2idx and use_unk:
                    print('unk word: ' + w)
                    w = unk_token
                inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
                if cuda:
                    inp = inp.cuda()
                out, hidden = model(inp, hidden)
                return out, hidden

            print('Extracting LSTM representations', file=sys.stderr)
            # output buffers
            if fixed_length_arrays:
                log_probabilities = np.zeros((len(sentences), max_length))
                if not perplexity:
                    vectors = {k: np.zeros((len(sentences), model.nhid * model.nlayers, max_length)) for k in
                               ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']}
            else:
                log_probabilities = [np.zeros(len(s)) for s in tqdm(sentences)]  # np.zeros((len(sentences), max_length))
                if not perplexity:
                    vectors = {k: [np.zeros((model.nhid * model.nlayers, len(s))) for s in sentences] for k in tqdm(
                        ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden',
                         'cell'])}  # np.zeros((len(sentences), model.nhid*model.nlayers, max_length)) for k in ['in', 'forget', 'out', 'c_tilde']}
            if lang == 'en':
                init_sentence = " ".join([
                                             "In service , the aircraft was operated by a crew of five and could accommodate either 30 paratroopers , 32 <unk> and 28 sitting casualties , or 50 fully equipped troops . <eos>",
                                             "He even speculated that technical classes might some day be held \" for the better training of workmen in their several crafts and industries . <eos>",
                                             "After the War of the Holy League in 1537 against the Ottoman Empire , a truce between Venice and the Ottomans was created in 1539 . <eos>",
                                             "Moore says : \" Tony and I had a good <unk> and off-screen relationship , we are two very different people , but we did share a sense of humour \" . <eos>",
                                             "<unk> is also the basis for online games sold through licensed lotteries . <eos>"])
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
            init_out, init_h = feed_sentence(model, hidden, init_sentence)

            for i, s in enumerate(tqdm(sentences)):
                # sys.stdout.write("{}% complete ({} / {})\r".format(int(i/len(sentences) * 100), i, len(sentences)))
                out = init_out[-1]
                hidden = init_h
                # reinit hidden
                # hidden = model.init_hidden(1)
                ## intitialize with end of sentence
                # inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[args.eos_separator]]]))
                # if args.cuda:
                #    inp = inp.cuda()
                # out, hidden = model(inp, hidden)
                # out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)
                for j, w in enumerate(s):
                    if w not in vocab.word2idx and use_unk:
                        #print('unk word: ' + w)
                        w = unk_token
                    # store the surprisal for the current word
                    log_probabilities[i][j] = out[0, 0, vocab.word2idx[w]].data[0]
                    inp = torch.autograd.Variable(torch.LongTensor([[vocab.word2idx[w]]]))
                    if cuda:
                        inp = inp.cuda()
                    out, hidden = model(inp, hidden)
                    out = torch.nn.functional.log_softmax(out[0]).unsqueeze(0)

                    if not perplexity:
                        vectors['hidden'][i][:, j] = hidden[0].data.view(1, 1, -1).cpu().numpy()
                        vectors['cell'][i][:, j] = hidden[1].data.view(1, 1, -1).cpu().numpy()
                        # we can retrieve the gates thanks to the hacked function
                        for k, gates_k in vectors.items():
                            if 'gates' in k:
                                k = k.split('.')[1]
                                gates_k[i][:, j] = torch.cat([g[k].data for g in model.rnn.last_gates], 1).cpu().numpy()
                # save the results
                saved['log_probabilities'] = log_probabilities

                # if format != 'hdf5':
                #     saved['sentences'] = sentences

                # saved['sentence_length'] = np.array(sentence_length)

                if not perplexity:
                    for k, g in vectors.items():
                        saved[k] = g

            print("Perplexity: {:.2f}".format(
                math.exp(
                    sum(-lp.sum() for lp in log_probabilities) /
                    sum((lp != 0).sum() for lp in log_probabilities))))
        if not perplexity:
            # print ("DONE. Perplexity: {}".format(
            #        math.exp(-log_probabilities.sum()/((log_probabilities!=0).sum()))))

            return saved

    @staticmethod
    def filter_dict(s_dict, word_positions):
        """
        Filter from a dictionary representing sentence data
        the word positions given in the list

        Args:
            s_dict:         the dictionary to filter
            word_positions: the word positions to filter

        """
        # create new dictionary
        new_s_dict = {}

        # fetch sentence and
        s = s_dict['sentence']
        l = len(s.split())

        # loop over key, value pairs in s_dict, filter them
        for key, val in s_dict.items():
            if isinstance(val, list):
                new_val = [val[i] for i in word_positions]
            elif isinstance(val, str):
                val_list = val.strip('\n').split()
                if len(val_list) != l:
                    continue
                new_val = ' '.join([val_list[i] for i in word_positions])
            elif isinstance(val, np.ndarray):
                try:
                    new_val = val[:, word_positions]
                except IndexError:
                    new_val = val[word_positions]
            elif isinstance(val, int):
                continue
            else:
                raise ValueError("Unknown attribute type %s" % type(val))

            new_s_dict[key] = new_val

        return new_s_dict

    @staticmethod
    def get_word_freqs(word_freq_file):
        """
        Create a dictionary mapping words to
        frequencies
        """
        d = {}
        f = open(word_freq_file, 'rb')
        for line in f:
            freq, word = line.decode().split('\t')
            d[word.strip('\n')] = freq

        return d

