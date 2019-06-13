import argparse
import numpy as np
from lexicon_Italian import Words

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-n', '--natask', default='embedding_mental', type=str, help = 'Number-agreement (NA) task to generate (nounpp/subjrel_that/objrel_that)')
parser.add_argument('-seed', default=1 , type=int, help = 'Random seed for replicability')
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


def get_random_article(determiners):
    # Generates a random (definite) article
    rand_gender = ['masculine', 'feminine'][np.random.randint(2)]
    rand_number = ['singular', 'plural'][np.random.randint(2)]
    num_possible_articles = len(determiners['definit'][rand_gender][rand_number])
    rand_IX = np.random.randint(num_possible_articles)
    return determiners['definit'][rand_gender][rand_number][rand_IX]


np.random.seed(args.seed)
# Create counter
counter = {}
for attractor1_gender in ['masculine', 'feminine']:
    for attractor1_number in ['singular', 'plural']:
        for gender in ['masculine', 'feminine']:
            for number in ['singular', 'plural']:
                counter["_".join([gender, number, attractor1_gender, attractor1_number])] = 0

# Generate sentences and print to terminal

#### nounPP #####
if args.natask == 'nounpp':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            N1s = Words['nouns'][subject_gender][subject_number]
            for n1, subject in enumerate(N1s):
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                DP = det + ' ' + subject
                for attractor1_gender in ['masculine', 'feminine']:
                    for attractor1_number in ['singular', 'plural']:
                        N2s = Words['location_nouns'][attractor1_gender][attractor1_number]
                        for n2, attractor in enumerate(N2s):
                            IX_attractor = construct_DP(attractor, attractor1_gender, attractor1_number)
                            if n1 != n2:
                                for prep in Words['loc_preps']:
                                    prep_word, prep_article = prep.split(' ')
                                    article = Words['determinants'][prep_article][attractor1_gender][attractor1_number][IX_attractor]
                                    NP = ' '.join([DP] + [prep_word] + [article] + [attractor])
                                    for v, verb in enumerate(Words['verbs'][subject_number]):
                                        opposite_number = 'singular' if subject_number == 'plural' else 'plural'
                                        last_article = get_random_article(Words['determinants'])
                                        sentence = NP + ' ' + verb + ' ' + last_article
                                        print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor1_gender, attractor1_number, Words['verbs'][opposite_number][v]))
                                        counter["_".join([subject_gender, subject_number, attractor1_gender, attractor1_number])] += 1


if args.natask == 'subjrel_that':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            N1s = Words['nouns'][subject_gender][subject_number]
            for n1, subject in enumerate(N1s):
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                NP_start = det + ' ' + subject
                for attractor1_gender in ['masculine', 'feminine']:
                    for attractor1_number in ['singular', 'plural']:
                        N2s = Words['nouns'][attractor1_gender][attractor1_number]
                        for n2, attractor in enumerate(N2s):
                            IX_attractor = construct_DP(attractor, attractor1_gender, attractor1_number)
                            if n1 != n2: # check noun repetition at the lemma level
                                article = Words['determinants']['definit'][attractor1_gender][attractor1_number][IX_attractor]
                                for v1, verb1 in enumerate(Words['verbs'][subject_number]):
                                    clause = ' '.join(['che', verb1, article, attractor])
                                    for v2, verb2 in enumerate(Words['verbs'][subject_number]):
                                        if v1 != v2: # check verb repetition at the lemma level
                                            opposite_number_V1 = 'singular' if subject_number == 'plural' else 'plural'
                                            opposite_number_V2 = 'singular' if subject_number == 'plural' else 'plural'
                                            last_article = get_random_article(Words['determinants'])
                                            sentence = NP_start + ' ' + clause + ' ' + verb2 + ' ' + last_article
                                            print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor1_gender, attractor1_number, Words['verbs'][opposite_number_V1][v1], Words['verbs'][opposite_number_V2][v2]))
                                            counter["_".join([subject_gender, subject_number, attractor1_gender, attractor1_number])] += 1


