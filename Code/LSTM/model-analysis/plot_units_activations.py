import pickle, argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Visualize unit activations from an LSTM Language Model')
parser.add_argument('-sentences', '--stimuli-file-name', type=str, help='Path to text file containing the list of sentences to analyze')
parser.add_argument('-meta', '--stimuli-meta-data', type=str, help='The corresponding meta data of the sentences')
parser.add_argument('-activations', '--LSTM-file-name', type=str, help='The corresponding sentence (LSTM) activations')
parser.add_argument('-o', '--output-file-name', type=str, help='Path to output folder for figures')
parser.add_argument('-c', '--condition', type=str, help='Which condition to plot: RC, nounpp, etc.')
parser.add_argument('-g', '--graphs', nargs='+', action='append', type=str,
                    help='Specify a curve to be added to the figure according to unit number, '
                         'gate, and the key + value as in Theo\'s meta info, '
                         'e.g., -k 775 forget number_1 singular number_2 singular '
                         '-k 769 output number_1 plural number_2 singular. '
                         'The gate should be one of: '
                         'gates.in, gates.forget, gates.out, gates.c_tilde, hidden, cell')
args = parser.parse_args()


def get_unit_gate_and_indices_for_current_graph(graph, info, condition):
    '''

    :param graph: list containing info regarding the graph to plot - unit number, gate and constraints
    :param info: info objcet in Theo's format
    :param condition: sentence type (e.g., objrel, nounpp).
    :return:
    unit - unit number
    gate - gate type (gates.in, gates.forget, gates.out, gates.c_tilde, hidden, cell)
    IX_sentences - list of indices pointing to sentences numbers that meet the constraints specified in the arg graph
    '''
    unit = int(graph[0])
    gate = graph[1]
    # constraints are given in pairs such as 'number_1', 'singular' after unit number and gate
    keys_values = [(graph[i], graph[i + 1]) for i in range(2, len(graph), 2)]
    label = '_'.join([key + '_' + value for (key, value) in keys_values])
    IX_to_sentences = []
    for i, curr_info in enumerate(info):
        check_if_contraints_are_met = True
        for key_value in keys_values:
            key, value = key_value
            if curr_info[key] != value:
                check_if_contraints_are_met = False
        if check_if_contraints_are_met and curr_info['RC_type']==condition:
            IX_to_sentences.append(i)
    return unit, gate, IX_to_sentences, label

def add_graph_to_plot(LSTM_activations, stimuli, unit, gate):
    '''

    :param LSTM_activations(ndarray):  LSTM activations for current *gate*
    :param stimuli (list): sentences over which activations are averaged
    :param unit (int): unit number to plot
    :param gate (str): gate type (gates.in, gates.forget, gates.out, gates.c_tilde, hidden, cell)
    :return: None (only append curve on active figure)
    '''
    print('Unit ' + str(unit))
    if gate.find('gate')==0: gate = gate[6::] # for legend, omit 'gates.' prefix in e.g. 'gates.forget'
    # Calc mean and std
    mean_activity = np.mean(np.vstack([LSTM_activations[i][unit, :] for i in range(len(LSTM_activations))]), axis=0)
    std_activity = np.std(np.vstack([LSTM_activations[i][unit, :] for i in range(len(LSTM_activations))]), axis=0)

    # Add curve to plot
    ax.errorbar(range(1, mean_activity.shape[0] + 1), mean_activity, yerr=std_activity, label=str(unit)+' '+gate, linewidth=5) #, ls='--')
    ax.set_ylabel('Activation', fontsize=35)
    ax.set_xticks(range(1, mean_activity.shape[0] + 1))
    ax.set_xticklabels(stimuli[0].split(' '), rotation='vertical')
    ax.legend(fontsize=24, numpoints=1, loc=(1, 0.5), framealpha=0)
    ax.tick_params(labelsize=30)
    fig.subplots_adjust(bottom=0.25)


# make output dir in case it doesn't exist
os.makedirs(os.path.dirname(args.output_file_name), exist_ok=True)

###### Load LSTM activations, stimuli and meta-data ############
print('Loading pre-trained LSTM data...')
LSTM_activation = pickle.load(open(args.LSTM_file_name, 'rb'))
print('Loading stimuli and meta-data...')
with open(args.stimuli_file_name, 'r') as f:
    stimuli = f.readlines()
info = pickle.load(open(args.stimuli_meta_data, 'rb'))

##### Plot all curves on the same figure #########
fig, ax = plt.subplots(1, 1, figsize=(35, 20))
for g, graph in enumerate(args.graphs):
    unit, gate, IX_to_sentences, label = get_unit_gate_and_indices_for_current_graph(graph, info, args.condition)
    print(gate, label)
    graph_activations = [sentence_matrix for ind, sentence_matrix in enumerate(LSTM_activation[gate]) if ind in IX_to_sentences]
    curr_stimuli = [sentence for ind, sentence in enumerate(stimuli) if ind in IX_to_sentences]
    # print('\n'.join(curr_stimuli))
    add_graph_to_plot(graph_activations, curr_stimuli, unit, gate)

# Save and close figure
plt.savefig(args.output_file_name)
plt.close(fig)
print('The figure was saved to: ' + args.output_file_name)