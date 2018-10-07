#!/usr/bin/env python
import sys, os
import torch
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/word_language_model')))
import data
import numpy as np
import pickle
import matplotlib.pyplot as plt
import lstm
import networkx as nx

parser = argparse.ArgumentParser(description='PyTorch PennTreeBank RNN/LSTM Language Model')
parser.add_argument('-model', type=str, default='model.pt', help='Meta file stored once finished training the corpus')
parser.add_argument('-o', '--output', default='weights_rnn.pkl', help='Destination for the output weights')
parser.add_argument('-fu', '--from-units', nargs='+', type=int, default=[], help='Weights FROM which units (counting from zero)')
parser.add_argument('-tu', '--to-units', nargs='+', type=int, default=[], help='Weights TO which units (counting from zero)')
parser.add_argument('--cuda', action='store_true', default=False)
args = parser.parse_args()

os.makedirs(os.path.dirname(args.output), exist_ok=True)


def extract_weights_from_nn(weight_type, from_units, to_units):
    '''

    :param weight_type: (str) 'weight_ih_l1' or 'weight_hh_l0' or 'weight_hh_l1'
    :param from_units: (list of int) weights FROM which units to extract
    :param to_units: (list of int) weights TO which units to extract
    :return:
    weights: (list of ndarrays) containing the extracted weights
    weights_names (list of str) containing the corresponding names (e.g., '1049_775').
    '''
    weights = []
    weights_names = []
    if len(to_units) > 0 and len(from_units) > 0:
        for from_unit in from_units:
            for to_unit in to_units:
                if from_unit != to_unit:
                    curr_weights_all_gates = []
                    for gate in range(4):
                        weights_nn = getattr(model.rnn, weight_type)
                        curr_weights_all_gates.append(weights_nn.data[gate * 650 + to_unit, from_unit])
                    weights.append(curr_weights_all_gates)
                    if weight_type in ('weight_hh_l1', 'weight_ih_l1'):
                        to_unit_str = 650 + to_unit
                        if weight_type == 'weight_hh_l1':
                            from_unit_str = 650 + from_unit
                    weights_names.append(str(from_unit_str) + '_' + str(to_unit_str))
    return weights, weights_names


def plot_hist_all_weights_with_arrows_for_units_of_interest(axes, weights_all, weight_of_interest, weight_names, layer, gate, arrow_dy=100):
    '''

    :param axes: axes of the plt on which hists will be presented
    :param weights_all: (list of ndarrays) len(list) = 4 (#gates).
    :param weight_of_interest: (list of sublists of floats) each sublist contains 4 floats for the weights between units of interest
    :param weight_names: (list of str) with the corresponding names for the weights of interest
    :param layer: (int) 0 or 1. 0=first layer; 1=second layer
    :param gate: (int) 0,1,2, or 3. 0=input, 1=forget, 2=cell or 3=output gate.
    :param arrow_dy  # arrow length
    :return:
    '''

    gate_names = ['Input', 'Forget', 'Cell', 'Output']
    colors = ['r', 'g', 'b', 'y']
    print('Weight histogram for: ' + 'layer ' + str(layer) + ' gate ' + gate_names[gate] )
    axes[layer, gate].hist(weights_all[gate].flatten(), bins=100, facecolor=colors[gate], lw=0, alpha=0.5)
    for c, weights in enumerate(weight_of_interest):
        axes[layer, gate].arrow(weights[gate], arrow_dy, 0, arrow_dy/10 - arrow_dy, color='k', width=0.01,
                                      head_length=arrow_dy/10, head_width=0.05)
        axes[layer, gate].text(weights[gate], 10+arrow_dy, str(weight_names[c]),
                                     {'ha': 'center', 'va': 'bottom'},
                                     rotation=90)
    if layer == 0:
        axes[layer, gate].set_title(gate_names[gate], fontsize=30)
    if layer == 2:
        axes[layer, gate].set_xlabel('weight size', fontsize=30)
    if gate == 0:
        if layer == 0:
            axes[layer, gate].set_ylabel('# recurrent l0 connections', fontsize=20)
        if layer == 1:
            axes[layer, gate].set_ylabel('# recurrent l1 connections', fontsize=20)
        if layer == 2:
            axes[layer, gate].set_ylabel('# l0-to-l1 connections', fontsize=20)


