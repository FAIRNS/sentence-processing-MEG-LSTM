import os.path as op
import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt


class data:
    def __init__(self):
        pass

def load_data(settings, params):
    # Load MEG data
    curr_data = data()
    curr_data.MEG_sentences = np.load(op.join(settings.path2MEGdata, settings.MEG_file_name))

    # Load stimuli (a string for each sentence)
    with open(op.join(settings.path2MEGdata, settings.stimuli_file_name), 'r') as f:
        curr_data.stimuli = f.readlines()
    # Parse stimuli into words
    curr_data.words = [x.strip().split(" ") for x in curr_data.stimuli]
    # Find the common lexicon for all words
    curr_data.lexicon = sorted(list(set([y for x in curr_data.words for y in x])))
    # Label each word according to its position in the alphabetically-sorted lexicon (curr_data.lexicon).
    num_trials = len(curr_data.stimuli)
    curr_data.labels = [[curr_data.lexicon.index(word) for word in curr_data.words[trial]] for trial in range(num_trials)]

    return curr_data

def bin_data(data, params):
    num_trials = data.shape[0]

    binned_data = []
    for trial in range(num_trials):
        curr_trial = data[trial, params.channel, :]
        # Cut duration before first-word onset time
        curr_trial = curr_trial[params.sfreq * params.startTime / 1e3:]
        # Generate bins according to SOA
        num_samples = params.bin_size * 8  # 8 words in each trial
        bins_start = range(0, num_samples, params.bin_size) # first sample of each bin
        digitized = np.digitize(range(num_samples), bins_start) # map each sample to its bin
        # Bin trial into 8 bins
        curr_trial_binned = [curr_trial[digitized == i] for i in range(1, np.max(digitized) + 1)]
        binned_data = binned_data + curr_trial_binned

    binned_data = np.asanyarray(binned_data)
    return binned_data


def generate_ERF_figure(data_parsed_to_words, settings, params):
    # Plot the mean field for each word within the SOA duration
    num_samples = data_parsed_to_words.shape[0]
    num_time_points = data_parsed_to_words.shape[1]
    t = range(num_time_points)
    t = [i*1e3/params.sfreq for i in t] # convert from samples to msec
    y = np.mean(np.asarray(data_parsed_to_words), axis=0)
    error = np.std(np.asarray(data_parsed_to_words), axis=0) / np.sqrt(num_samples)  # SEM
    plt.plot(t, y, 'k-')
    plt.fill_between(t, y - error, y + error, color='r', alpha=0.5)
    plt.xlabel('Time [msec]', size=18)
    plt.ylabel('ERF', size=18)
    # Save to 'Figures' folder
    file_name = 'mean_activity_in_bin_channel_' + str(params.channel+1) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close()

