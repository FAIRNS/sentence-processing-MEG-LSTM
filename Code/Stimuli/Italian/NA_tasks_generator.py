import argparse
from lexicon_Italian import Words

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-n', '--natask', default='objrel', type=str, help = 'Number-agreement (NA) task to generate')
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

# Create counter
counter = {}
for attractor_gender in ['masculine', 'feminine']:
    for attractor_number in ['singular', 'plural']:
        for gender in ['masculine', 'feminine']:
            for number in ['singular', 'plural']:
                counter["_".join([gender, number, attractor_gender, attractor_number])] = 0

# Generate sentences and print to terminal

#### nounPP #####
if args.natask == 'nounpp':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            subjects = Words['nouns'][subject_gender][subject_number]
            for subject in subjects:
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                DP = det + ' ' + subject
                for attractor_gender in ['masculine', 'feminine']:
                    for attractor_number in ['singular', 'plural']:
                        for attractor in Words['location_nouns'][attractor_gender][attractor_number]:
                            if subject != attractor:
                                IX_attractor = construct_DP(attractor, attractor_gender, attractor_number)
                                for prep in Words['loc_preps']:
                                    prep_word, prep_article = prep.split(' ')
                                    article = Words['determinants'][prep_article][attractor_gender][attractor_number][IX_attractor]
                                    NP = ' '.join([DP] + [prep_word] + [article] + [attractor])
                                    for v, verb in enumerate(Words['verbs'][subject_number]):
                                        opposite_number = 'singular' if subject_number == 'plural' else 'plural'
                                        sentence = NP + ' ' + verb
                                        print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor_gender, attractor_number, Words['verbs'][opposite_number][v]))
                                        counter["_".join([subject_gender, subject_number, attractor_gender, attractor_number])] += 1


if args.natask == 'subjrel':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            subjects = Words['nouns'][subject_gender][subject_number]
            for subject in subjects:
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                NP_start = det + ' ' + subject
                for attractor_gender in ['masculine', 'feminine']:
                    for attractor_number in ['singular', 'plural']:
                        for attractor in Words['nouns'][attractor_gender][attractor_number]:
                            if subject != attractor:
                                IX_attractor = construct_DP(attractor, attractor_gender, attractor_number)
                                article = Words['determinants']['definit'][attractor_gender][attractor_number][IX_attractor]
                                for v1, verb1 in enumerate(Words['verbs'][subject_number]):
                                    clause = ' '.join(['che', verb1, article, attractor])
                                    for v2, verb2 in enumerate(Words['verbs'][subject_number]):
                                        if verb1 != verb2:
                                            opposite_number = 'singular' if subject_number == 'plural' else 'plural'
                                            sentence = NP_start + ' ' + clause + ' ' + verb2
                                            print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor_gender, attractor_number, Words['verbs'][opposite_number][v1]))
                                            counter["_".join([subject_gender, subject_number, attractor_gender, attractor_number])] += 1


if args.natask == 'objrel':
    for subject_gender in ['masculine', 'feminine']:
        for subject_number in ['singular', 'plural']:
            subjects = Words['nouns'][subject_gender][subject_number]
            for subject in subjects:
                IX_subject = construct_DP(subject, subject_gender, subject_number)
                det = Words['determinants']['definit'][subject_gender][subject_number][IX_subject]
                NP_start = det + ' ' + subject
                for attractor_gender in ['masculine', 'feminine']:
                    for attractor_number in ['singular', 'plural']:
                        for attractor in Words['nouns'][attractor_gender][attractor_number]:
                            if subject != attractor:
                                IX_attractor = construct_DP(attractor, attractor_gender, attractor_number)
                                article = Words['determinants']['definit'][attractor_gender][attractor_number][IX_attractor]
                                for v1, verb1 in enumerate(Words['verbs'][attractor_number]):
                                    clause = ' '.join(['che', article, attractor, verb1])
                                    for v2, verb2 in enumerate(Words['verbs'][subject_number]):
                                        if verb1 != verb2:
                                            opposite_number = 'singular' if subject_number == 'plural' else 'plural'
                                            sentence = NP_start + ' ' + clause + ' ' + verb2
                                            print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (args.natask, sentence, subject_gender, subject_number, attractor_gender, attractor_number, Words['verbs'][opposite_number][v1]))
                                            counter["_".join([subject_gender, subject_number, attractor_gender, attractor_number])] += 1



if not all(x==list(counter.values())[0] for x in counter.values()):
    raise Exception("Number of conditions mismatch: ", counter)