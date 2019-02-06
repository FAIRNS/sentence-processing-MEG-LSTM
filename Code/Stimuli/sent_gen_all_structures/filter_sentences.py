import os, pickle

path2info_all_struct = 'example_sentences/info_all_struct.p'

# ALL STRUCTURES SENTENCES
info_all_struct = pickle.load(open(path2info_all_struct, 'rb'))

# identify all structures based on PoS sequence
pos = [info['PoS'] for info in info_all_struct]
pos = list(set(tuple(l) for l in pos))

sentences_all_structures = []
for s, struct in enumerate(pos):
    noun_types = [p for p in struct if 'Noun' in p]
    for subject_sexe in ['masc', 'femi']:
        for subject_plurality in ['sing', 'plur']:
            curr_sentences = []
            for info in info_all_struct:
                if info['PoS'] == list(struct) and info['subject_sexe'] == subject_sexe and info['subject_plurality'] == subject_plurality:
                    curr_sentences.append(info['sentence']+'\n')

            if len(curr_sentences) > 10:
                file_name = 'struct_' + str(s) + '_' + '_'.join([subject_sexe, subject_plurality]) + '.txt'
                with open(os.path.join('example_sentences', file_name), 'w') as f:
                    f.writelines(curr_sentences)