import argparse

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-f', '--data-filename', default='example.txt', type=str, help = 'filename of the dataset')
parser.add_argument('-n', default=4000 , type=int, help = 'number of samples from each condition')
parser.add_argument('--max-iter', default=10 , type=int, help = 'maximal number of allowed iterations over the input text file')
args = parser.parse_args()


def counter_fullfilled(counter, n):

    fullfilled = True
    for attractor_gender in ['masc', 'femi']:
        for attractor_number in ['sing', 'plur']:
            for gender in ['masc', 'femi']:
                for number in ['sing', 'plur']:
                    if counter["_".join([gender, number, attractor_gender, attractor_number])] < n:
                        fullfilled = False
    return fullfilled


# Create counter
counter = {}
for attractor_gender in ['masc', 'femi']:
    for attractor_number in ['sing', 'plur']:
        for gender in ['masc', 'femi']:
            for number in ['sing', 'plur']:
                counter["_".join([gender, number, attractor_gender, attractor_number])] = 0


import numpy as np
for iter in range(args.max_iter):
    with open(args.data_filename, 'r') as f:
        while not finished:
            # read line
            line = f.readline()
            if not line:
                break
            features = line.split('/t')[1::] # N1_gender, N1_number, N2_gender, N2_number
            if np.random.random.randint(
            counter["_".join(features)] += 1
            finished = counter_fullfilled(counter, n):

    if finished:
        break


    for subject_gender in ['masc', 'femi']:
        for subject_number in ['sing', 'plur']:
            subjects = Words['nouns'][subject_gender][subject_number]
            for subject in subjects:
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                DP = det + ' ' + subject
                for attractor_gender in ['masc', 'femi']:
                    for attractor_number in ['sing', 'plur']:
                        for attractor in Words['location_nouns'][attractor_gender][attractor_number]:
                            if subject != attractor:
                                IX_attractor = construct_DP(attractor, attractor_gender, attractor_number)
                                for prep in Words['loc_preps']:
                                    prep_word, prep_article = prep.split(' ')
                                    article = Words['determinants'][prep_article][attractor_gender][attractor_number][IX_attractor]
                                    NP = ' '.join([DP] + [prep_word] + [article] + [attractor])
                                    for verb in Words['verbs'][subject_number]:
                                        sentence = NP + ' ' + verb
                                        print('%s\t%s\t%s\t%s\t%s' % (sentence, subject_gender, subject_number, attractor_gender, attractor_number))
                                        counter["_".join([subject_gender, subject_number, attractor_gender, attractor_number])] += 1



if not all(x==list(counter.values())[0] for x in counter.values()):
    raise Exception("Number of conditions mismatch: ", counter)






