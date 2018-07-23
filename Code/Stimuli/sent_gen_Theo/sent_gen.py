#This script execute main.py and parse and save the sentences as blocks for one subject.

# !! Clear workspace before executing !!

from random import shuffle
import os
import shutil
import pickle

path = os.path.abspath(os.path.dirname(__file__))
os.chdir(path)
session_name = 'example_sentences'
if os.path.isdir(session_name):
    shutil.rmtree(session_name)
os.mkdir(session_name)

nb_sent = 100000#1920#480#192
len_block = 80#240#60#24
speeds = [300, 160, 120, 80, 300, 160, 120, 80] ## Should be the same length as nb_block
nb_block = 8

anomalies = [] 

def check_speeds(speeds):
# Shuffle speed but always put a slow block at the begining and do not immediately repeat the same speed
    shuffle(speeds)
    if (speeds[0] != max(speeds)):
        slow_speed = speeds.index(max(speeds))
        speeds[0], speeds[slow_speed] = speeds[slow_speed], speeds[0]
    for i_speed in range(len(speeds)-1):
        if speeds[i_speed] == speeds[i_speed + 1]:
            if i_speed == 6 or i_speed == 5:
                speeds[i_speed-2], speeds[i_speed] = speeds[i_speed], speeds[i_speed-2]
            else:
                speeds[i_speed+2], speeds[i_speed] = speeds[i_speed], speeds[i_speed+2]
            check_speeds(speeds)
    return speeds
    
check_speeds(speeds)

pickle.dump(speeds, open(os.path.join(path, session_name, 'speeds.p'), "wb" ), 2)
        
# 4 speeds, 2 blocks of 240 sentences 

exec(open("./main.py").read())
import pickle
pickle.dump(info, open(os.path.join(path, session_name, 'info.pkl'),'wb'))

#Shuffle sentences
indices = list(range(len(sentences)))
shuffle(indices) # Contains shuffled indices for the stimuli. We will remove used indices in real time

os.chdir(os.path.join(path, session_name))

for i_block in range(nb_block):
        speed = speeds[i_block]
        os.chdir(os.path.join(path, session_name))
        os.mkdir('block' + str(i_block) + '_' + str(speed) + 'ms')
        os.chdir(os.path.join(path, session_name, 'block' + str(i_block) + '_' + str(speed) + 'ms'))
        stimuli = []
        info_stim = []
        for dummy in range(len_block//2): #correct sentences
            stimuli.append(sentences[indices[0]])
            info_stim.append(info[indices[0]])
            info_stim[-1]['anomaly'] = 'correct'
            indices.remove(indices[0])
        for dummy in range(len_block//6):
            stimuli.append(sentences_string_anomaly[indices[0]])
            info_stim.append(info[indices[0]])
            info_stim[-1]['anomaly'] = 'string'
            indices.remove(indices[0])
        for dummy in range(len_block//6):
            stimuli.append(sentences_syntaxic_anomaly[indices[0]])
            info_stim.append(info[indices[0]])
            info_stim[-1]['anomaly'] = 'syntax'
            indices.remove(indices[0])            
        for dummy in range(len_block//6):
            stimuli.append(sentences_semantic_anomaly[indices[0]])
            info_stim.append(info[indices[0]])
            info_stim[-1]['anomaly'] = 'semantic'
            indices.remove(indices[0]) 
            
        #shuffle block
        block_indices = list(range(len(stimuli)))
        shuffle(block_indices)
        final_stimuli = [stimuli[block_indices[i]] for i in range(len(stimuli))]
        final_info_stim = [info_stim[block_indices[i]] for i in range(len(stimuli))]
        
        pickle.dump(final_stimuli, open(os.path.join(path ,session_name,  'block' + str(i_block) + '_' + str(speed) + 'ms', 'stimuli.p'), "wb" ), 2)
        pickle.dump(final_info_stim, open(os.path.join(path, session_name, 'block' + str(i_block) + '_' + str(speed) + 'ms', 'info_stim.p'), "wb" ), 2)
        
        #save anomalies
        for i_sent in range(len(final_info_stim)):
            if final_info_stim[i_sent]['anomaly'] == 'correct':
                anomalies.append(0)
            else:
                anomalies.append(1)

pickle.dump(anomalies, open(os.path.join(path, session_name, 'anomalies.p'), "wb" ), 2)
