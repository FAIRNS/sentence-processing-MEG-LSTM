import sys, os
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
import pickle
import argparse

parser = argparse.ArgumentParser(description='Visualize unit activations from an LSTM Language Model')
parser.add_argument('-sentences', '--stimuli-file-name', type=str, help='Path to text file containing the list of sentences to analyze')
parser.add_argument('-meta', '--stimuli-meta-data', type=str, help='The corresponding meta data of the sentences')
parser.add_argument('-activations', '--LSTM-file-name', type=str, help='The corresponding sentence (LSTM) activations')
parser.add_argument('-u', '--units', nargs='+', type=int, help='List of units for which to plot activations')
parser.add_argument('-o', '--output-file-name', type=str, help='Path to output folder for figures')
parser.add_argument('-k', '--split-by-keys', nargs='+', type=str, default='RC_type', help='Split analyses according to keys in Theo\'s meta info (e.g., RC_type, sentence_length, number_1, number_2, success)')
args = parser.parse_args()


# --------- Main script -----------
settings = lsp.settings()
params = lsp.params()
if len(sys.argv) > 1:
    settings.stimuli_file_name = args.stimuli_file_name              # list of sentences (txt file)
    settings.stimuli_meta_data = args.stimuli_meta_data              # corresponding meta info (pickle file)
    settings.LSTM_file_name = args.LSTM_file_name                    # corresponding LSTM activations  (pickle file)
    settings.path2stimuli = os.path.dirname(args.stimuli_file_name)  # input folder: sentences+metadata
    settings.path2LSTMdata = os.path.dirname(args.LSTM_file_name)    # input folder: LSTM activations
    settings.path2figures = args.output_file_name                    # output folder: figures
    units = args.units
else:
    print('Loading settings and parameters from function/load_settings_params')
    units = [950, 373, 984, 932, 179, 697, 924, 396, 554, 94,
                 552, 726, 612, 969, 731, 478, 733, 178, 604, 588]
    units = [758, 759, 930, 1041, 1101, 1149, 1198, 769, 775]
os.makedirs(os.path.join(args.output_file_name, 'units_activation'), exist_ok=True)

###### LOAD ############
# Load stimuli in groups according to struct
print('loading info file ' + settings.stimuli_meta_data)
all_stim_clean, all_info_clean, all_info_correct, IX_structures, labels, colors = alu.get_stimuli_and_info(settings, params, args.split_by_keys)

# Load LSTM data
print('Loading pre-trained LSTM data...')
with open(os.path.join(settings.path2LSTMdata, settings.LSTM_file_name), 'rb') as f:
    print(os.path.join(settings.path2LSTMdata, settings.LSTM_file_name))
    LSTM_and_baselines_data = pickle.load(f)
# LSTM_data = [item for i, item in enumerate(LSTM_data) if i in range(100)]

# Generate and plot unit activations
for IX_structure, label in zip(IX_structures, labels):
    print(label)
    LSTM_and_baselines_data_curr_structure = {}
    for key in ['gates.in', 'gates.forget', 'gates.out', 'gates.c_tilde', 'hidden', 'cell']:
       LSTM_and_baselines_data_curr_structure[key] = [sentence_matrix for ind, sentence_matrix in enumerate(LSTM_and_baselines_data[key]) if ind in IX_structure]
    curr_stimuli = [sentence for ind, sentence in enumerate(all_stim_clean) if ind in IX_structure]
    alu.plot_units_activation(LSTM_and_baselines_data_curr_structure, label, curr_stimuli, units, settings, params)

print('Figures were saved to: ' + os.path.join(args.output_file_name, 'units_activation'))