def generate_mds_for_connectivity(weights, layer, gate, from_units, to_units):
    '''

    :param weights:
    :param layer: 0, 1, or 2 = l0-l0, l1-l1 or l0-l2 connections
    :param gate: 0, 1, 2, or 3 = input, forget, cell or output.
    :param from_units: (list of int) weights FROM which units to extract
    :param to_units: (list of int) weights TO which units to extract
    :return:
    '''
    from sklearn import manifold

    layer_names = ['recurrent l0', 'recurrent l1', 'l0-l1 connections']
    gate_names = ['Input', 'Forget', 'Cell', 'Output']
    print('MDS for weights: layer - ' + layer_names[layer] + ', gate -' + gate_names[gate])
    seed = np.random.RandomState(seed=3)
    A = np.abs(weights[gate])
    A = np.maximum(A, A.transpose())
    A = np.exp(-A)

    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                       dissimilarity="precomputed", n_jobs=-2)

    pos = mds.fit(A).embedding_

    fig_mds, ax = plt.subplots(figsize=(40, 30))
    for i in range(650):
        c = 'k'; label = 'unidentified'
        if i in from_units:
            c = 'b'; label = 'syntax unit'
        elif i in to_units:
            c = 'r'; label = 'number unit'
        plt.text(pos[i, 0], pos[i, 1], str(i + layer*650), color=c, label=label)
    plt.xlim(np.min(pos[:, 0]), np.max(pos[:, 0]))
    plt.ylim(np.min(pos[:, 1]), np.max(pos[:, 1]))
    plt.axis('off')
    ax.set_title('Layer: ' + layer_names[layer] + ', Gate:' + gate_names[gate], fontsize=30)
    plt.savefig(args.output + '_gate_' + str(gate) + '_layers_' + str(layer) + '.mds.png')
    plt.close(fig_mds)


def plot_graph_for_connectivity(weights, layer, gate, from_units, to_units):
    layer_names = ['recurrent l0', 'recurrent l1', 'l0-l1 connections']
    gate_names = ['Input', 'Forget', 'Cell', 'Output']
    print('generating weights graph for: layer - ' + layer_names[layer] + ', gate -' + gate_names[gate])

    # thresh = 5*np.std(weights[gate].flatten())
    # mask = np.logical_or(weights[gate]>thresh, weights[gate]<-thresh).astype(int)

    A = np.abs(weights[gate])
    A = np.exp(-np.abs(recurrent_weights_l1_all[0])) # weighted adjacency matrix (LSTM weights are transformed to distance)
    A = np.maximum(A, A.transpose())

    plt.subplots(figsize=(40, 30))

    G = nx.from_numpy_matrix(A)

    labels = {}
    for idx, node in enumerate(G.nodes()):
        labels[node] = str(idx + 650)
    G = nx.relabel_nodes(G, labels)
    pos = nx.spring_layout(G, k=3 / np.sqrt(650))
    colors = ['b' if i in from_units else 'r' if i in to_units else 'g' for i in range(650)]
    nx.draw(G, pos, node_color = colors, node_size=500, width=0.01)  # , node_size=500, labels=labels, with_labels=True)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    plt.savefig(args.output + '_gate_' + str(gate) + '_layers_' + str(layer) + '.graph.png')
    plt.close()


#def sort_units_according_to_weights_with_number_units():
#    number_units = [769, 775]




# Load model
print('Loading models...')
print('\nmodel: ' + args.model+'\n')
model = torch.load(args.model)
model.rnn.flatten_parameters()

# generate unit lists per layer
from_units_l0 = [u for u in args.from_units if u < 650]  # units 1-650 (0-649) in layer 0 (l0)
from_units_l1 = [u - 650 for u in args.from_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)
to_units_l0 = [u for u in args.to_units if u < 650]  # units 1-650 (0-649) in layer 0 (l0)
to_units_l1 = [u - 650 for u in args.to_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)

