import sys, os, pickle
from matplotlib import pyplot as plt


def generate_and_plot_null_dists(path2ablation_results, many_k_or_single, filter_units):
    '''
    Collect ablation experiments for group of units of size k, save the results per k,
    and plot the corresponding distributions.

    :param path2ablation_results: (string) indicating the path to the summary text file of all ablation experiments.
    :return: performance_per_k: (dict) key: k, value: list with 1000 performances on random ablations of k units.

    In addition, the scripts saves to a pkl the null distributions for all k's found,
    then it plots and saves them to separate png files.
    '''

    performance_per_k = {}
    with open(path2ablation_results, 'r') as f:
        results = f.readlines()

    experiment_info = [line.rstrip().split('\t')[0] for line in results]

    filtered_units = []; filtered_performance = []
    if many_k_or_single != 'many' and isinstance(many_k_or_single, int):  # ablation results contain only a single size of group of units (e.g., k=17)
        task_performance = [float(line.rstrip().split('\t')[1]) for line in results]
        units = [list(map(int, s.split('_')[1::])) for s in experiment_info]
        for i, (curr_units, curr_performance) in enumerate(zip(units, task_performance)):
            if not set(curr_units).intersection(set(filter_units)):
                filtered_units.append(curr_units)
                filtered_performance.append(curr_performance)
        performance_per_k[many_k_or_single] = filtered_performance


    elif many_k_or_single == 'many':  # ablation results contain are for many size groups (k)
        filtered_k_s = []
        task_performance = [float(line.rstrip().split('\t')[2]) for line in results]
        k_s = [int(line[line.find('_k_')+3:line.find('_units_')]) for line in experiment_info]
        units = [list(map(int, s[s.find('pkl')+3:s.find('groupsize')-1].split('_'))) for s in experiment_info]
        for i, (curr_units, curr_performance, curr_k) in enumerate(zip(units, task_performance, k_s)):
            if not set(curr_units).intersection(set(filter_units)):
                filtered_units.append(curr_units)
                filtered_performance.append(curr_performance)
                filtered_k_s.append(curr_k)

        sys.stdout.write('Plotting null dist for k = ')
        for k_loop in set(filtered_k_s):
            sys.stdout.write(str(k_loop) + ', ')
            sys.stdout.flush()
            curr_performance = [p for (k, p) in zip(filtered_k_s, filtered_performance) if k == k_loop]
            performance_per_k[k_loop] = curr_performance

        with open(path2ablation_results + '.pkl', 'wb') as f:
            pickle.dump(performance_per_k, f)
        print('\nNull dists were saved to: ' + path2ablation_results + '.pkl')

    return performance_per_k


def generate_and_plot_null_dists_simple(path2ablation_results, many_k_or_single, filter_units):
    '''
    Collect ablation experiments for group of units of size k, save the results per k,
    and plot the corresponding distributions.

    :param path2ablation_results: (string) indicating the path to the summary text file of all ablation experiments.
    :return: performance_per_k: (dict) key: k, value: list with 1000 performances on random ablations of k units.

    In addition, the scripts saves to a pkl the null distributions for all k's found,
    then it plots and saves them to separate png files.
    '''

    performance = {}
    with open(path2ablation_results, 'r') as f:
        results = f.readlines()
    performance[many_k_or_single] = [float(line.rstrip().split('\t')[0]) for line in results]

    return performance



def get_p_value_from_null_dist(null_distribution, performance):
    '''
    :param null_distribution: (list) of performance values
    :param performance: (float) performance for which p-value is calculated
    :return: p_value: (float) estimated p-value for the given performance and null distribution.
    '''

    trials_with_performance_greater_than_test = len([p for p in null_distribution if p < performance])
    total_num_of_trials = len(null_distribution)
    p_value = (trials_with_performance_greater_than_test + 1)/(total_num_of_trials + 1)

    return p_value

