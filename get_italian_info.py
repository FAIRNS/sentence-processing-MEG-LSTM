import pickle
import re
import sys

pref = sys.argv[1]

f = open(pref+'.txt', 'r')
o = open(pref+'.pickle', 'w')

info = {}

for line in f:
    parts = line.split('\t')
    sent = ' '.join(parts[1].split()[:-1])
    sent_type = parts[0]
    prefix = ' '.join(sent.split()[:-1])
    subj_number = parts[3]
    attr_number = parts[5]
    incorrect_verb = parts[-1].strip()
    correct_verb = sent.split()[-1]
    
    # put all in dictionary
    info[sent] = {}
    info[sent]['sent_type'] = sent_type
    info[sent]['prefix'] = prefix
    info[sent]['subj_number'] = subj_number
    info[sent]['attr_number'] = attr_number
    info[sent]['incorrect_verb'] = incorrect_verb
    info[sent]['correct_verb'] = correct_verb

pickle.dump(info, o)
o.close()

