import os, pickle, argparse
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='serif')

parser = argparse.ArgumentParser(description='Visualize unit activations from an LSTM Language Model')
parser.add_argument('-sentences', '--stimuli-file-name', type=str, help='Path to text file containing the list of sentences to analyze')
parser.add_argument('-meta', '--stimuli-meta-data', type=str, help='The corresponding meta data of the sentences')
parser.add_argument('-activations', '--LSTM-file-name', type=str, help='The corresponding sentence (LSTM) activations')
parser.add_argument('-o', '--output-file-name', type=str, help='Path to output folder for figures')
parser.add_argument('-c', '--condition', type=str, help='Which condition to plot: RC, nounpp, etc.')
parser.add_argument('-g', '--graphs', nargs='+', action='append', type=str,
                    help='Specify a curve to be added to the figure with the following info: subplot-number, color, '
                         'line-style, line-width, unit number, gate, and key-value pairs as in Theo\'s meta info, '
                         'e.g., -g 1 b -- 775 forget number_1 singular number_2 singular '
                         '-g 2 g - 769 output number_1 plural number_2 singular.'
                         'gate should be one of: '
                         'gates.in, gates.forget, gates.out, gates.c_tilde, hidden, cell')
parser.add_argument('-r', '--remove', type=int, default=0, help='How many words to omit from the end of sentence')
parser.add_argument('-x', '--xlabels', nargs='+', type=str, help='List with xlabels for all subplors. Must match the number of time points')
parser.add_argument('-y', '--ylabels', nargs='+', type=str, help='List with ylabels for all subplors. Must match the number of subplots provided by --graphs')
parser.add_argument('--no-legend', action='store_true', default=False, help='If specified, legend will be omitted')
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
    #print(graph)
    color = graph[1]
    ls = graph[2]
    ls = ls.replace("\\", '')
    lw = int(graph[3])
    unit = int(graph[4])
    gate = graph[5]
    # constraints are given in pairs such as 'number_1', 'singular' after unit number and gate
    keys_values = [(graph[i], graph[i + 1]) for i in range(6, len(graph), 2)]
    label = str(unit) + '_' + gate + '_' + '_'.join([key + '_' + value for (key, value) in keys_values])
    IX_to_sentences = []
    for i, curr_info in enumerate(info):
        check_if_contraints_are_met = True
        for key_value in keys_values:
            key, value = key_value
            if curr_info[key] != value:
                check_if_contraints_are_met = False
        if check_if_contraints_are_met and curr_info['RC_type']==condition:
            IX_to_sentences.append(i)
    return unit, gate, IX_to_sentences, label, color, ls, lw

def add_graph_to_plot(ax, LSTM_activations, unit, gate, label, c, ls, lw):
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
    ax.errorbar(range(1, mean_activity.shape[0] + 1), mean_activity, yerr=std_activity,
                label=label, ls=ls, lw=lw, color=c)
    if gate in ['in', 'forget', 'out']:
        ax.set_yticks([0, 1])
    else:
        ax.set_yticks([-1.5, 1.5])
        #ax.set_yticks(np.arange(min(-1, min(mean_activity)), 1+max(np.ceil(max(mean_activity)), 1), 1.0))


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
subplot_numbers = [int(graph_info[0]) for graph_info in args.graphs]
num_subplots = np.max(subplot_numbers)
fig, axs = plt.subplots(num_subplots, 1, sharex=True, figsize=(20, 15))
if num_subplots==1: axs=[axs] # To make the rest compatible in case of a single subplot
for g, graph in enumerate(args.graphs):
    subplot_number = subplot_numbers[g]-1
    unit, gate, IX_to_sentences, label, color, ls, lw = get_unit_gate_and_indices_for_current_graph(graph, info, args.condition)
    print(gate, label)
    graph_activations = [sentence_matrix for ind, sentence_matrix in enumerate(LSTM_activation[gate]) if ind in IX_to_sentences]
    curr_stimuli = [sentence for ind, sentence in enumerate(stimuli) if ind in IX_to_sentences]
    if args.remove > 0:
        graph_activations = [sentence_matrix[:, 0:-args.remove] for sentence_matrix in graph_activations]
        curr_stimuli = curr_stimuli[0][0:-args.remove]
    # print('\n'.join(curr_stimuli))
    add_graph_to_plot(axs[subplot_number], graph_activations, unit, gate, label, color, ls, lw)

# Cosmetics
axs[0].set_xticks(range(1, graph_activations[1].shape[1] + 1))
for i, ax in enumerate(axs):
    if args.xlabels:
        ax.set_xticklabels(args.xlabels) #, rotation='vertical')
    else:
        ax.set_xticklabels(stimuli[0].split(' ')) #, rotation='vertical')
    ax.tick_params(labelsize=45)
    ax.tick_params(axis='x', pad=40)
    if args.ylabels:
        ax.set_ylabel(args.ylabels[i], fontsize=45, rotation='horizontal', ha='right')
    #else:
        #ax.set_ylabel('Activation', fontsize=45)
    if not args.no_legend: ax.legend(fontsize=35, numpoints=1, loc=(1, 0), framealpha=0)

# Save and close figure
plt.subplots_adjust(left=0.15, hspace=0.25)
if not args.no_legend: plt.subplots_adjust(right = 0.5)
plt.savefig(args.output_file_name)
plt.savefig(os.path.splitext(args.output_file_name)[0] +'.png') # Save also as svg
plt.close(fig)
print('The figure was saved to: ' + args.output_file_name)