# collect weights for each of the three cases (l0-l0, l1-l1, l0-l1):
# gates order in model.rnn.weight.data tensor: w_hi, w_hf, w_hc, w_ho
recurrent_weights_l0, recurrent_weights_l0_names = extract_weights_from_nn('weight_hh_l0', from_units_l0, to_units_l0)
recurrent_weights_l1, recurrent_weights_l1_names = extract_weights_from_nn('weight_hh_l1', from_units_l1, to_units_l1)
weights_l0_l1, weights_l0_l1_names = extract_weights_from_nn('weight_ih_l1', from_units_l0, to_units_l1)

# save weights to output file
with open(args.output, 'wb') as fout:
    pickle.dump([recurrent_weights_l0, recurrent_weights_l1, weights_l0_l1], fout, -1)

# for each gate and for each of the three cases above, extract ALL weights in the network and plot corresponding hists:
fig, axes = plt.subplots(3, 4, figsize=[30, 20])
arrow_dy = 10000 # arrow length
gate_names = ['Input', 'Forget', 'Cell', 'Output']
recurrent_weights_l0_all = []; recurrent_weights_l1_all = []; weights_l0_l1_all = []
#recurrent_weights_l1_769 = []; weights_l0_l1_769 = []
#recurrent_weights_l1_775 = []; weights_l0_l1_775 = []
#recurrent_weights_l1_987 = []; weights_l0_l1_987 = []
#recurrent_weights_l1_from_curr_unit = []; recurrent_weights_l1_to_curr_unit = []
for gate in range(4): # loop over the four gates (columns in the final figure)
    # Extract weights among ALL units:
    recurrent_weights_l0_all.append(model.rnn.weight_hh_l0.data[range(gate * 650, (gate + 1) * 650), :].numpy())
    recurrent_weights_l1_all.append(model.rnn.weight_hh_l1.data[range(gate * 650, (gate + 1) * 650), :].numpy())
    weights_l0_l1_all.append(model.rnn.weight_ih_l1.data[range(gate * 650, (gate + 1) * 650), :].numpy())
    
    for unit in from_units_l1:
        recurrent_weights_l1_from_curr_unit = model.rnn.weight_hh_l1.data[gate*650:(gate+1)*650, unit].numpy()
        units_with_highest_neg_proj_from_curr_unit = 650 + np.argsort(recurrent_weights_l1_from_curr_unit)
        units_with_highest_pos_proj_from_curr_unit = 650 + np.argsort(np.negative(recurrent_weights_l1_from_curr_unit))
        print('Gate ' + str(gate) + ' - units with highest neg/pos weights FROM ' + str(unit+650) + ':')
        print(units_with_highest_neg_proj_from_curr_unit[0:10])
        print(units_with_highest_pos_proj_from_curr_unit[0:10])
        print('\n')

    for unit in to_units_l1:
        recurrent_weights_l1_to_curr_unit = model.rnn.weight_hh_l1.data[(unit-650)+gate * 650, :].numpy()
        units_with_highest_neg_proj_to_curr_unit = 650 + np.argsort(recurrent_weights_l1_to_curr_unit)
        units_with_highest_pos_proj_to_curr_unit = 650 + np.argsort(np.negative(recurrent_weights_l1_to_curr_unit))
        print('Gate ' + str(gate) + ' - units with highest neg/pos weights TO ' + str(unit+650) + ':')
        print(units_with_highest_neg_proj_to_curr_unit[0:10])
        print(units_with_highest_pos_proj_to_curr_unit[0:10])
        print('\n')

    #recurrent_weights_l1_769.append(model.rnn.weight_hh_l1.data[(769-650)+gate * 650, :].numpy())
    #weights_l0_l1_769.append(model.rnn.weight_ih_l1.data[gate * 650:(gate + 1) * 650, 769 - 650].numpy())
    # all weights to 769:
    #recurrent_weights_l1_769.append(model.rnn.weight_hh_l1.data[(769-650)+gate * 650, :].numpy())
    #weights_l0_l1_769.append(model.rnn.weight_ih_l1.data[gate * 650:(gate + 1) * 650, 769 - 650].numpy())
    # all weights to 775:
    #recurrent_weights_l1_775.append(model.rnn.weight_hh_l1.data[(775-650)+gate * 650, :].numpy())
    #weights_l0_l1_775.append(model.rnn.weight_ih_l1.data[gate * 650:(gate + 1) * 650, 775-650].numpy())
    # all weights to 987:
    #recurrent_weights_l1_987.append(model.rnn.weight_hh_l1.data[(987-650)+gate * 650, :].numpy())
    #weights_l0_l1_987.append(model.rnn.weight_ih_l1.data[gate * 650:(gate + 1) * 650, 987-650].numpy())

    #units_with_highest_neg_proj_to_775 = 650 + np.argsort(recurrent_weights_l1_775[gate])
    #units_with_highest_pos_proj_to_775 = 650 + np.argsort(np.negative(recurrent_weights_l1_775[gate]))
    #print('units with highest pos/neg weights to 775')
    #print(units_with_highest_neg_proj_to_775[0:5])
    #print(units_with_highest_pos_proj_to_775[0:5])

    #print('units with highest pos/neg weights to 987')
    #units_with_highest_neg_proj_to_987 = 650 + np.argsort(recurrent_weights_l1_987[gate])
    #units_with_highest_pos_proj_to_987 = 650 + np.argsort(np.negative(recurrent_weights_l1_987[gate]))
    #print(units_with_highest_neg_proj_to_987[0:5])
    #print(units_with_highest_pos_proj_to_987[0:5])

    # Plot the hist of all weights and add arrows for the weight values of specific units (e.g., number or syntax units)
    plot_hist_all_weights_with_arrows_for_units_of_interest(axes, recurrent_weights_l0_all, recurrent_weights_l0, recurrent_weights_l0_names, 0, gate, arrow_dy=10000)
    plot_hist_all_weights_with_arrows_for_units_of_interest(axes, recurrent_weights_l1_all, recurrent_weights_l1, recurrent_weights_l1_names, 1, gate, arrow_dy=10)
    plot_hist_all_weights_with_arrows_for_units_of_interest(axes, weights_l0_l1_all, weights_l0_l1, weights_l0_l1_names, 2, gate, arrow_dy=10000)

