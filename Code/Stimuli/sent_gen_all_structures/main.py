'''
Sentence Generator
Made by Théo Desbordes
Last modification on the 27th of May 2018
Generated and tested on python 3.4.5
'''

## Import functions and words
from random import shuffle
import os

try: 
    path
except NameError: # if called from sent_gen.py, then no need to define all these variables
    path = '/home/yl254115/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/Stimuli/sent_gen_all_structures/example_sentences'
    os.chdir(path)
    session_name = 'example_sentences' # name of the folder in which the sentences will be saved
    nb_sent = 10000 # number of sentence to generate
 
from functions import *
from words import *

save = True # whether or not save the generated sentences
save_path = path # path to which the sentences will be saved

generate_jabberwocky_and_wordlists = False # Wether to create the jabbberwocky anomaly condityion or not

generate_NP_VP_transition = True # necessary for all structures

include_relative_clauses = False

generate_all_struct = True

## Construct sentences

sentences = []

anomaly_position_counter = [[0,0,0] for i in range(3)] # for each structure, for positions 4, 6 and 8

sentences_string_anomaly = [] # the word is replaced by a string of consonants
sentences_syntaxic_anomaly = [] # we change the category of the word (V<->N)
sentences_semantic_anomaly = [] # we change the meaning while keeping the category

if generate_jabberwocky_and_wordlists:
    sentences_jabberwocky_anomaly = []  # a word is replaced by its pseudoword counterpart
    wordlists = [] # list with the words but unordered
    wordlists_jabberwocky = [] # same in the jab condition

if generate_NP_VP_transition:
    sentences_NP_VP_transition_variation = []
    NP_end_counter = [0,0,0] # here we want only relatvie clause sentences
    VP_begin_counter = [0,0,0,0]

if include_relative_clauses:
    sentences_relative_clauses = []
    relative_clauses_conter = [0,0]

if generate_all_struct:
    sentences_all_struct = []
    structure_counter = [0,0,0]
    relative_clauses_conter = [0,0]
    adverb_struct_counter = [0,0]


for i in range(nb_sent):
    
    create_info(info)
    #print(info)

    type = get_type(Types, Types_counter)

    ###### !!! Stop the usage of sentences of type 0 and 3 , that use passive verbs , this also makes the type counter wrong !!!
    while type == 0 or type == 3:
        type = get_type(Types, Types_counter)
    
    structure = get_structure(structures)
    # structure = 2
    
    subject, ind_subject = get_subject(Words, type)
    
    det = get_det(Words, type, structure, ind_subject)
    
    verb = get_verb(Words, type, structure, ind_subject)
    
    object, ind_object = get_object(Words, type, structure)
    
    det2 = get_det2(Words, type, structure, ind_object)
    
    prepo = get_prepo(Words, type, structure)
    
    sentence = construct_sentence(structure, det, subject, prepo, verb, det2, object)
    sentences.append(sentence)
    
    #print('t=%s, struct=%s, sub=%s, d=%s, v=%s, o=%s, det2=%s, p=%s, %s' % (type, structure, subject, det, verb, object, det2, prepo, sentence))
    #print(sentence)
    # ind_anomaly_pos, anmaly_position, anomaly_position_counter = get_anomaly_position(structure, type, anomaly_position_counter)
            
    # sentence_string_anomaly = generate_string_anomaly(sentence, ind_anomaly_pos, structure)
    # sentences_string_anomaly.append(sentence_string_anomaly)
    
    # sentence_syntaxic_anomaly = generate_syntaxic_anomaly(Words, type, structure,  det, subject, prepo, verb, det2, object, ind_anomaly_pos, ind_subject)
    # sentences_syntaxic_anomaly.append(sentence_syntaxic_anomaly)
    
    # sentence_semantic_anomaly = generate_semantic_anomaly(Words, type, structure, det, subject, ind_subject, prepo, verb, det2, object, ind_object, ind_anomaly_pos)
    # sentences_semantic_anomaly.append(sentence_semantic_anomaly)
    
    if generate_jabberwocky_and_wordlists:
        sentence_jabberwocky_anomaly = generate_jabberwocky_anomaly(sentence, ind_anomaly_pos, word2jab, structure)
        sentences_jabberwocky_anomaly.append(sentence_jabberwocky_anomaly)
        
        wordlist = generate_wordlist()
        wordlists.append(wordlist)
        
        wordlist_jabberwocky = generate_jabberwocky_anomaly(wordlist, ind_anomaly_pos, word2jab, structure)
        wordlists_jabberwocky.append(wordlist_jabberwocky)

    if generate_NP_VP_transition:
        sentences_NP_VP_transition_variation.append( generate_NP_VP_transition_variation(sentence, NP_end_counter, VP_begin_counter) )

    if include_relative_clauses:
        sentences_relative_clauses.append( generate_relative_clauses(sentences_NP_VP_transition_variation[-1], relative_clauses_conter) ) 

    if generate_all_struct:
        sentences_all_struct.append( master_structure(sentences_NP_VP_transition_variation[-1], structure_counter, relative_clauses_conter, adverb_struct_counter) )         

