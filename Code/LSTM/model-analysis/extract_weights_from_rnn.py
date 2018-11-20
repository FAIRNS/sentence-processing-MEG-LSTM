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

parser = argparse.ArgumentParser(description='Extract and plot LSTM weights')
parser.add_argument('-model', type=str, help='Meta file stored once finished training the corpus')
parser.add_argument('-o', '--output', help='Destination for the output weights')
parser.add_argument('-fu', '--from-units', nargs='+', type=int, default=[], help='Weights FROM which units (counting from zero)')
parser.add_argument('-tu', '--to-units', nargs='+', type=int, default=[], help='Weights TO which units (counting from zero)')
parser.add_argument('-sr', '--short-range', nargs='+', type=int, default=[], help='list of short-range numebr units')
parser.add_argument('-lr', '--long-range', nargs='+', type=int, default=[], help='list of long-range numebr units')
parser.add_argument('-sy', '--syntax', nargs='+', type=int, default=[], help='list of syntax units')
parser.add_argument('--no-mds', action='store_true', default=False)
args = parser.parse_args()

# os.makedirs(os.path.dirname(args.output), exist_ok=True)


def extract_weights_from_nn(model, weight_type, from_units, to_units):
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
                    # Give a name to the weight according to units (unit1_unit2)
                    if weight_type in ('weight_hh_l1', 'weight_ih_l1'):
                        to_unit_str = 650 + to_unit
                        if weight_type == 'weight_hh_l1':
                            from_unit_str = 650 + from_unit
                    weights_names.append(str(from_unit_str) + '_' + str(to_unit_str))
    return weights, weights_names


def get_weight_type(fu, tu):
    if fu < 650:
        if tu < 650:
            w_type = 'weight_hh_l0'
        else:
            tu = tu - 650
            w_type = 'weight_ih_l1'
    else:
        fu = from_unit - 650
        if tu >= 650:
            tu = tu - 650
            w_type = 'weight_hh_l1'
    return fu, tu, w_type


def get_weight_between_two_units(model, gate, from_unit, to_unit):

    from_unit, to_unit, weight_type = get_weight_type(from_unit, to_unit)
    weights_nn = getattr(model.rnn, weight_type)
    weight = weights_nn.data[gate * 650 + to_unit, from_unit]

    return weight


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


