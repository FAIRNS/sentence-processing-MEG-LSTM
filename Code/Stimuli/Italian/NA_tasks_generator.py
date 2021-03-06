import sys, argparse
import numpy as np
from lexicon_Italian import Words

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-t', '--natask', default='embedding_mental', type=str, help = 'Number-agreement (NA) task to generate (nounpp/subjrel_that/objrel_that)')
parser.add_argument('-n', default=1 , type=int, help = 'number of samples from each condition')
parser.add_argument('-seed', default=1 , type=int, help = 'Random seed for replicability')
args = parser.parse_args()

stimuli = []
np.random.seed(args.seed)

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


def init_counter(features):
    # Create counter
    import itertools 
    counter = {}
    feature_combinations = list(itertools.product(*features.values())) 
    for comb in feature_combinations:
        counter['_'.join(comb)] = 0
    return counter


def counter_fullfilled(counter, n):
    return False if any(v < n for v in list(counter.values())) else True


# Generate sentences and print to terminal

# det N1 that the N2 V2 V1 det N3
if args.natask == 'simple_non':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    counter = init_counter(features)
    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # DET
        IX_subject = construct_DP(N1, N1_gender, N1_number)
        det = Words['determinants']['definit'][N1_gender][N1_number][IX_subject]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # sentence
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join([det, N1, 'non', V1, 'il'])

        if counter['_'.join([N1_gender, N1_number])] < args.n:
            stimuli.append([args.natask, sentence,
                   N1_gender, N1_number,
                   Words['verbs'][opposite_number_V1][IX_V1]])
            counter['_'.join([N1_gender, N1_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[2], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 1
    [print('\t'.join(l)) for l in stimuli]


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
# The N1 that the N2 P the N3 V2 V1 (N1 N2 P N3 V2 V1)
#num_nouns=4
if args.natask == 'embedding_mental':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']
    
    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
        det_N1 = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
        # V1
        V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
        det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        IX_det_N3 = construct_DP(N3, N3_gender, N3_number)
        # prep
        preps = Words['loc_preps']
        IX_prep = np.random.randint(len(preps))
        prep = preps[IX_prep]
        prep_word, prep_article = prep.split(' ')
        det_N3 = Words['determinants'][prep_article][N3_gender][N3_number][IX_det_N3]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join([det_N1, N1, V1, 'che', det_N2, N2, prep_word, det_N3, N3, V2, last_article]) 

        if IX_N1 != IX_N2 and IX_N1 != IX_N3 and IX_N2 != IX_N3: # check noun repetition at the lemma level
            if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])] < args.n:
                stimuli.append([args.natask, sentence,
                       N1_gender, N1_number,
                       N2_gender, N2_number,
                       N3_gender, N3_number,
                       Words['matrix_verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])]+=1 

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]



if args.natask == 'embedding_mental_SR':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']
    
    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
        det_N1 = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
        # V1
        V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
        det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join([det_N1, N1, V1, 'che', det_N2, N2, V2, last_article]) 

        if IX_N1 != IX_N2: # check noun repetition at the lemma level
            if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])] < args.n:
                stimuli.append([args.natask, sentence,
                       N1_gender, N1_number,
                       N2_gender, N2_number,
                       Words['matrix_verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])]+=1 

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]



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


# The N1 that the N2 P the N3 V2 V1 (N1 N2 P N3 V2 V1)
#num_nouns=4
if args.natask == 'double_subjrel':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']
    
    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        IX_det_N1 = construct_DP(N1, N1_gender, N1_number)
        det_N1 = Words['determinants']['definit'][N1_gender][N1_number][IX_det_N1]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        IX_det_N2 = construct_DP(N2, N2_gender, N2_number)
        det_N2 = Words['determinants']['definit'][N2_gender][N2_number][IX_det_N2]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        IX_det_N3 = construct_DP(N3, N3_gender, N3_number)
        det_N3 = Words['determinants']['definit'][N3_gender][N3_number][IX_det_N3]
        # V3
        V3s = Words['verbs'][N1_number]
        IX_V3 = np.random.randint(len(V3s))
        V3 = V3s[IX_V3]
        # sentence
        opposite_number_V3 = 'singular' if N1_number == 'plural' else 'plural'
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join([det_N1, N1, 'che', V1, det_N2, N2, 'che', V2, det_N3, N3, V3]) 

        if IX_N1 != IX_N2 and IX_N1 != IX_N3 and IX_N2 != IX_N3: # check noun repetition at the lemma level
            if IX_V1 != IX_V2 and IX_V1 != IX_V3 and IX_V2 != IX_V3: # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                       N1_gender, N1_number,
                       N2_gender, N2_number,
                       N3_gender, N3_number,
                       Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2], Words['verbs'][opposite_number_V3][IX_V3]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])]+=1 

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]


#if not all(x==list(counter.values())[0] for x in counter.values()):
#    raise Exception("Number of conditions mismatch: ", counter)
