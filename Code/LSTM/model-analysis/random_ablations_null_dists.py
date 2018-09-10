import sys, os, pickle
from matplotlib import pyplot as plt


def generate_and_plot_null_dists(path2ablation_results):
    '''
    Collect ablation experiments for group of units of size k, save the results per k,
    and plot the corresponding distributions.

    :param path2ablation_results: (string) indicating the path to the summary text file of all ablation experiments.
    :return: performance_per_k: (dict) key: k, value: list with 1000 performances on random ablations of k units.

    In addition, the scripts saves to a pkl the null distributions for all k's found,
    then it plots and saves them to separate png files.
    '''

    with open(path2ablation_results, 'r') as f:
        results = f.readlines()

    experiment_info = [line.rstrip().split('\t')[0] for line in results]
    task_performance = [float(line.rstrip().split('\t')[2]) for line in results]
    k_s = [int(line[line.find('_k_')+3:line.find('_units_')]) for line in experiment_info]

    performance_per_k = {}
    sys.stdout.write('Plotting null dist for k = ')
    for k_loop in set(k_s):
        sys.stdout.write(str(k_loop) + ', ')
        sys.stdout.flush()
        curr_performance = [p for (k, p) in zip(k_s, task_performance) if k == k_loop]
        performance_per_k[k_loop] = curr_performance
        fig, ax = plt.subplots(figsize=(40, 30))
        plt.hist(curr_performance, bins=100)
        ax.set_xlabel('Task performance (fraction of correct trials)', fontsize=40)
        ax.set_ylabel('Number of random ablation experiments', fontsize=40)
        ax.set_title('k = ' + str(k_loop), fontsize=40)
        ax.tick_params(axis='both', labelsize=35)
        plt.xlim(0.5, 1)
        plt.ylim(0, 800)
        # Save figure per k
        file_name = 'null_distribution_ablation_experiment_k_' + str(k_loop) + '.png'
        plt.savefig(os.path.join('..', '..', '..', 'Figures', file_name))
        plt.close(fig)

    with open(path2ablation_results + '.pkl', 'wb') as f:
        pickle.dump(performance_per_k, f)
    print('\nNull dists were saved to: ' + path2ablation_results + '.pkl')

    return performance_per_k

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



# MAIN
path2ablation_results = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_experiments/regression_unit_ablation_results.txt'
# _ = generate_and_plot_null_dists(path2ablation_results)

# Example
with open(path2ablation_results + '.pkl', 'rb') as f:
    performance_per_k = pickle.load(f)

script = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py'
model = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
agreement_data = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/agreement-data/best_model.tab'
vocab = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
output = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit_'
eos = '"<eos>"'
format = 'pkl'
seed = 1 # random seed for numpy
unit_to_kill = [578, 988, 1041, 1149, 1229, 758, 1101, 916, 1005, 29, 186, 1061, 759, 31, 1198, 930, 488] # unit number (counting from one!)
unit_to_kill = [u+1 for u in unit_to_kill] # change counting from 1.
g = 1 # group size of units to kill in including random ones

command = script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                    ' --eos-separator ' + eos + ' --format ' + format + ' -u ' + ' '.join(map(str, unit_to_kill)) + ' -g '\
      + str(g) + ' -s ' + str(seed)

print(command)
import subprocess
cmd = subprocess.Popen(command)
cmd.communicate()

output = output + "_".join(map(str, unit_to_kill)) + '_groupsize_' + str(g) + '_seed_' + str(seed)  # Update output file name
output_fn = output + '_' + str(True) + '.pkl'  # update output file name

with open(output_fn, 'rb') as f:
    results = pickle.load(output_fn)

performance = results['score_on_task']/results['sentences']
p_value = get_p_value_from_null_dist(performance_per_k[10], performance)
print(p_value)