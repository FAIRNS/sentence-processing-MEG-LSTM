# This script parse Marco's sentences + metadata files into separate files: sentences, Theo's pkl meta file and
# Tal's meta file.

import argparse

parser = argparse.ArgumentParser(description='Switching from Marco files to Tal format')
parser.add_argument('-i', '--input', required=True, help='Input sentences in Marco\'s format')
parser.add_argument('-s', '--sentences', required=True, help='Output sentences in Tal\'s format')
parser.add_argument('-o', '--info', required=True, help='Output info pickle file in Theo\'s format')
parser.add_argument('-t', '--tal_fn', required=True, help='Output meta file for agreement task in Tal\'s format')
args = parser.parse_args()

keep_sentences = [['subjrel_that', 'singular', 'singular'], ['subjrel_that', 'plural', 'singular'], ['subjrel_that', 'plural', 'plural'], ['objrel', 'plural', 'plural'], ['objrel_that', 'plural', 'plural']]
# Open raw text file from Marco's sentence generator
with open(args.input, 'r') as f:
    raw_sentences = f.readlines()

# Split each row to different fields and save separately the sentences and the info
sentences = [line.split('\t')[1]+ '\n' for line in raw_sentences]
# For Theo's format:
info = []
for line in raw_sentences:
    curr_info = {}
    curr_line = line.split('\t')
    curr_info['RC_type'] = curr_line[0]
    curr_info['sentence_length'] = len(curr_line)
    curr_info['number_1'] = curr_line[2]
    curr_info['number_2'] = curr_line[3]
    if len(curr_line)>4:
        curr_info['number_3'] = curr_line[4]
    if len(curr_line) > 5:
        curr_info['verb_1_wrong'] = curr_line[5]
    if len(curr_line) > 6:
        curr_info['verb_2_wrong'] = curr_line[6]
    info.append(curr_info)

# Filter certain sentence types if desired.
if keep_sentences:
    IX_to_keep = []
    for sent_type in keep_sentences:
        IX_to_keep.append([IX for IX, sent_info in enumerate(info) if
                      sent_info['RC_type'] == sent_type[0] and
                      sent_info['number_1'] == sent_type[1] and
                      sent_info['number_2'] == sent_type[2]])
    IX_to_keep = [IX for sublist in IX_to_keep for IX in sublist]
    # Filter sentence and info
    sentences = [curr_sentence for IX, curr_sentence in enumerate(sentences) if IX in IX_to_keep]
    info = [curr_info for IX, curr_info in enumerate(info) if IX in IX_to_keep]


# Prepare in Tal's format:
sentences_Tal = []; gold_Tal = []; info_Tal = []
for sentence, curr_info in zip(sentences, info):
    # curr_line = line.split('\t')
    if curr_info['RC_type'] == 'objrel': # analyzing ONLY OBJREL for 1149
        verb1_position = '4'
        verb2_position = 5
        verb2_correct = sentence.split(' ')[verb2_position].strip()
        verb2_wrong = curr_info['verb_2_wrong'].strip()
        num_attributes = '-999'
        line_Tal = str(verb2_position) + '\t' + verb2_correct + '\t' + verb2_wrong + '\t' + num_attributes + '\n'

        sentences_Tal.append(sentence)
        gold_Tal.append(line_Tal)
        info_Tal.append(curr_info)



import pickle
# Save sentences
with open(args.sentences, 'w') as f:
    f.writelines(sentences)

# Save info in Theo's format
with open(args.info, 'wb') as f:
    pickle.dump(info, f)

# Save sentences for Tal's agreement task
with open(args.tal_fn + '.text', 'w') as f:
    f.writelines(sentences_Tal)

# Save meta for Tal's agreement task
with open(args.tal_fn + '.gold', 'w') as f:
    f.writelines(gold_Tal)

# Save info for Tal's agreement task
with open(args.tal_fn + '.info', 'wb') as f:
    pickle.dump(info_Tal, f)

# ------------------------------------------------------------
# path2input_text = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/objrel_objrel_that_subjrel_that.txt'
# path2output_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_english_marco.txt'
# path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_english_marco.p'


# path2input_text = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_double_subjrel_that_english_marco.txt'
# path2output_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_double_english_marco.txt'
# path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_double_english_marco.p'
#
# # Open raw text file from Marco's sentence generator
# with open(path2input_text, 'r') as f:
#     data = f.readlines()
#
# # Split each row to different fields and save separately the sentences and the info
# sentences = [line.split('\t')[1]+ '\n' for line in data]
# info = []
# for line in data:
#     curr_info = {}
#     curr_info['RC_type'] = line.split('\t')[0]
#     curr_info['sentence_length'] = len(line.split('\t'))
#     curr_info['number_1'] = line.split('\t')[2]
#     curr_info['number_2'] = line.split('\t')[3]
#     curr_info['number_3'] = line.split('\t')[4]
#     curr_info['number_4'] = line.split('\t')[5]
#     curr_info['verb_1'] = line.split('\t')[6]
#     curr_info['verb_2'] = line.split('\t')[7]
#     curr_info['verb_3'] = line.split('\t')[8]
#     info.append(curr_info)
#
# # Save info list to drive
# import pickle
# with open(path2output_sentences, 'w') as f:
#     f.writelines(sentences)
#
# with open(path2output_info, 'wb') as f:
#     pickle.dump(info, f)
