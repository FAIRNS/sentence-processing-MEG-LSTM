import os.path as op
import numpy as np

class settings:
    def __init__(self):
        self.patient = 'am150105'
        self.raw_file_name = self.patient + '_speed4_V2-epo.fif'
        self.path2MEGdata = op.join('..', '..', 'Data', 'MEG', self.patient)
        self.path2LSTMdata = op.join('..', '..', 'Data', 'LSTM')
        self.path2figures = op.join('..', '..', 'Figures')
        self.path2output = op.join('..', '..', 'Output')
        self.stimuli_file_name = 'patient_am150105_stimuli_anomaly_type_0'
        self.MEG_file_name = 'patient_am150105_epochs_lock_to_beginning_of_sentence_anomaly_type_0.npy'
        self.LSTM_file_name = 'vectors-LSTM1000-0.npy'
        self.num_MEG_channels = 306

class params:
    def __init__(self):
        self.SOA = 300 # [msec]
        self.real_speed = 301 # [msec]
        self.sfreq = 200 # [Hz]
        self.startTime = 760 #[msec]
        self.seed_split = 1 # random seed for split
        self.CV_fold = 5  # 5-fold
        self.num_channels = 306

        # Additional hyper-parameters
        self.n_alphas = 50 # regularization size
        self.alpha_order_min = -10 # 10^(order)
        self.alpha_order_max = 3 # same
        self.alphas = np.logspace(self.alpha_order_min, self.alpha_order_max, self.n_alphas)
        self.eps = 5e-3
        self.l1_ratio = 0.8