

def get_classification_accuracy(model_fn, path2vocab, path2nouns, path2verbs):
    import sys, os
    import torch
    import data

    ################################
    # Read sg/pl noun and verb files
    ################################
    singular_nouns, plural_nouns = read_singular_plural_file(path2nouns)
    singular_verbs, plural_verbs = read_singular_plural_file(path2verbs)
    nouns_all = singular_nouns + plural_nouns
    verbs_all = singular_verbs + plural_verbs

    ######################
    # Load model
    ######################
    model = torch.load(model_fn)
    model.rnn.flatten_parameters()
    vocab = data.Dictionary(path2vocab)

    ######################################################
    # Get classification data: embeddings + labels(sg/pl)
    ######################################################
    encoding_embeddings_nouns, y_nouns = get_encoding_embeddings_and_labels(model, vocab, singular_nouns, plural_nouns)
    encoding_embeddings_verbs, y_verbs = get_encoding_embeddings_and_labels(model, vocab, singular_verbs, plural_verbs)

    #############################
    # Train SVM and get accuracy
    #############################
    acc_nouns = calc_svm_acc(encoding_embeddings_nouns, y_nouns)
    acc_verbs = calc_svm_acc(encoding_embeddings_verbs, y_verbs)

    return acc_nouns, acc_verbs


def read_singular_plural_file(path2file):
    '''

    :param path2file:
    :return: two lists with singular and plural words
    '''
    with open(path2file, 'r') as f:
        words = f.readlines()
    singular_words = [l.strip().split()[0] for l in words]
    plural_words = [l.strip().split()[1] for l in words]

    return singular_words, plural_words


def get_encoding_embeddings_and_labels(model, vocab, singular_words, plural_words):
    import numpy as np
    embeddings_in = model.encoder.weight.data.cpu().numpy()
    idx_singulars = [vocab.word2idx[w] for w in singular_words]
    idx_plurals = [vocab.word2idx[w] for w in plural_words]
    encoding_embeddings = embeddings_in[idx_singulars + idx_plurals, :]
    labels = '1' * len(idx_singulars) + '2' * len(idx_plurals)
    labels = np.asarray([int(j) for j in labels])
    return encoding_embeddings, labels

def calc_svm_acc(X, y):
    from sklearn.model_selection import cross_val_score
    from sklearn import svm
    import numpy as np

    svc = svm.SVC(kernel='linear')
    svc.C = 1 
    score = cross_val_score(svc, X, y, cv=5, n_jobs=1)
    return np.mean(score)
