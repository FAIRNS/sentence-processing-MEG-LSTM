path2input_text = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/objrel_objrel_that_subjrel_that.txt'
path2output_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_english_marco.txt'
path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_english_marco.p'
keep_sentences = [['subjrel_that', 'singular', 'singular'], ['subjrel_that', 'plural', 'singular'], ['subjrel_that', 'plural', 'plural'], ['objrel', 'plural', 'plural'], ['objrel_that', 'plural', 'plural']]
# Open raw text file from Marco's sentence generator
with open(path2input_text, 'r') as f:
    raw_sentences = f.readlines()

# Split each row to different fields and save separately the sentences and the info
sentences = [line.split('\t')[1]+ '\n' for line in raw_sentences]
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
        curr_info['verb_1'] = curr_line[5]
    if len(curr_line) > 6:
        curr_info['verb_2'] = curr_line[6]
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



# Save info list to drive
import pickle
with open(path2output_sentences, 'w') as f:
    f.writelines(sentences)

with open(path2output_info, 'wb') as f:
    pickle.dump(info, f)

path2input_text = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_double_subjrel_that_english_marco.txt'
path2output_sentences = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_double_english_marco.txt'
path2output_info = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/info_RC_double_english_marco.p'

# Open raw text file from Marco's sentence generator
with open(path2input_text, 'r') as f:
    data = f.readlines()

# Split each row to different fields and save separately the sentences and the info
sentences = [line.split('\t')[1]+ '\n' for line in data]
info = []
for line in data:
    curr_info = {}
    curr_info['RC_type'] = line.split('\t')[0]
    curr_info['sentence_length'] = len(line.split('\t'))
    curr_info['number_1'] = line.split('\t')[2]
    curr_info['number_2'] = line.split('\t')[3]
    curr_info['number_3'] = line.split('\t')[4]
    curr_info['number_4'] = line.split('\t')[5]
    curr_info['verb_1'] = line.split('\t')[6]
    curr_info['verb_2'] = line.split('\t')[7]
    curr_info['verb_3'] = line.split('\t')[8]
    info.append(curr_info)

# Save info list to drive
import pickle
with open(path2output_sentences, 'w') as f:
    f.writelines(sentences)

with open(path2output_info, 'wb') as f:
    pickle.dump(info, f)