def find_optimal_bin(data, settings, params, bin_size_min = 10, bin_size_max=200, bin_size_step=1):
    # Calculate the F-statistic for a running window (bin) along the SOA duration,
    # Plot the result for all window centers and sizes.
    # The beginning of the running bin is determined according to the maximal bin size (see input vars).

    # Inputs -
    # bin_size_min:  optimal-bin search starts at this value. [msec]
    # bin_size_max:  optimal-bin search ends at this value. [msec]
    # bin_size_step: step between the above two values.
    # labels: the label of each word (e.g., 1=noun, 2=verb, 3=adj)

    bin_size_min = int(bin_size_min*params.sfreq/1e3)  # from msec to samples
    bin_size_max = int(bin_size_max*params.sfreq/1e3)  # from msec to samples
    bin_size_step = int(math.ceil(bin_size_step*params.sfreq/1e3))  # from msec to samples

    num_time_points = data.data_parsed_to_words.shape[1]

    bin_sizes = range(bin_size_min, np.min([num_time_points, bin_size_max]), bin_size_step) # All bin sizes
    t_centers = range(int(bin_size_max / 2), num_time_points - int(bin_size_max / 2)) # All centers of running bin
    f_stats = np.empty([len(bin_sizes), len(t_centers)]) # Initialize array
    p_values = np.empty([len(bin_sizes), len(t_centers)]) # Initialize array
    for i, bin_size in enumerate(bin_sizes): # Loop over bin-sizes
        for j, t_center in enumerate(t_centers): # Loop over t-centers
            bin_time_points = range(t_center-int(bin_size/2), t_center+int(bin_size/2)-1, 1) # samples of current bin
            curr_data = data.data_parsed_to_words[:,bin_time_points] # (num_words X num_time_points) extract relevant values from data
            ave_curr_data = np.mean(curr_data, axis=1) # (num_words X 1) average all values within current bin
            groups = [] # Initialize array
            labels = [l for sentence in data.labels for l in sentence] # (num_words X 1) Flat labels list to get the unique labels
            for label in set(labels): # Loop over unique labels
                curr_group = ave_curr_data[np.asarray(labels) == label] # Find indexes of current labels and extract mean values
                groups.append(curr_group) # Add the extracted values as a group (each group corresponds to a label)
            f_stats[i, j], p_values[i, j] = stats.f_oneway(*groups) # Summarize f-statistic for all bin-sizes and bin centers

    # Plot significant f-stat values
    p_thresh = 0.05
    f_stats = f_stats * (p_values < p_thresh)
    plt.imshow(f_stats, origin='lower', extent=[int(bin_size_max / 2)*1e3/params.sfreq,(num_time_points - int(bin_size_max / 2))*1e3/params.sfreq,bin_size_min*1e3/params.sfreq,bin_size_max*1e3/params.sfreq])
    cbar = plt.colorbar()
    cbar.set_label('F-statistic', size=18)
    plt.xlabel('Center of bin', size=18)
    plt.ylabel('Bin size', size=18)
    file_name = 'optimal_bin_channel_' + str(params.channel+1) + '.png'
    plt.savefig(op.join(settings.path2figures, file_name))
    plt.close()

    # Find maximal f_stats
    IX1_opt, IX2_opt = np.unravel_index(f_stats.argmax(), f_stats.shape)
    f_stat_opt = f_stats[IX1_opt, IX2_opt]
    p_value_opt = p_values[IX1_opt, IX2_opt]
    bin_size_opt = bin_sizes[IX1_opt] * 1e3/params.sfreq
    t_center_opt = t_centers[IX2_opt] * 1e3/params.sfreq

    return f_stat_opt, p_value_opt, bin_size_opt, t_center_opt


def average_over_optimal_bin_and_reconstruct_sentences(data_parsed_to_words, bin_size_opt, t_center_opt, settings, params):
    # After finding the optimal bin size and center, average the MEG values over this bin, for each channel. Then reshape
    # the data back to (num_trials X 8)
    opt_bin = range(int(t_center_opt*params.sfreq/1e3)-int(bin_size_opt*params.sfreq/1e3/2), int(t_center_opt*params.sfreq/1e3)+int(bin_size_opt*params.sfreq/1e3/2)-1, 1)
    data_parsed_to_words_ave_opt_bin = np.average(data_parsed_to_words[:, opt_bin], axis=1)
    curr_sentence = []; data_sentences_ave_opt_bin = []
    for i in range(len(data_parsed_to_words_ave_opt_bin)):
        if i%8!=0:
            curr_sentence.append(data_parsed_to_words_ave_opt_bin[i])
        elif i>0:
            curr_sentence.append(data_parsed_to_words_ave_opt_bin[i])
            data_sentences_ave_opt_bin.append(curr_sentence)
            curr_sentence = []
    curr_sentence.append(data_parsed_to_words_ave_opt_bin[i])
    data_sentences_ave_opt_bin.append(curr_sentence)
    data_sentences_ave_opt_bin = np.asarray(data_sentences_ave_opt_bin)
    file_name = 'MEG_data_sentences_averaged_over_optimal_bin_channel_' + str(params.channel+1)
    np.save(op.join(settings.path2output, file_name), data_sentences_ave_opt_bin, t_center_opt, bin_size_opt)
    return data_sentences_ave_opt_bin