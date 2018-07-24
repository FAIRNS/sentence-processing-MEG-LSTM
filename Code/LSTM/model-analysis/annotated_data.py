import pickle
import random

class Data(object):

    def __init__(self):
        self.data = []

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
            vals = line.split(separator)
            self.data.append(dict(zip(column_names, vals)))
            length = len(vals[0].split())
            self.data[-1]['length'] = length
            for key, val in kwargs.items():
                self.data[-1][key] = val(line)

        return

    def add_activation_data(self, model):
        """
        Add activation data to the sentences, based on
        a given model.
        """
        for c, s_dict in enumerate(self.data):
            activations = self.compute_activations(s_dict['sentence'])
            s_dict['activation_data'] = activations

    def compute_activations(self):
        raise NotImplementedError

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


    def filter(self, key='length', elements=xrange(8), n=50, set_as_attr=False):
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
        indices = [i for i in xrange(len(self.data))]
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
                    (found.values()[i], key, found.keys()[i]) 
                        for i in xrange(len(found))])
                )

        if set_as_attr:
            self.data = filtered_data

        return filtered_data

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