if args.natask == 'objrel_that':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            N1s = Words['nouns'][subject_gender][subject_number]
            for n1, subject in enumerate(N1s):
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                NP_start = det + ' ' + subject
                for attractor1_gender in ['masculine', 'feminine']:
                    for attractor1_number in ['singular', 'plural']:
                        N2s = Words['nouns'][attractor1_gender][attractor1_number]
                        for n2, attractor in enumerate(N2s):
                            IX_attractor = construct_DP(attractor, attractor1_gender, attractor1_number)
                            if n1 != n2: # check noun repetition at the lemma level
                                article = Words['determinants']['definit'][attractor1_gender][attractor1_number][IX_attractor]
                                for v1, verb1 in enumerate(Words['verbs'][attractor1_number]):
                                    clause = ' '.join(['che', article, attractor, verb1])
                                    for v2, verb2 in enumerate(Words['verbs'][subject_number]):
                                        if v1 != v2: # check verb repetition at the lemma level
                                            opposite_number_V1 = 'singular' if attractor1_number == 'plural' else 'plural'
                                            opposite_number_V2 = 'singular' if subject_number == 'plural' else 'plural'
                                            last_article = get_random_article(Words['determinants'])
                                            sentence = NP_start + ' ' + clause + ' ' + verb2 + ' ' + last_article
                                            print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor1_gender, attractor1_number, Words['verbs'][opposite_number_V1][v1], Words['verbs'][opposite_number_V2][v2]))
                                            counter["_".join([subject_gender, subject_number, attractor1_gender, attractor1_number])] += 1

#num_nouns = 1
# The N1 thinks that the N2 P the N3 V2
if args.natask == 'objrel_nounpp':
    for N1_gender in ['masculine', 'feminine']:
        for N1_number in ['singular', 'plural']:
            N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
            for IX_N1, N1 in enumerate(N1s):
                IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
                det = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
                NP_start = det + ' ' + N1
                for N2_gender in ['masculine', 'feminine']:
                    for N2_number in ['singular', 'plural']:
                        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
                        for IX_N2, N2 in enumerate(N2s):
                            IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
                            if IX_N1 != IX_N2: # check noun repetition at the lemma level
                                det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
                                V2s = Words['verbs'][N2_number]#[0:num_nouns]
                                for IX_V2, V2 in enumerate(V2s): # innter agreement
                                    for N3_gender in ['masculine', 'feminine']:
                                        for N3_number in ['singular', 'plural']:
                                            N3s = Words['location_nouns'][N3_gender][N3_number]#[0:num_nouns]
                                            for IX_N3, N3 in enumerate(N3s):
                                                IX_det_N3 = construct_DP(N3, N3_gender, N3_number)
                                                if IX_N1!=IX_N3 and IX_N2!=IX_N3:
                                                    for prep in Words['loc_preps']:
                                                        prep_word, prep_article = prep.split(' ')
                                                        det_N3 = Words['determinants'][prep_article][N3_gender][N3_number][IX_det_N3]
                                                        clause = ' '.join(['che', det_N2, N2, prep_word, det_N3, N3, V2])
                                                        V1s = Words['verbs'][N1_number]#[0:num_nouns]
                                                        for IX_V1, V1 in enumerate(V1s):
                                                            if IX_V1 != IX_V2: # check verb repetition at the lemma level
                                                                opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
                                                                opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
                                                                last_article = get_random_article(Words['determinants'])
                                                                sentence = NP_start + ' ' + clause + ' ' + V1 + ' ' + last_article
                                                                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                                                                       args.natask, sentence,
                                                                       N1_gender, N1_number,
                                                                       N2_gender, N2_number,
                                                                       N3_gender, N3_number,
                                                                       Words['verbs'][opposite_number_V2][IX_V2], Words['verbs'][opposite_number_V1][IX_V1]))
                                            #                    counter["_".join([N1_gender, N1_number, N2_gender, attractor1_number])] += 1



#num_nouns = 5
# The N1 P the N3 that the N2 V2 V1 (N1 P N3 N2 V2 V1)
if args.natask == 'nounpp_objrel':
    for N1_gender in ['masculine', 'feminine']:
        for N1_number in ['singular', 'plural']:
            N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
            for IX_N1, N1 in enumerate(N1s):
                IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
                det = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
                NP_start = det + ' ' + N1
                for N3_gender in ['masculine', 'feminine']:
                    for N3_number in ['singular', 'plural']:
                        N3s = Words['location_nouns'][N3_gender][N3_number]#[0:num_nouns]
                        for IX_N3, N3 in enumerate(N3s):
                            if IX_N1 != IX_N3: # check noun repetition at the lemma level
                                IX_det_N3 = construct_DP(N3, N3_gender, N3_number)
                                for prep in Words['loc_preps']:
                                    prep_word, prep_article = prep.split(' ')
                                    det_N3 = Words['determinants'][prep_article][N3_gender][N3_number][IX_det_N3]
                                    NP = NP_start + ' ' + prep_word + ' ' + det_N3 + ' ' + N3 
                                    for N2_gender in ['masculine', 'feminine']:
                                        for N2_number in ['singular', 'plural']:
                                            N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
                                            for IX_N2, N2 in enumerate(N2s):
                                                if IX_N2!=IX_N1 and IX_N2!=IX_N3:
                                                    IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
                                                    det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
                                                    for IX_V2, V2 in enumerate(Words['verbs'][N2_number]): # innter agreement
                                                        clause = ' '.join(['che', det_N2, N2, V2])
                                                        for IX_V1, V1 in enumerate(Words['verbs'][N1_number]):
                                                            if IX_V1 != IX_V2: # check verb repetition at the lemma level
                                                                opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
                                                                opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
                                                                last_article = get_random_article(Words['determinants'])
                                                                sentence = NP + ' ' + clause + ' ' + V1 + ' ' + last_article
                                                                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                                                                       args.natask, sentence,
                                                                       N1_gender, N1_number,
                                                                       N3_gender, N3_number,
                                                                       N2_gender, N2_number,
                                                                       Words['verbs'][opposite_number_V2][IX_V2], Words['verbs'][opposite_number_V1][IX_V1]))
                                            #                    counter["_".join([N1_gender, N1_number, N2_gender, attractor1_number])] += 1

