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
    data_sentences_train: list len as params.CV_fold. Contains all train splits.
    data_sentences_test: list len as params.CV_fold. Contains all test splits.
    '''
    data_sentences_train = []; data_sentences_test = []
    import random
    random.shuffle(data_sentences)

    num_sentences = len(data_sentences)
    split_size = int(num_sentences/params.CV_fold)
    for split in range(params.CV_fold):
        IX_test_set = range(split*split_size, (split+1)*split_size)
        data_sentences_train.append([ele for IX, ele in enumerate(data_sentences) if IX not in IX_test_set])
        data_sentences_test.append([ele for IX, ele in enumerate(data_sentences) if IX in IX_test_set])

    return data_sentences_train, data_sentences_test


def prepare_data_for_regression(data_sentences_train, data_sentences_test, feature_type='hidden', dependent_var_name='open_nodes'):
    X_train, y_train = get_design_matrix(data_sentences_train, dependent_var_name)
    X_test, y_test = get_design_matrix(data_sentences_test, dependent_var_name)

    return X_train, y_train, X_test, y_test

def get_design_matrix(data_sentences, dependent_var_name, feature_type='hidden'):
    '''
    A function to transform the data structure into a design matrix for a regression model X*w = y.

    :param data_sentences: data object
    :params feature_type: str which type of activations to extract (hidde/cell/both)
    :return: X: design matrix (ndarray num_samples X num_features)
            y: corresponding vector with dependent variable
    '''
    X = []; y = []

    # len(activations_train)=num_sentences_train. Each element has num_words vectors of activation
    activations = [np.vstack(ele[feature_type]) for ele in data_sentences]
    word_freq = np.expand_dims(np.asarray([int(w) for ele in data_sentences for w in ele['word_frequencies'].strip().split(' ')]), 1)
    open_nodes = [int(w) for ele in data_sentences for w in ele['open_nodes_count'].strip().split(' ')]
    constituent_boundary = [int(w) for ele in data_sentences for w in ele['constituent_boundary'].strip().split(' ')]

    # Cat all sentences to generate matrices where each row is per word
    X = np.hstack(activations).transpose()
    X = np.hstack((X, word_freq)) # Add word freqs as another feature

    if dependent_var_name == 'open_nodes':
        y = np.hstack(open_nodes)
    elif dependent_var_name == 'constituent_boundary':
        y = np.hstack(constituent_boundary)

    return X, y