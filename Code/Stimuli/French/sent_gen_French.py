import argparse
from lexicon import Words

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for French')
parser.add_argument('-t', '--type', default='all', type=str, help = '{0-5, all}: one of six types of sentences in Theo dataset. "all" for looping over all types')
parser.add_argument('-n', '--natask', default='nounPP', type=str, help = 'Number-agreement (NA) task to generate')

args = parser.parse_args()
if args.type == 'all':
	types = range(6)
else:
	types = [int(args.type)]

# Create counter
counter = {}
for gender_attractor in ['masc', 'femi']:
    for number_attractor in ['sing', 'plur']:
        for gender in ['masc', 'femi']:
            for number in ['sing', 'plur']:
                counter["_".join([gender, number, gender_attractor, number_attractor])] = 0

# Generate sentences and print to terminal
for type in types:
	if args.natask == 'nounPP':
		for subject, gender, number in zip(Words[type]['subjects']['word'], Words[type]['subjects']['sexe'], Words[type]['subjects']['plurality']):
			det_type = 'determinants' if number == 'sing' else 'determinants_plural'
			for det in Words[type][det_type][gender]:
				for gender_attractor in ['masc', 'femi']:
					for number_attractor in ['sing', 'plur']:
						for PP in Words[type]['prepositions'][subject][gender_attractor][number_attractor]:
							NP = ' '.join([det] + [subject] + [PP])
							for tense in ['past', 'future']:
								for VP in Words[type]['verbs'][tense][number]:
									sentence = NP + ' ' + VP
									print('%s\t%s\t%s\t%s\t%s\t%s' % (sentence, tense, gender, number, gender_attractor, number_attractor))
									counter["_".join([gender, number, gender_attractor, number_attractor])] += 1 


	if args.natask == 'nounPPAdj':
		for subject, gender, number in zip(Words[type]['subjects']['word'], Words[type]['subjects']['sexe'], Words[type]['subjects']['plurality']):
			det_type = 'determinants' if number == 'sing' else 'determinants_plural'
			for det in Words[type][det_type][gender]:
				for gender_attractor in ['masc', 'femi']:
					for number_attractor in ['sing', 'plur']:
						for PP in Words[type]['prepositions'][subject][gender_attractor][number_attractor]:
							for adjectif in Words[type]['adjectives'][gender_attractor][number_attractor]:
								NP = ' '.join([det] + [subject] + [PP] + [adjectif])
								for tense in ['past', 'future']:
									for VP in Words[type]['verbs'][tense][number]:
										sentence = NP + ' ' + VP
										print('%s\t%s\t%s\t%s\t%s\t%s' % (sentence, tense, gender, number, gender_attractor, number_attractor))
										counter["_".join([gender, number, gender_attractor, number_attractor])] += 1

if not all(x==list(counter.values())[0] for x in counter.values()): 
    raise Exception("Number of conditions mismatch: ", counter)