<<<<<<< HEAD
# The N1 that the N2 P the N3 V2 V1 (N1 N2 P N3 V2 V1)
num_nouns=4
if args.natask == 'embedding_mental':
    for N1_gender in ['masculine', 'feminine']:
        for N1_number in ['singular', 'plural']:
            N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
            for IX_N1, N1 in enumerate(N1s):
                IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
                det = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
                V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
                for IX_V1, V1 in enumerate(V1s):
                    NP_start = det + ' ' + N1 + ' ' + V1

                    for N2_gender in ['masculine', 'feminine']:
                        for N2_number in ['singular', 'plural']:
                            N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
                            for IX_N2, N2 in enumerate(N2s):
                                IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
                                if IX_N1 != IX_N2: # check noun repetition at the lemma level
                                    det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
                                    for IX_V2, V2 in enumerate(Words['verbs'][N2_number]):  # innter agreement
                                        for N3_gender in ['masculine', 'feminine']:
                                            for N3_number in ['singular', 'plural']:
                                                N3s = Words['location_nouns'][N3_gender][N3_number]#[0:num_nouns]
                                                for IX_N3, N3 in enumerate(N3s):
                                                    IX_det_N3 = construct_DP(N3, N3_gender, N3_number)
                                                    if IX_N1 != IX_N3 and IX_N2 != IX_N3:
                                                        for prep in Words['loc_preps']:
                                                            prep_word, prep_article = prep.split(' ')
                                                            det_N3 = Words['determinants'][prep_article][N3_gender][N3_number][IX_det_N3]
                                                            clause = ' '.join(['che', det_N2, N2, prep_word, det_N3, N3, V2])
                                                            V2s = Words['verbs'][N2_number]#[0:num_nouns]
                                                            for IX_V2, V2 in enumerate(V2s):
                                                                opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
                                                                opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
                                                                last_article = get_random_article(Words['determinants'])
                                                                sentence = NP_start + ' ' + clause + ' ' + last_article
                                                                print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                                                                       args.natask, sentence,
                                                                       N1_gender, N1_number,
                                                                       N2_gender, N2_number,
                                                                       N3_gender, N3_number,
                                                                       Words['verbs'][opposite_number_V2][IX_V2], Words['matrix_verbs'][opposite_number_V1][IX_V1]))




if args.natask == 'nounpp_copula':
    for subject_gender in ['masculine', 'feminine']:
        opposite_gender = 'masculine' if subject_gender == 'feminine' else 'feminine'
        for subject_number in ['singular', 'plural']:
            opposite_number = 'singular' if subject_number == 'plural' else 'plural'
            N1s = Words['nouns'][subject_gender][subject_number]
            for n1, subject in enumerate(N1s):
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                DP = det + ' ' + subject
                for attractor1_gender in ['masculine', 'feminine']:
                    for attractor1_number in ['singular', 'plural']:
                        N2s = Words['location_nouns'][attractor1_gender][attractor1_number]
                        for n2, attractor in enumerate(N2s):
                            IX_attractor = construct_DP(attractor, attractor1_gender, attractor1_number)
                            if n1 != n2:
                                for prep in Words['loc_preps']:
                                    prep_word, prep_article = prep.split(' ')
                                    article = Words['determinants'][prep_article][attractor1_gender][attractor1_number][IX_attractor]
                                    NP = ' '.join([DP] + [prep_word] + [article] + [attractor])
                                    verb = Words['copula'][subject_number]
                                    for a, adjective in enumerate(Words['adjectives'][subject_gender][subject_number]):
                                        sentence = NP + ' ' + verb + ' ' + adjective
                                        print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor1_gender, attractor1_number, Words['copula'][opposite_number], Words['adjectives'][opposite_gender][subject_number][a]))
                                        counter["_".join([subject_gender, subject_number, attractor1_gender, attractor1_number])] += 1



if not all(x==list(counter.values())[0] for x in counter.values()):
    raise Exception("Number of conditions mismatch: ", counter)
