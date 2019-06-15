import pickle
import numpy as np
import sys
import glob
import os

pkl_folder = sys.argv[1]
#meta_file = sys.argv[2]
correct_index = int(sys.argv[2])
#number_index = int(sys.argv[4])

all_files = glob.glob(pkl_folder+"correct_wrong_*.txt")
#[correct_wrong_adv_adv.txt,  correct_wrong_adv_conjunction.txt,  correct_wrong_adv.txt,  correct_wrong_namepp.txt,  correct_wrong_nounpp.txt,  correct_wrong_simple.txt]


for file in all_files:
	corrects = 0
	total = 0
	with open(file) as f:
		for line in f:
			total += 1
			fields=line.strip().split("\t")
			correct_flag = fields[correct_index]
			if (correct_flag == "correct"):
				corrects += 1
	f.close()

	print(file.split(os.sep)[-1], str(corrects/total))	
