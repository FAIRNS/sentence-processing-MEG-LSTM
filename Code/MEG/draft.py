import os.path as op
from functions import analyse_LSTM_units as alu
from functions import load_settings_params as lsp
from matplotlib import  pyplot as plt
import matplotlib.image as mpimg


import os
os.chdir(os.path.dirname(__file__))

# ------------------------------------
# Generate PCA figures with all models
# ------------------------------------

vectors = ['cell', 'hidden', 'word_vectors', 'bow_vectors']

print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()

# Load structure labels
_, _, _, _, labels, _ = alu.get_stimuli_and_info(settings, params)

# Generate figures for each label containing all model vectors
fig, axs = plt.subplots(2, 2, figsize=(60, 30))
for label in labels:
    fig_name = 'PCA_' + label + '_' + settings.LSTM_file_name + '.png'
    for i, vector_type in enumerate(vectors):
        file_name = 'PCA_LSTM_' + vector_type + '_' + label + '_' + settings.LSTM_file_name + '.png'
        img = mpimg.imread(op.join(settings.path2figures, 'units_activation', file_name))
        axs[i%2, i/2].imshow(img)
        axs[i%2, i/2].axis('off')
        axs[i%2, i/2].set_title(vector_type, fontsize=26)
    plt.tight_layout()
    plt.savefig(op.join(settings.path2figures, 'units_activation', fig_name))
    print('Saved to ', op.join(settings.path2figures, 'units_activation', fig_name))

