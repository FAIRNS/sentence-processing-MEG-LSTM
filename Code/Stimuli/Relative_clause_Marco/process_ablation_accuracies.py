import numpy as np
from os import listdir
import sys

prefix = sys.argv[1]
data_dir = sys.argv[2]
data_dir = data_dir + '/'
all_files = listdir(data_dir)

for file in all_files:
    if file.endswith('abl') and file.startswith(prefix):
        data=np.load(data_dir+file)
        hits = data['score_on_task']
        tot_sentences = data['num_sentences']
        accuracy = hits/(tot_sentences+0.0)
        print(file + '\t' + str(hits) + '\t' + str(tot_sentences) + '\t' + str(accuracy))
        
