import os.path as op
import numpy as np

class settings:
    def __init__(self):

        # General
        self.patient = 'am150105'
        self.stimuli_type = 'from_marco_script' # MEG_stimuli, NP_VP_transition, Relative_clauses

        # Paths
        #base_folder = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM'
        base_folder = '/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM'

        self.path2code = op.join('..', '..', 'Code', 'MEG')
        self.path2MEGdata = op.join('..', '..', 'Data', 'MEG', self.patient)

        # FRENCH
        #self.path2LSTMdata = op.join(base_folder, 'Data', 'LSTM', 'activations', 'french', 'model2-500-2-0.5-SGD-10-tied.False-300')
        self.path2LSTMdata = op.join('..', '..', 'Data', 'LSTM')

        # ENGLISH
        #self.path2figures = op.join('..', '..', 'Figures')
        self.path2figures = op.join(base_folder, 'Figures')

        #self.path2output = op.join('..', '..', 'Output')
        self.path2output = op.join(base_folder, 'Output')

        # self.path2stimuli = op.join('..', '..', 'Data', 'Stimuli')
        self.path2stimuli = op.join(base_folder, 'Data', 'Stimuli')

        self.path2stimuli_parent = '/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-' + self.patient
        #self.path2stimuli_parent = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/MEG/' + self.patient

        # Files
        self.stimuli_file_name = 'RC_english_synthetic_with_objdep.txt' # Sentence list (text file)
        self.stimuli_meta_data = 'info_RC_english_synthetic_with_objdep.p' # Corresponding meta-data (pickle)
        self.LSTM_file_name = 'RC_english_synthetic_with_objdep.pkl' # LSTM activations for the sentences (pickle)
        
        self.raw_file_name = self.patient + '_speed4_V2-epo.fif'
        self.MEG_file_name = 'patient_' + self.patient + '_epochs_lock_to_beginning_of_sentence_anomaly_type_0.npy'
        self.MEG_file_name = 'am150105_speed4_V2 - epo.fif'
        self.word_vectors_file_name = 'word_vectors.npy'
        self.word_vectors_BOW_file_name = 'bow_vectors.npy'
        self.bad_trials_file_name = '/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/bad_epochs_' + self.patient + '_speed4_V3-epo.npy'
        self.bad_trials_file_name = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/MEG/am150105/bad_epochs_' + self.patient + '_speed4_V3-epo.npy'

        # MEG
        self.num_MEG_channels = 306

        # Flags
        self.use_optimal_bin = False
        self.use_sources_data = True
        self.run_Ridge = True
        self.run_LASSO = False
        self.run_ElasticNet = False

class params:
    def __init__(self):
        self.SOA = 300 # [msec]
        self.real_speed = 301 # [msec]
        self.sfreq = 200 # [Hz]
        self.startTime = 760 #[msec]
        self.seed_split = 1 # random seed for split
        self.CV_fold = 5  # 5-fold
        self.num_channels = 306

        # Hyper-parameters:
        self.n_alphas = 50 # regularization size
        self.alpha_order_min = -6 # 10^(order) range for regularization size search
        self.alpha_order_max = 3 # same
        self.alphas = np.logspace(self.alpha_order_min, self.alpha_order_max, self.n_alphas)
        self.eps = 1e-3 # see Scikit-learn
        self.l1_ratio = 0.8 # For Elastic-Net
