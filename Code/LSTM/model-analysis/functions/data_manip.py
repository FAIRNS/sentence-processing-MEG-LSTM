import numpy as np

def load_data_from_sentence_generator(settings):
    data = []
    for i in range(1000):
        dict = {}
        dict['sentence'] = ['an', 'example', 'sentence']
        dict['open_nodes'] = np.random.randint(0, 10, size=3)
        dict['activations'] = [np.random.rand(10), np.random.rand(10), np.random.rand(10)]
        data.append(dict)

    return data



def split_data(data_sentences, params):
    '''

    :param data_sentences: list of dictionaries. len(list) = num_sentences.
    :param params: object that includes info about CV settings
    :return:
    data_sentences_train: list len as params.CV_fold. Containts all train splits.
    data_sentences_test: list len as params.CV_fold. Contatins all test splits.
    '''
    data_sentences_train = []; data_sentences_test = []
    import random
    random.seed(params.seed_split)
    random.shuffle(data_sentences)

    num_sentences = len(data_sentences)
    split_size = int(num_sentences/params.CV_fold)
    for split in range(params.CV_fold):
        IX_test_set = range(split*split_size, (split+1)*split_size)
        data_sentences_train.append([ele for IX, ele in enumerate(data_sentences) if IX not in IX_test_set])
        data_sentences_test.append([ele for IX, ele in enumerate(data_sentences) if IX in IX_test_set])

    return data_sentences_train, data_sentences_test


def prepare_data_for_regression(data_sentences_train, data_sentences_test):
    #TODO: get a key (hidde/cell/both) for which activations to put in the regression
    X_train = []; y_train = []; X_test = []; y_test = []

    # len(activations_train)=num_sentences_train. Each element has num_words vectors of activation
    activations_train = [np.vstack(ele['hidden']) for ele in data_sentences_train]
    activations_test = [np.vstack(ele['hidden']) for ele in data_sentences_test]
    open_nodes_train = [int(w) for ele in data_sentences_train for w in ele['open_nodes_count'].strip().split(' ')]
    open_nodes_test = [int(w) for ele in data_sentences_test for w in ele['open_nodes_count'].strip().split(' ')]

    # Cat all sentences to generate matrices where each row is per word
    X_train = np.hstack(activations_train).transpose()
    X_test = np.hstack(activations_test).transpose()
    y_train = np.hstack(open_nodes_train)
    y_test = np.hstack(open_nodes_test)

    return X_train, y_train, X_test, y_test