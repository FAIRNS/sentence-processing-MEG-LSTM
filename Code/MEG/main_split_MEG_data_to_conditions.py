import os, mne
import numpy as np
from Scripts import sentcomp_epoching
import pickle
import codecs

# Paths
patient = 'am150105'
path2data = '/neurospin/meg/meg_tmp/sentcomp_Marti_2016/FAIRNeSs/am150105'
file_name = 'am150105_speed4_V2-epo.fif'
path2stimuli = '/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-am150105/Stim/data'
stimuli_file_name = 'data.p'

# Load stimuli

f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-am150105/Stim/block2_300ms/stimuli.p', 'r')
run1 = pickle.load(f)

f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-am150105/Stim/block6_300ms/stimuli.p', 'r')
run2 = pickle.load(f)

f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-am150105/Stim2/block0_300ms/stimuli.p', 'r')
run3 = pickle.load(f)

f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/1-am150105/Stim2/block2_300ms/stimuli.p', 'r')
run4 = pickle.load(f)

all_stim = run1 + run2 + run3 + run4

# load the rejected trials
bad_trials = np.load('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/bad_epochs_am150105_speed4_V3-epo.npy')
# All stimuli without rejected ones
all_stim2 = [i for j, i in enumerate(all_stim) if j not in bad_trials]

# Load epoch data
epochs = mne.read_epochs(os.path.join(path2data, file_name))
epochs.events[:, 1] = range(358)
epochs_all_channels_trials = epochs.get_data()

# Generate epochs locked to anomalous words
real_speed = .301 # in sec
anomaly = 0 # 0: normal, 1: nonword (without vowels), 2: syntactic, 3: semantic
position = [4, 6, 8] # 0,1,2..8
responses = [0, 1] # Correct/wrong response of the subject
structures = [1, 2, 3] # 1: 4-4, 2: 2-6, 3: 6-2

conditions = dict([
			('Anomalies', [anomaly]),
			('Positions', position),
			('Responses', responses),
            ('Structure', structures)])

knames1, ep1 = sentcomp_epoching.get_condition(conditions=conditions, epochs=epochs, startTime=-.2, duration=1.5, real_speed=real_speed)

# Lock to beginning of sentence
epochs_sliced_entire_sentence = epochs[knames1].get_data()
IX_for_stimuli = epochs[knames1].events[:,1]
all_stimuli_sliced_entire_sentence = [i for j, i in enumerate(all_stim2) if j in IX_for_stimuli]
file_name = 'patient_' + patient + '_stimuli' + '_anomaly_type_' + str(anomaly)
f = codecs.open(os.path.join(path2data, file_name), 'w', 'utf-8')
for item in all_stimuli_sliced_entire_sentence:
  print>>f, item
f.close
file_name = 'patient_' + patient + '_epochs_lock_to_beginning_of_sentence' + '_anomaly_type_' + str(anomaly)
np.save(os.path.join(path2data, file_name), epochs_sliced_entire_sentence)

# Lock to anomalous word
epochs_sliced_lock_to_anomalous_word = ep1[knames1].get_data()
file_name = 'patient_' + patient + '_epochs_lock_to_anomalous_word' + '_anomaly_type_' + str(anomaly)
np.save(os.path.join(path2data, file_name), epochs_sliced_lock_to_anomalous_word)
