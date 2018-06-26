import os.path as op
import os
import numpy as np
from sklearn.model_selection import train_test_split
from functions import load_settings_params as lsp
from functions import model_fitting_and_evaluation as mfe
from functions import plot_results as pr
import sys
import pickle

# --------- Main script -----------
vector_type = 'hidden'
print('Vector type: ' + vector_type)
print('Load settings and parameters')
settings = lsp.settings()
params = lsp.params()
# os.chdir(settings.path2code)
# print(os.getcwd())

file_name = 'sources_evoked_inverse_am150105.pkl'
with open(op.join(settings.path2MEGdata, 'sources', file_name)) as f:
    av_stc_meg2 = pickle.load(f)

subjects_dir = op.join(settings.path2MEGdata, 'anatomy')
av_stc_meg2.plot(subject='fsaverage', surface='inflated', hemi='lh', smoothing_steps=1, time_viewer=True, subjects_dir=subjects_dir, figure=None, views='lat', backend='mayavi', time_unit='ms', spacing='oct6')