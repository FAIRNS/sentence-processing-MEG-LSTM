from functions import load_settings_params as lsp
from functions import find_optimal_bin as fob
import os.path as op
import numpy as np

# -------------MAIN SCRIPT---------------
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

print('Load data')
data = fob.load_data(settings, params)

num_channels = data.MEG_sentences.shape[1]
for channel in range(num_channels):
    print('Plots for Channel #' + str(channel + 1) + ' will be saved to Figures folder, and np arrays to Output folder')
    params.channel = channel
    # Parse data into word bins from sentences
    data.data_parsed_to_words = fob.bin_data(data.MEG_sentences, params) # Parse data into words
    # Calculate mean activity across all words
    fob.generate_ERF_figure(data.data_parsed_to_words, settings, params)
    # Calculate F-statistic over all word groups (noun/verb/etc.), for a running bin of varying sizes
    bin_size_min = 30; bin_size_max = 100; bin_size_step = 1 # in [msec]
    f_stat_opt, p_value_opt, bin_size_opt, t_center_opt = fob.find_optimal_bin(
        data, settings, params, bin_size_min, bin_size_max, bin_size_step)
    # Average data according to optimal time bin and save to Output folder
    data_sentences_ave_opt_bin = fob.average_over_optimal_bin_and_reconstruct_sentences(
        data.data_parsed_to_words, bin_size_opt, t_center_opt, settings, params)