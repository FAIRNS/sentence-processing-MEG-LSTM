import os.path as op
import numpy as np

class settings:
    def __init__(self):


        # Paths
        self.path2code = '/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/MEG'
        self.path2LSTMdata = op.join('..', '..', 'Data', 'LSTM')
        self.path2figures = op.join('..', '..', 'Figures')
        self.path2output = op.join('..', '..', 'Output')

        # Files
       #self.LSTM_file_name = 'vectors-LSTM1000-0.npy'
        self.LSTM_file_name = 'vectors-LSTM500_2-0.npz'

        # Flags

class params:
    def __init__(self):
        #
        self.seed_split = 1 # random seed for split
        self.CV_fold = 5  # 5-fold

        # Hyper-parameters regression:
        self.n_alphas = 50 # regularization size
        self.alpha_order_min = -6 # 10^(order) range for regularization size search
        self.alpha_order_max = 3 # same
        self.alphas = np.logspace(self.alpha_order_min, self.alpha_order_max, self.n_alphas)
        self.eps = 1e-3 # see Scikit-learn
        self.l1_ratio = 0.8 # For Elastic-Net

class preferences:
    def __init__(self):
        self.run_Ridge = False
        self.run_LASSO = True
        self.run_ElasticNet = False