def plot_null_dist(performances_null, k, performance_test, p_value, fontsize=30):
    '''
    Generate png file of the null disttribution together with a labeled arrow indicating the test performance and its p-value
    :param performances_null: (list) of task-performance values from random ablation experiments
    :param k: (int) number of units ablated together in each of the experiments
    :param performance_test: (float) the value of a single test ablation experiment that will be compared to the null
    :param p_value: (float) its corresponding p-value based on the null-distribution
    :param fontsize: (float, optional) fontsize for the labels and title in the plot
    :return:
    '''
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(performances_null, bins=60)
    ax.set_xlabel('Task performance (fraction of correct trials)', fontsize=fontsize)
    ax.set_ylabel('Number of random ablation experiments', fontsize=fontsize)
    ax.set_title('Number of ablated units: k = ' + str(k), fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=fontsize*0.6)
    ax.set_xlim(0.6, 1)
    ax.set_ylim(0, 600)

    # add arrow for p-value:
    if p_value:
        arrow_dy = 50  # arrow length
        ax.arrow(performance_test, arrow_dy, 0, -40, color='k', width=0.001,
                                head_length=10, head_width=0.01)
        ax.text(performance_test, 10 + arrow_dy, 'task-performance = ' + str("{:.3f}".format(performance_test)) + '\np-value = '+str("{:.3f}".format(p_value)),
                               {'ha': 'center', 'va': 'bottom', 'fontsize':0.8*fontsize},
                               rotation=90)

    # Save figure per k
    file_name = 'null_distribution_ablation_experiment_k_' + str(k) + '.png'
    plt.savefig(os.path.join('..', '..', '..', 'Figures', file_name))
    plt.close(fig)


def plot_all_null_dists(performance_per_k, fontsize=25):
    '''
    generate a single figure with all null distributions, each in a subplot.
    :param performance_per_k: (dict) keys-k-values, values: lists of task performance.
    :param fontsize:
    :return:
    '''
    fig, axs = plt.subplots(3, 4, figsize=(40, 30))
    axs = axs.flatten()
    for i, k_loop in enumerate(set(performance_per_k.keys())):
        sys.stdout.write(str(k_loop) + ', ')
        sys.stdout.flush()
        axs[i].hist(performance_per_k[k_loop], bins=100)
        if i > 7:
            axs[i].set_xlabel('Task performance (fraction of correct trials)', fontsize=fontsize)
        if i%4==0:
            axs[i].set_ylabel('Number of random ablation experiments', fontsize=fontsize)
        axs[i].set_title('Number of ablated units: k = ' + str(k_loop), fontsize=fontsize)
        axs[i].tick_params(axis='both', labelsize=fontsize*0.8)
        axs[i].set_xlim(0.6, 1)
        axs[i].set_ylim(0, 600)

    # Save figure per k
    file_name = 'null_distribution_ablation_experiment.png'
    plt.savefig(os.path.join('..', '..', '..', 'Figures', file_name))
    plt.close(fig)
    print('Figure saved at %s' % os.path.join('..', '..', '..', 'Figures', file_name))

# Settings
filter_units = [776, 988] # counting from 1 - which units are not allowed in the ablated units (e.g, LR number units)
many_k_or_single = 12 # either the str 'many' or an int representing the size of the ablated group of units (k)
condition = ['simple_plural_control', 'simple_singular_control', 'adv_plural_control', 'adv_singular_control', 'adv_adv_plural_control', 'adv_adv_singular_control']

for cond in range(6):
    # MAIN
    # path2ablation_results = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_experiments/nounpp_plural_singular_control.txt'
    # path2ablation_results = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_experiments/nounpp_singular_plural_control.txt'
    path2ablation_results = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_experiments/' + condition[cond] + '.txt'

    # performance_per_k = generate_and_plot_null_dists(path2ablation_results, many_k_or_single, filter_units)
    performance_per_k = generate_and_plot_null_dists_simple(path2ablation_results, many_k_or_single, filter_units)

    # Example
    # with open(path2ablation_results + '.pkl', 'rb') as f:
    #     performance_per_k = pickle.load(f)


    #output_fn = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_experiments/ablation_results_killing_regression_unit_579_989_1042_1150_1230_759_1102_917_1006_30_187_1062_760_32_1199_931_489_groupsize_1_seed_1_True.pkl'

    #with open(output_fn, 'rb') as f:
    #    results = pickle.load(f)

    # performance_test = results['score_on_task']/results['num_sentences']
    # performance_test = 0.9466666666666667 # nounpp PS
    # performance_test = 0.65 # nounpp SP

    performance_test = {}
    performance_test['simple_singular_control'] = 0.8833333333333333 # simple S
    performance_test['simple_plural_control'] = 0.8733333333333333 # simple P
    performance_test['adv_singular_control'] = 0.8933333333333333 # adv S
    performance_test['adv_plural_control'] = 0.6422222222222222 # adv P
    performance_test['adv_adv_singular_control'] = 0.6144444444444445 # adv_adv S
    performance_test['adv_adv_plural_control'] = 0.7111111111111111 # adv_adv P


    #
    p_value = get_p_value_from_null_dist(performance_per_k[many_k_or_single], performance_test[condition[cond]])
    print(condition[cond], performance_test[condition[cond]], p_value)

    # plot_null_dist(performance_per_k[many_k_or_single], many_k_or_single, performance_test[condition[cond]], p_value)
    # plot_all_null_dists(performance_per_k)

    # 0.023976023976023976