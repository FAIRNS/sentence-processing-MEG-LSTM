import numpy as np
from sklearn.preprocessing import StandardScaler

def load_data_from_sentence_generator(settings):
    data = []
    for i in range(1000):
        dict = {}
        dict['sentence'] = ['an', 'example', 'sentence']
        dict['open_nodes'] = np.random.randint(0, 10, size=3)
        dict['activations'] = [np.random.rand(10), np.random.rand(10), np.random.rand(10)]
        data.append(dict)

    return data


def standardize_data(X_train, X_test):
    # Concatenate train and test datasets
    num_samples_train = X_train.shape[0]
    data = np.vstack((X_train, X_test))
    # Standardize data
    scaler = StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)
    # Split back into train and test datasets
    X_train = data[0:num_samples_train, :]
    X_test = data[num_samples_train::, :]
    return X_train, X_test



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
    word_freq_train = np.expand_dims(np.asarray([int(w) for ele in data_sentences_train for w in ele['word_frequencies'].strip().split(' ')]), 1)
    word_freq_test = np.expand_dims(np.asarray([int(w) for ele in data_sentences_test for w in ele['word_frequencies'].strip().split(' ')]), 1)
    open_nodes_train = [int(w) for ele in data_sentences_train for w in ele['open_nodes_count'].strip().split(' ')]
    open_nodes_test = [int(w) for ele in data_sentences_test for w in ele['open_nodes_count'].strip().split(' ')]

    # Cat all sentences to generate matrices where each row is per word
    X_train = np.hstack(activations_train).transpose()
    X_train = np.hstack((X_train, word_freq_train)) # Add word freqs as another feature

    X_test = np.hstack(activations_test).transpose()
    X_test = np.hstack((X_test, word_freq_test))  # Add word freqs as another feature

    y_train = np.hstack(open_nodes_train)
    y_test = np.hstack(open_nodes_test)

    return X_train, y_train, X_test, y_test