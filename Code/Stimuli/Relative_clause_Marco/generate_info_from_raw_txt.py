# This script parse Marco's sentences + metadata files into separate files: sentences, Theo's pkl meta file and
# Tal's meta file.

import argparse

parser = argparse.ArgumentParser(description='Switching from Marco files to Tal format')
parser.add_argument('-i', '--input', required=True, help='Input sentences in Marco\'s format')
parser.add_argument('-o', '--output', required=True, help='Filename (without extension) for Tal\'s format - only path and basename should be specified. The script will then generate three files with the following extensions: text (sentences), gold (labels)  and info (pickle in Theo\'s format), which can be then used for further analyses and ablation experiments.')
parser.add_argument('-f', '--filter-sentences', action='store_true', default=False, help = 'whether to filter sentences according to specific stimulus types (e.g., only subjrel_that). If this argument is given then the user needs to change the \'hard-coded\' keep_sentences var at the top of the code.')
args = parser.parse_args()

if args.filter_sentences:
    # Sublists containing which types of sentences to keep in the output files
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
    double_subjrel = True if curr_info['RC_type'] == 'double_subjrel_that' else False # double_subjrel has a different number of elements in each row of Marco generator output.
    curr_info['sentence_length'] = len(curr_line)
    curr_info['number_1'] = curr_line[2]
    curr_info['number_2'] = curr_line[3]
    curr_info['number_3'] = curr_line[4+double_subjrel]
    curr_info['verb_1_wrong'] = curr_line[5+double_subjrel]
    curr_info['verb_2_wrong'] = curr_line[6+double_subjrel]
    if double_subjrel:
        curr_info['number_4'] = curr_line[4]
        curr_info['verb_3_wrong'] = curr_line[8]
    info.append(curr_info)

# Filter certain sentence types if desired.
if args.filter_sentences:
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
   verb_2_position = None
   if curr_info['RC_type'] == 'objrel':
       verb2_position = 5
       verb2_correct = sentence.split(' ')[verb2_position].strip()
       verb2_wrong = curr_info['verb_2_wrong'].strip()
   elif curr_info['RC_type'] == 'objrel_that':
       verb2_position = 6
       verb2_correct = sentence.split(' ')[verb2_position].strip()
       verb2_wrong = curr_info['verb_2_wrong'].strip()
   elif curr_info['RC_type'] == 'subjrel_that':
       verb2_position = 6
       verb2_correct = sentence.split(' ')[verb2_position].strip()
       verb2_wrong = curr_info['verb_2_wrong'].strip()
   elif curr_info['RC_type'] == 'double_subjrel_that':
       verb2_position = 10 # Note that in this case of double subjrel we typically test the network on the *third* and not second verb in the sentence.
       verb2_correct = sentence.split(' ')[verb2_position].strip()
       verb2_wrong = curr_info['verb_3_wrong'].strip()
   else:
       print(curr_info['RC_type'])
       verb2_position = '0'
       verb2_correct = ''
       verb2_wrong = ''

   num_attributes = '-999'
   line_Tal = str(verb2_position) + '\t' + verb2_correct + '\t' + verb2_wrong + '\t' + num_attributes + '\n'


   sentences_Tal.append(sentence)
   gold_Tal.append(line_Tal)
   info_Tal.append(curr_info)



import os, pickle
# Save sentences in a text file
with open(args.output + '.text', 'w') as f:
    f.writelines(sentences_Tal)
    print('Sentences, gold labels and info files were saved to: ' + os.path.dirname(args.output))

# Save meta for Tal's agreement task
with open(args.output + '.gold', 'w') as f:
    f.writelines(gold_Tal)

# Save info in Theo's format
with open(args.output + '.info', 'wb') as f:
    pickle.dump(info_Tal, f)