plt.savefig(args.output + '.png')
plt.close(fig)
print('Hists were saved to: ' + args.output + '.png')


#### ------------ Visualize weight matrix with MDS ----------------
generate_MDS = False
if generate_MDS:
    generate_mds_for_connectivity(recurrent_weights_l0_all, 0, 0, from_units_l0, to_units_l0) # input
    generate_mds_for_connectivity(recurrent_weights_l0_all, 0, 1, from_units_l0, to_units_l0) # forget
    generate_mds_for_connectivity(recurrent_weights_l0_all, 0, 2, from_units_l0, to_units_l0) # cell
    generate_mds_for_connectivity(recurrent_weights_l0_all, 0, 3, from_units_l0, to_units_l0) # output
    generate_mds_for_connectivity(recurrent_weights_l1_all, 1, 0, from_units_l1, to_units_l1) # input
    generate_mds_for_connectivity(recurrent_weights_l1_all, 1, 1, from_units_l1, to_units_l1) # forget
    generate_mds_for_connectivity(recurrent_weights_l1_all, 1, 2, from_units_l1, to_units_l1) # cell
    generate_mds_for_connectivity(recurrent_weights_l1_all, 1, 3, from_units_l1, to_units_l1) # output

#### ------------ Visualize adjacency matrix with networkX----------------
# plot_graph_for_connectivity(recurrent_weights_l0_all, 0, 0, from_units_l0, to_units_l0)
generate_graph = False
if generate_graph:
    plot_graph_for_connectivity(recurrent_weights_l1_all, 1, 0, from_units_l1, to_units_l1)
    plot_graph_for_connectivity(recurrent_weights_l1_all, 1, 1, from_units_l1, to_units_l1)
    plot_graph_for_connectivity(recurrent_weights_l1_all, 1, 2, from_units_l1, to_units_l1)
    plot_graph_for_connectivity(recurrent_weights_l1_all, 1, 3, from_units_l1, to_units_l1)