## Save as text

if save:
    file_name = os.path.join(save_path, session_name) + os.sep

    if os.path.isdir(save_path + os.sep + session_name):
        import shutil
        shutil.rmtree(save_path + os.sep + session_name)
    os.mkdir(session_name)
    
    # for anomaly, Sentences in [('correct', sentences)]:#, ('string', sentences_string_anomaly),('syntaxic', sentences_syntaxic_anomaly), ('semantic', sentences_semantic_anomaly)]:
    #     file = open(file_name + anomaly + ".txt", "a")
    #     for sentence in Sentences:
    #         file.write(sentence + "\n")        
    #     file.close()
    
    if generate_jabberwocky_and_wordlists:
        file = open(file_name + 'jabberwocky' + ".txt", "a")
        for sentence in sentences_jabberwocky_anomaly:
            file.write(sentence + "\n")    
        file.close()

    # if generate_NP_VP_transition:
    #     file = open(file_name + 'NP_VP_transition' + ".txt", "a")
    #     for sentence in sentences_NP_VP_transition_variation:
    #         file.write(sentence + "\n")    
    #     file.close()
        
    if include_relative_clauses:
        file = open(file_name + 'relative_clauses' + ".txt", "a")
        for sentence in sentences_relative_clauses:
            file.write(sentence + "\n")    
        file.close()

    if generate_all_struct:
        file = open(file_name + 'all_struct' + ".txt", "a")
        for sentence in sentences_all_struct:
            file.write(sentence + "\n")    
        file.close()


    import pickle
    pickle.dump( info, open(file_name + 'info.p', 'wb') )
        


#After this point is just code for checking the quality of the sentences. Should not be active when you just want to generate sentences

## Show sentences


show = False

if show == True:
    for id_sent in range(len(sentences)):
        print(sentences[id_sent])
        print(sentences_syntaxic_anomaly[id_sent])
        print(sentences_semantic_anomaly[id_sent])
        print('structure: ', info[id_sent]['structure'], 'type: ',  info[id_sent]['type'], 'anomaly position: ', info[id_sent]['anomaly_position']+1)
        print('\n')


show = False

if show == True:
    print('\nCorrect sentences: \n')
    for sent in sentences:
        print(sent)
    print('\nString of consonants anomaly: \n')
    for sent in sentences_string_anomaly:
        print(sent)
    print('\nSyntactic anomaly: \n')
    for sent in sentences_syntaxic_anomaly:
        print(sent)
    print('\nSemantic anomaly: \n')
    for sent in sentences_semantic_anomaly:
        print(sent)
    print('\nJabberwocky anomaly: \n')
    for sent in sentences_jabberwocky_anomaly:
        print(sent)
    

## Analyse

analyse = False # show all the sentences containing the target word

target = 'alimenter'

if analyse:
    for sent in sentences:
        if target in sent.split():
            print(sent)

# for sentence in sentences:
#     if '' in sentence:
#         print(sentence)