def generate_mds_for_connectivity(curr_ax, weights, layer, gate, from_units, to_units):
    '''

    :param weights:
    :param ax: axis of figure on which to plot MDS
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
    # A = np.abs(weights[gate])
    A = np.abs(weights)
    A = np.maximum(A, A.transpose())
    A = np.exp(-A)

    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                       dissimilarity="precomputed", n_jobs=-2)

    # print('fitting MDS')
    pos = mds.fit(A).embedding_
    # print('Done')
    # fig_mds, ax = plt.subplots(figsize=(40, 30))
    for i in range(650):
        c = 'k'; label = 'unidentified'; s = 5; fontweight = 'light'
        if i in [u-650 for u in args.syntax]:
            c = 'g'; label = 'syntax unit'; s = 12; fontweight = 'bold'
        elif i in [u-650 for u in args.short_range]:
            c = 'm'; label = 'LR unit'; s = 12; fontweight = 'bold'
        elif i in [u-650 for u in args.long_range]:
            c = 'c'; label = 'number unit'; s = 12; fontweight = 'bold'
        elif i == 987-650:
            c = 'r'; label = 'number unit'; s = 12; fontweight = 'bold'
        elif i == 775-650:
            c = 'b'; label = 'number unit'; s = 12; fontweight = 'bold'
        elif i == 1149-650:
            c = 'g'; label = 'syntax unit'; s = 12; fontweight = 'bold'

        curr_ax.text(pos[i, 0], pos[i, 1], str(1 + i + layer*650), color=c, label=label, size=s, fontweight=fontweight)
        curr_ax.set_xlim(np.min(pos[:, 0]), np.max(pos[:, 0]))
    curr_ax.set_ylim(np.min(pos[:, 1]), np.max(pos[:, 1]))
    curr_ax.axis('off')
    # curr_ax.set_title('Layer: ' + layer_names[layer] + ', Gate:' + gate_names[gate], fontsize=30)
    # plt.savefig(args.output + '_gate_' + str(gate) + '_layers_' + str(layer) + '.mds.png')
    # plt.close(fig_mds)


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


def check_if_weight_is_outlier(curr_weight, all_weights_to_unit, all_weights_from_unit):
    mean_to = np.mean(all_weights_to_unit)
    std_to = np.std(all_weights_to_unit)
    mean_from = np.mean(all_weights_from_unit)
    std_from = np.std(all_weights_from_unit)
    outlier_to = curr_weight >= mean_to + 3 * std_to or curr_weight <= mean_to - 3 * std_to
    outlier_from = curr_weight >= mean_from + 3 * std_from or curr_weight <= mean_from - 3 * std_from

    return outlier_to, outlier_from

gate_names = ['Input', 'Forget', 'Cell', 'Output']
# Load model
print('Loading models...')
print('\nmodel: ' + args.model+'\n')
model = torch.load(args.model)
model.rnn.flatten_parameters()
# print(model.rnn._all_weights)

from_units_l1 = [u - 650 for u in args.from_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)
to_units_l1 = [u - 650 for u in args.to_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)

############## Generate a figure for each gate with connectivity table, weights dists, and MDS
bar_width = 0.4
rowLabels = [str(u) for u in args.from_units]
colLabels = [str(u) for u in args.to_units]
for gate in range(4):
    colors = []
    # Create a table at the bottom-left of the figure
    fig, ax1 = plt.subplots(1, figsize = (10, 3)) # Top-left distrubtions
    ax2 = fig.add_axes([0.5, 0.19, 0.4, 0.14])  # for 5 units: 0.5, 0.12, 0.4, 0.195 # Bottom-right distrubtions
    cell_text = np.empty((len(args.from_units), len(args.to_units)))
    jitter_to = []; jitter_from = []
    for i, from_unit in enumerate(args.from_units):
        # Plot right distribution
        all_weights_from_curr_unit = model.rnn.weight_hh_l1.data[gate * 650:(gate + 1) * 650, from_unit - 650].numpy()
        top_5_units = 650 + np.argsort(np.negative(np.absolute(all_weights_from_curr_unit)))[0:5]
        top_5_weights = all_weights_from_curr_unit[top_5_units-650]
        print('Gate ' + gate_names[gate] + ': Top 5 (abs) weights from unit ' + str(from_unit), top_5_units, top_5_weights)
        colors_row = []
        for j, to_unit in enumerate(args.to_units):
            all_weights_to_curr_unit = model.rnn.weight_hh_l1.data[(to_unit - 650) + gate * 650, :].numpy()
            if i == len(args.from_units)-1:
                top_5_units = 650 + np.argsort(np.negative(np.absolute(all_weights_to_curr_unit)))[0:5]
                top_5_weights = all_weights_to_curr_unit[top_5_units - 650]
                print('Gate ' + gate_names[gate] + ': Top 5 (abs) weights to unit ' + str(to_unit), top_5_units, top_5_weights)
                weights = model.rnn.weight_ih_l1.data[(to_unit - 650) + gate * 650, :].numpy()
                top_5_units = np.argsort(np.negative(np.absolute(weights)))[0:5]
                top_5_weights = weights[top_5_units]
                print('Gate ' + gate_names[gate] + ': Top 5 (abs) weights to unit ' + str(to_unit), top_5_units, top_5_weights)

            # Plot top distributions
            if i == 0:
                jitter_to.append(np.random.random(all_weights_to_curr_unit.size) * bar_width - 3 * bar_width / 4)
                ax1.scatter(j + jitter_to[j], all_weights_to_curr_unit, s=3)
            # Plot right-side distribution
            if j == 0:
                num_from_units = cell_text.shape[0]
                jitter_from.append(np.random.random(all_weights_from_curr_unit.size) * bar_width - bar_width / 2)
                ax2.scatter(all_weights_from_curr_unit, num_from_units - i + jitter_from[i], s=1)
            # Get weight
            curr_weight = get_weight_between_two_units(model, gate, from_unit, to_unit)
            # if i!=j:
            cell_text[i, j] = '%1.2f' % curr_weight

            # If weight is outlier color it in table and dists
            outlier_to, outlier_from = check_if_weight_is_outlier(curr_weight, all_weights_to_curr_unit,
                                                                  all_weights_from_curr_unit)
            if outlier_to:
                IX_to = np.where(all_weights_to_curr_unit == curr_weight)
                if i != j: ax1.scatter(j + jitter_to[j][IX_to[0][0]], curr_weight, color='r', s=3)
                if from_unit == 1149: # Mark weights from 1149
                    if i != j: ax1.text(j, curr_weight, str(from_unit) + '-' + str(to_unit), fontsize=8)

            if outlier_from and i!=j:
                IX_from = np.where(all_weights_from_curr_unit == curr_weight)
                ax2.scatter(curr_weight, num_from_units - i + jitter_from[i][IX_from[0][0]], color='r', s=3)
                colors_row.append('#56b5fd')
            else:
                colors_row.append('w')
        colors.append(colors_row)

    the_table = ax1.table(cellText=cell_text,
                          rowLabels=rowLabels,
                          colLabels=colLabels, rowLoc='center', cellColours=colors,
                          loc='bottom')
    the_table.set_fontsize(6)

    ### Add MDS to upper-right part of the figures
    if not args.no_mds:
        ax3 = fig.add_axes([0.52, 0.37, 0.4, 0.46])
        recurrent_weights_l1_all = model.rnn.weight_hh_l1.data[range(gate * 650, (gate + 1) * 650), :].numpy()
        generate_mds_for_connectivity(ax3, recurrent_weights_l1_all, 1, gate, from_units_l1, to_units_l1)

    ### cosmetics
    # ax1.set_ylim((-2, 2))
    # ax2.set_xlim((-2, 2))
    ax1.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    ax1.set_ylabel('Weight size (afferent)', fontsize=12)
    ax2.set_xlabel('Weight size (efferent)', fontsize=12)
    # ax2.xaxis.set_label_position('top')
    plt.subplots_adjust(bottom=0.37, right=0.5)
    ax1.set_title(gate_names[gate])

    ### Save figure
    dirname = os.path.dirname(args.output)
    basename = os.path.basename(args.output)
    fig.savefig(os.path.join(dirname, 'gate_' + gate_names[gate] + '_' + basename))
    print('Figures saved to: ' + os.path.join(dirname, 'gate_' + gate_names[gate] + '_' + basename))
    # print(the_table.get_window_extent('Agg'))


##########################################################################
old_figs = False
if old_figs:

    # generate unit lists per layer
    from_units_l0 = [u for u in args.from_units if u < 650]  # units 1-650 (0-649) in layer 0 (l0)
    from_units_l1 = [u - 650 for u in args.from_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)
    to_units_l0 = [u for u in args.to_units if u < 650]  # units 1-650 (0-649) in layer 0 (l0)
    to_units_l1 = [u - 650 for u in args.to_units if u > 649]  # units 651-1300 (650-1299) in layer 1 (l1)

    # collect weights for each of the three cases (l0-l0, l1-l1, l0-l1):
    # gates order in model.rnn.weight.data tensor: w_hi, w_hf, w_hc, w_ho
    recurrent_weights_l0, recurrent_weights_l0_names = extract_weights_from_nn(model, 'weight_hh_l0', from_units_l0, to_units_l0)
    recurrent_weights_l1, recurrent_weights_l1_names = extract_weights_from_nn(model, 'weight_hh_l1', from_units_l1, to_units_l1)
    forward_weights_l0_l1, forward_weights_l0_l1_names = extract_weights_from_nn(model, 'weight_ih_l1', from_units_l0, to_units_l1)

    # save weights to output file
    with open(os.path.join('Output', args.output), 'wb') as fout:
        pickle.dump([recurrent_weights_l0, recurrent_weights_l1, forward_weights_l0_l1], fout, -1)
    print('Weights save into a pickle: ' + os.path.join('Output', args.output))

    # for each gate and for each of the three cases above, extract ALL weights in the network and plot corresponding hists:
    fig, axes = plt.subplots(3, 4, figsize=[30, 20])
    arrow_dy = 10000 # arrow length
    gate_names = ['Input', 'Forget', 'Cell', 'Output']
    recurrent_weights_l0_all = []; recurrent_weights_l1_all = []; forward_weights_l0_l1_all = []
    for gate in range(4): # loop over the four gates (columns in the final figure)
        # Extract weights among ALL units:
        recurrent_weights_l0_all.append(model.rnn.weight_hh_l0.data[range(gate * 650, (gate + 1) * 650), :].numpy())
        recurrent_weights_l1_all.append(model.rnn.weight_hh_l1.data[range(gate * 650, (gate + 1) * 650), :].numpy())
        forward_weights_l0_l1_all.append(model.rnn.weight_ih_l1.data[range(gate * 650, (gate + 1) * 650), :].numpy())

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



        # Plot the hist of all weights and add arrows for the weight values of specific units (e.g., number or syntax units)
        plot_hist_all_weights_with_arrows_for_units_of_interest(axes, recurrent_weights_l0_all, recurrent_weights_l0, recurrent_weights_l0_names, 0, gate, arrow_dy=10000)
        plot_hist_all_weights_with_arrows_for_units_of_interest(axes, recurrent_weights_l1_all, recurrent_weights_l1, recurrent_weights_l1_names, 1, gate, arrow_dy=10)
        plot_hist_all_weights_with_arrows_for_units_of_interest(axes, forward_weights_l0_l1_all, forward_weights_l0_l1, forward_weights_l0_l1_names, 2, gate, arrow_dy=10000)

    plt.savefig(os.path.join('Figures', args.output + '.png'))
    plt.close(fig)
    print('Hists were saved to: ' + os.path.join('Figures', args.output + '.png'))


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

