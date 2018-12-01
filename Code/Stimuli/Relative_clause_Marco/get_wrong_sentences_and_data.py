import pickle
import numpy as np
import sys

pkl_file = sys.argv[1]
meta_file = sys.argv[2]
correct_index = int(sys.argv[3])
number_index = int(sys.argv[4])
target_verb_index = int(sys.argv[5])

all_data=pickle.load( open(pkl_file, "rb" ) )


# read metadata
number_of = {}
correct_sentence_of = {}
wrong_sentence_of = {}
correct_list = []
id_list = []
with open(meta_file) as f:
    for line in f:
        fields=line.strip().split("\t")
        id = fields[3]
        correct_flag = fields[correct_index]
        if (correct_flag == "correct"):
            number_of[id] = fields[number_index]
            correct_sentence_of[id] = fields[0]
        else:
            wrong_sentence_of[id] = fields[0]
        correct_list.append(correct_flag)
        id_list.append(id)
f.close()

correct_ll_of = {}
wrong_ll_of = {}

for sentence_counter_id, lls in enumerate(all_data['log_probabilities']):
    id = id_list[sentence_counter_id]
    if (correct_list[sentence_counter_id]=="correct"):
        correct_ll_of[id] = lls[target_verb_index]
    else:
        wrong_ll_of[id] = lls[target_verb_index]

for id in correct_ll_of:
    if correct_ll_of[id] < wrong_ll_of[id]:
        print(correct_sentence_of[id] + "\t" + number_of[id] + "\tcorrect\t" + id)
        print(wrong_sentence_of[id] + "\t" + number_of[id] + "\twrong\t" + id)
