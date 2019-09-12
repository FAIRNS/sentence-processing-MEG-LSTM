import argparse, os
from lexicon_Italian import Words
import numpy as np

parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
#parser.add_argument('-f', '--data-filename', default='/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Data/stimuli_for_nested_LR_dependencies_exp/Italian_embedding_mental_4032.txt', type=str, help = 'filename of input dataset')
#parser.add_argument('-f', '--data-filename', default='/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Data/stimuli_for_nested_LR_dependencies_exp/Italian_embedding_mental_SR_4000.txt', type=str, help = 'filename of input dataset')
#parser.add_argument('-f', '--data-filename', default='/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Data/stimuli_for_nested_LR_dependencies_exp/Italian_objrel_nounpp_4032.txt', type=str, help = 'filename of input dataset')
parser.add_argument('-f', '--data-filename', default='/home/yl254115/Projects/computational/FAIRNS/sentence-processing-MEG-LSTM/Data/stimuli_for_nested_LR_dependencies_exp/Italian_objrel_that_4000.txt', type=str, help = 'filename of input dataset')
args = parser.parse_args()


def construct_DP(subject, subject_gender, subject_number):
    ''' This function returns the index to the pertinent article given the gender and grammatical number of the noun.
    For example, singular nouns that begins with a vowel go with the article "l'" before them, whereas singular masculine
    starting with, e.g., 'sp' will go with 'lo'.
    !!! The function expects a FIXED structure for each type of article (see lexicon). For example,
    definit['masc']['sing'] = ['il', 'lo', "l'"]
    definit['masc']['plur'] = ['i', 'gli']
    definit['femi']['sing'] = ['la', "l'"]
    definit['femi']['plur'] = ['le']
    So for a singular noun starting with a vowel the function will return the index IX=-1 (last element in the list).
    For a singular masculin noun starting with 'sp' the function witll return the index IX=1, thus referring to 'lo'.

    :param subject: string of the noun (e.g., 'tavolo')
    :param subject_gender: string ('masc' or 'femi')
    :param subject_number: string ('plur' or 'sing')
    :return: IX [0, 1, or -1]. Index to the token in the list (assuming a fixed structure - see lexicon_*.py)
    '''
    vowels = ['a', 'e', 'i', 'o', 'u']
    special_consonants = ['y', 'z']
    special_bi_consonants = ['ps', 'pn', 'gn']

    # Tests for initial letters
    subject = subject.lower()
    starts_with_vowel = subject[0] in vowels
    starts_with_special_consonant = subject[0] in special_consonants or subject[0:1] in special_bi_consonants or (subject[0]=='s' and subject[1] not in vowels)

    IX = 0
    if subject_number == 'singular':
        if starts_with_vowel:
            IX = -1 # choose det l'
        elif subject_gender == 'masculine' and starts_with_special_consonant:
            IX = 1 # choose det 'lo'
    else: #plural
        if subject_gender == 'masculine' and (starts_with_vowel or starts_with_special_consonant or subject[0] == 'x'):
            IX = 1 # Choose det 'gli'

    return IX


objects = Words['location_nouns']

with open(args.data_filename, 'r') as f:
    data = f.readlines()
    data = [l.split('\t') for l in data]

new_data = []
for i, l in enumerate(data):
    curr_sentence = l[1]
    curr_sentence = curr_sentence.split(' ')
    last_det = curr_sentence[-1]

    print(i, last_det)

    already_in_sentence = True
    while already_in_sentence:
        random_gender = 'feminine' if np.random.randint(2) == 1 else 'masculine'
        random_number = 'singular' if np.random.randint(2) == 1 else 'plural'
        word_list = objects[random_gender][random_number]
        IX_word = np.random.randint(len(word_list))
        random_word = word_list[IX_word]
        already_in_sentence = False
        for word in curr_sentence:
            if len(word) > 2: # check if 3 first letters are the same
                cnt = 0
                for i in range(3):
                    if word[i] == random_word[i]:
                        cnt+=1
                if cnt == 3:
                    already_in_sentence = True
                    break

    IX_det = construct_DP(random_word, random_gender, random_number)
    det = Words['determinants']['definit'][random_gender][random_number][IX_det]

    curr_sentence = curr_sentence[:-1]
    new_sentence = curr_sentence + [det] + [random_word]
    l[1] = ' '.join(new_sentence)
    new_data.append(l)


dirname = os.path.dirname(args.data_filename)
filename = os.path.basename(args.data_filename)

with open(os.path.join(dirname, 'new_' + filename), 'w') as f_new:
    for l in new_data:
        f_new.write('\t'.join(l) + '\n')
