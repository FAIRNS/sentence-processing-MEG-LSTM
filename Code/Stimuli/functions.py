import random
import numpy as np
from words import *

## TOOLS & COUNTERS

def weighted_min_indice(list):
    weights = []
    for count in list:
        if count == 0:
            weights.append(1)
        else:
            weights.append(1/(count*count))
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
    
def Count(Counter, word):
    if word not in Counter['word']:
        Counter['word'].append(word)
        Counter['counter'].append(0) 
    Counter['counter'][Counter['word'].index(word)] += 1
    
def Count_infinitive_verbs(Counter, word):
    Counter['counter_infinitive_verbs'][Counter['infinitive_verbs'].index(word)] += 1
    
def add_info(info, word_type, word, ind, type, anomaly=False, tense=None, conjugated_verb=None, exception=False):
    if word_type == 'subjects':
        if not anomaly:
            info[-1]['subject'] = word
            info[-1]['subject_sexe'] = Words[type][word_type]['sexe'][ind]
            info[-1]['subject_plurality'] = Words[type][word_type]['plurality'][ind]
        elif anomaly == 'syntaxic':
            info[-1]['syntaxic_anomaly_type'] = word_type
            info[-1]['syntaxic_anomaly'] = word
            info[-1]['syntaxic_anomaly_sexe'] = Words[type][word_type]['sexe'][ind_subject]
            info[-1]['syntaxic_anomaly_plurality'] = Words[type][word_type]['plurality'][ind]
        elif anomaly == 'semantic':
            info[-1]['semantic_anomaly_type'] = word_type
            info[-1]['semantic_anomaly'] = word
            info[-1]['semantic_anomaly_sexe'] = Words[type][word_type]['sexe'][ind]
            info[-1]['semantic_anomaly_plurality'] = Words[type][word_type]['plurality'][ind]
            
    elif word_type == 'verbs':
        if not anomaly:
            info[-1]['verb'] = conjugated_verb
            info[-1]['verb_infinitive'] = verb
            info[-1]['tense'] = tense
        elif anomaly == 'syntaxic':
            # info.append(info[-1].copy())
            info[-1]['syntaxic_anomaly_type'] = word_type
            info[-1]['syntaxic_anomaly'] = word
        elif anomaly == 'semantic':
            info[-1]['semantic_anomaly_type'] = word_type
            info[-1]['semantic_anomaly'] = conjugated_verb
            info[-1]['semantic_anomaly_verb_infinitive'] = word
            info[-1]['semantic_anomaly_verb_tense'] = tense
            
    elif word_type == 'objects':
        if not anomaly:
            if exception:
                info[-1]['object_sexe'] = Words[type]['objects']['except_structure']['sexe'][ind_object]
                info[-1]['object_plurality'] = Words[type]['objects']['except_structure']['plurality'][ind_object]
            else:
                info[-1]['object_sexe'] = Words[type]['objects']['sexe'][ind_object]
                info[-1]['object_plurality'] = Words[type]['objects']['plurality'][ind_object]
            info[-1]['object'] = word
        elif anomaly == 'syntaxic':
            if exception:
                info[-1]['syntaxic_anomaly_sexe'] = Words[type]['objects']['except_structure']['sexe'][ind_object]
                info[-1]['syntaxic_anomaly_plurality'] = Words[type]['objects']['except_structure']['plurality'][ind_object]
            else:
                info[-1]['syntaxic_anomaly_sexe'] = Words[type]['objects']['sexe'][ind_object]
                info[-1]['syntaxic_anomaly_plurality'] = Words[type]['objects']['plurality'][ind_object]
            info[-1]['syntaxic_anomaly_type'] = word_type
            info[-1]['syntaxic_anomaly'] = word            
        elif anomaly == 'semantic':
            info[-1]['semantic_anomaly_type'] = word_type
            info[-1]['semantic_anomaly'] = word
            if exception:
                info[-1]['semantic_anomaly_sexe'] = Words[type]['objects']['except_structure']['sexe'][ind_object]
                info[-1]['semantic_anomaly_plurality'] = Words[type]['objects']['except_structure']['plurality'][ind_object]
            else:
                info[-1]['semantic_anomaly_sexe'] = Words[type]['objects']['sexe'][ind_object]
                info[-1]['semantic_anomaly_plurality'] = Words[type]['objects']['plurality'][ind]
        
    elif word_type =='det':
        info[-1]['det'] = word
    
    elif word_type =='det2':
        info[-1]['det2'] = word
        
    elif word_type == 'prepo':
        if not anomaly:
            info[-1]['prepo'] = word
        elif anomaly == 'syntaxic':
            info_syntac_anomaly[-1]['syntaxic_anomaly_type'] = word_type
            info_syntac_anomaly[-1]['syntaxic_anomaly'] = word    
        elif anomaly == 'semantic':
            info[-1]['semantic_anomaly_type'] = word_type
            info[-1]['semantic_anomaly'] = word
    
def create_info(info):
    info.append({})
    return info
    
## CONSTRUCT SENTENCES

def get_type(Types, Types_counter):   
    global info
    type = weighted_min_indice(Types_counter)
    Types_counter[type] += 1
    info[-1]['type'] = type
    return type
    
def get_structure(structures):
    global info
    ind_struct = weighted_min_indice(structures['counter'])
    structure = structures['structure'][ind_struct]
    structures['counter'][ind_struct] += 1
    info[-1]['structure'] = structure
    return structure
    
def get_subject(Words, type, count=True, anomaly=False):
    global subject, ind_subject, info
    #get subject
    ind_subject = weighted_min_indice(Words[type]['subjects']['counter'])   
    subject = Words[type]['subjects']['word'][ind_subject]
    #count and add info
    if count:
        Words[type]['subjects']['counter'][ind_subject] += 1
        Count(Counter, subject)
    add_info(info, 'subjects', subject, ind_subject, type, anomaly)
    return subject, ind_subject
    
def get_det(Words, type, structure, ind_subject, count=True):
    global ind_det, Counter , info
    # get det
    ind_det = weighted_min_indice(Words[type]['determinants']['counter'])
    if Words[type]['subjects']['sexe'][ind_subject] == 'masc':
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            det = Words[type]['determinants']['masc'][ind_det]
        else:
            det = Words[type]['determinants_plural']['masc'][ind_det]
    else:
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            det = Words[type]['determinants']['femi'][ind_det]
        else:
            det = Words[type]['determinants_plural']['femi'][ind_det]
    #count 
    if count:
        Words[type]['determinants']['counter'][ind_det] += 1
        Count(Counter, det)
    #match det
    det = match_det(Words, type, det, subject, Words[type]['subjects']['sexe'][ind_subject], 'subject', ind_subject, structure)
    #add info
    add_info(info, 'det', det, ind_det, type)
    return det
    
def get_verb(Words, type, structure, ind_subject, count=True, fixed_tense=False, anomaly=False, anom_anim=False):
    global verb, ind_verb, tense, ind_tense, Counter, info
    if anomaly == 'syntaxic' and type == 1: # Manger cannot be used because 'le manger is correct'.
        verb = 'avaler'
        ind_verb = 0
        add_info(info, 'verbs', verb, ind_verb, type, anomaly, tense)
        return verb
    if anomaly == 'syntaxic' and type == 2: # "...du bricoler" ressemble trop à "bricoleur"
        verb = 'réparer'
        ind_verb = 0
        add_info(info, 'verbs', verb, ind_verb, type, anomaly, tense)
        return verb
     
    if anomaly == 'semantic' and type in ([1,2,4,5]) and anom_anim: # then we choose specific verbs = germer, moisir, pourrir
        ind_verb = weighted_min_indice(Words[type]['verbs']['semantic_anom']['counter'])
        verb = Words[type]['verbs']['semantic_anom']['word'][ind_verb]
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            conjugated_verb = Words[type]['verbs']['semantic_anom'][tense]['sing'][ind_verb]
        elif Words[type]['subjects']['plurality'][ind_subject] == 'plur':
            conjugated_verb = Words[type]['verbs']['semantic_anom'][tense]['plur'][ind_verb]
            
    elif Words[type]['verbs']['except'][ind_subject] == 1: #exception for specific subject
        ind_verb = weighted_min_indice(Words[type]['verbs']['except_verbs']['counter'])
        verb = Words[type]['verbs']['except_verbs']['word'][ind_verb]
        if fixed_tense == True:
            pass
        else:
            ind_tense = weighted_min_indice(Words[type]['verbs']['except_verbs']['counter_tenses'])
            tense = Words[type]['verbs']['except_verbs']['tenses'][ind_tense]
        
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            conjugated_verb = Words[type]['verbs']['except_verbs'][tense]['sing'][ind_verb]
        elif Words[type]['subjects']['plurality'][ind_subject] == 'plur':
            conjugated_verb = Words[type]['verbs']['except_verbs'][tense]['plur'][ind_verb]
        if count:
            Words[type]['verbs']['except_verbs']['counter'][ind_verb] += 1
            Words[type]['verbs']['except_verbs']['counter_tenses'][ind_tense] += 1
    
    elif Words[type]['verbs']['except_struct'][structure-1] == 1 or (anomaly == 'semantic' and type == any([0,3])): # except for structure 3 : the verb is at the end of the sentence, same for semantic anomalies in types 0,3
        ind_verb = weighted_min_indice(Words[type]['verbs']['except_structure']['counter'])
        verb = Words[type]['verbs']['except_structure']['word'][ind_verb]
        if fixed_tense == True:
            pass
        else:
            ind_tense = weighted_min_indice(Words[type]['verbs']['except_structure']['counter_tenses'])
            tense = Words[type]['verbs']['except_structure']['tenses'][ind_tense]
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            conjugated_verb = Words[type]['verbs']['except_structure'][tense]['sing'][ind_verb]
        elif Words[type]['subjects']['plurality'][ind_subject] == 'plur':
            conjugated_verb = Words[type]['verbs']['except_structure'][tense]['plur'][ind_verb]
        if count:
            Words[type]['verbs']['except_structure']['counter'][ind_verb] += 1
            Words[type]['verbs']['except_structure']['counter_tenses'][ind_tense] += 1
    else:
        #no exception
        ind_verb = weighted_min_indice(Words[type]['verbs']['counter'])
        verb = Words[type]['verbs']['word'][ind_verb]
        if fixed_tense == True:
            pass
        elif len(Words[type]['verbs']['past']['sing']) == 1: # If only one tense, it's the future (past can lead to passive form like in 'est devenu')
            ind_tense = 1
            tense = 'future'
        else:
            ind_tense = weighted_min_indice(Words[type]['verbs']['counter_tenses'])
            tense = Words[type]['verbs']['tenses'][ind_tense]
        if Words[type]['subjects']['plurality'][ind_subject] == 'sing':
            conjugated_verb = Words[type]['verbs'][tense]['sing'][ind_verb]
        elif Words[type]['subjects']['plurality'][ind_subject] == 'plur':
            conjugated_verb = Words[type]['verbs'][tense]['plur'][ind_verb]
        if count:
            Words[type]['verbs']['counter'][ind_verb] += 1
            Words[type]['verbs']['counter_tenses'][ind_tense] += 1
    #count and add info
    if count:
        Count(Counter, conjugated_verb)
        Count_infinitive_verbs(Counter, verb)
    if anomaly == 'syntaxic':
        add_info(info, 'verbs', verb, ind_verb, type, anomaly, tense)
        return verb
    else:
        add_info(info, 'verbs', verb, ind_verb, type, anomaly, tense, conjugated_verb)
        return conjugated_verb
    
def get_object(Words, type, structure, count=True, anomaly=False):
    global ind_object, object, det2, ind_det2, Counter, info
    if structure == 3 and anomaly==False:  #then there is no object
        info[-1]['object'] = None
        return None, None
    else:
        if Words[type]['objects']['except_struct'][structure-1] == 1: #except structure 2 : long complement relative to object
            exception=True
            ind_object = weighted_min_indice(Words[type]['objects']['except_structure']['counter'])
            object = Words[type]['objects']['except_structure']['word'][ind_object]
            if count:
                Words[type]['objects']['except_structure']['counter'][ind_object] += 1
        elif type == 3: # The object need to be accorded to the subject (une graine donne une plante)
            exception = False
            if Words[type]['subjects']['plurality'][ind_subject] == 'plur':
                ind_object = weighted_min_indice(Words[type]['objects']['counter_plur']) + (int(len(Words[type]['objects']['word']) / 2))
            elif Words[type]['subjects']['plurality'][ind_subject] == 'sing':
                ind_object = weighted_min_indice(Words[type]['objects']['counter_sing'])
            object = Words[type]['objects']['word'][ind_object]
            if count:
                Words[type]['objects']['counter'][ind_object] += 1
                Words[type]['objects']['counter_plur'] = Words[type]['objects']['counter'][(int(len(Words[type]['objects']['word']) / 2))::]
                Words[type]['objects']['counter_sing'] = Words[type]['objects']['counter'][0:(int(len(Words[type]['objects']['word']) / 2))]
        
        else: # no exception
            exception = False
            ind_object = weighted_min_indice(Words[type]['objects']['counter'])
            object = Words[type]['objects']['word'][ind_object]
            if count:
                Words[type]['objects']['counter'][ind_object] += 1
        if count:
            Count(Counter, object)
        add_info(info, 'objects', object, ind_object, type, anomaly, exception=exception)
        return object, ind_object
    
def get_det2(Words, type, structure, ind_object, count=True):
    global ind_det2, object, Counter, info
    if structure == 3: #then there is no object so no 2nd det
        info[-1]['det2'] = None
        return None
    elif len(object.split()) > 1:
        info[-1]['det2'] = None
        return ''
    else:
        if Words[type]['exceptions']['objects'][ind_object] != 0:  # manage exceptions
            if Words[type]['exceptions']['objects'][ind_object] in Words[type]['determinants']['masc']:
                Words[type]['determinants']['counter'][Words[type]['determinants']['masc'].index(Words[type]['exceptions']['objects'][ind_object])] += 1
            else:
                Words[type]['determinants']['counter'][Words[type]['determinants']['femi'].index(Words[type]['exceptions']['objects'][ind_object])] += 1
            det2 = Words[type]['exceptions']['objects'][ind_object] 
        else:
            ind_det2 = weighted_min_indice(Words[type]['determinants']['counter'])
            if Words[type]['objects']['sexe'][ind_object] == 'masc':
                if Words[type]['objects']['plurality'][ind_object] == 'sing':
                    det2 = Words[type]['determinants']['masc'][ind_det2]
                elif Words[type]['objects']['plurality'][ind_object] == 'plur':
                    det2 = Words[type]['determinants_plural']['masc'][ind_det2]
            else:
                if Words[type]['objects']['plurality'][ind_object] == 'sing':
                    det2 = Words[type]['determinants']['femi'][ind_det2]
                elif Words[type]['objects']['plurality'][ind_object] == 'plur':
                    det2 = Words[type]['determinants_plural']['femi'][ind_det2]
            Words[type]['determinants']['counter'][ind_det2] += 1
            det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure)
        if count:
            Count(Counter, det2)
        add_info(info, 'det2', det2, ind_det2, type)
        return det2
    
def get_prepo(Words, type, structure, count=True, anomaly=False):
    global object, subject, ind_prep, Counter, info
    if structure == 1: # if structure == 1 the prepo is relative to the subject
        try:
            ind_prep = weighted_min_indice(Words[type]['prepositions']['counter_' + subject])
        except:
            subject, ind_subject = get_subject(Words, type, count=False)
            ind_prep = weighted_min_indice(Words[type]['prepositions']['counter_' + subject])
        prepo = Words[type]['prepositions'][subject][ind_prep]
        try: # Check if the prepo and the object don't refer to the same proper name.
            if object.split()[1] == prepo.split()[1]:
                prepo = get_prepo(Words, type, structure, count=False)
        except:
            pass
        if count:
            Words[type]['prepositions']['counter_'+subject][ind_prep] += 1
            Count(Counter, prepo)
    elif structure == 2: #if structure = 2 the prepo is relative to the object
        if len(object.split()) >= 4: # exception for long objects 
            prepo = ''
        else:
            try:
                ind_prep = weighted_min_indice(Words[type]['prepositions']['counter_'+object])
            except:
                object, ind_object = get_object(Words, type, structure, count=False)
                print(type, object)
                ind_prep = weighted_min_indice(Words[type]['prepositions']['counter_'+object])
            prepo = Words[type]['prepositions'][object][ind_prep]
            if count:
                Words[type]['prepositions']['counter_'+object][ind_prep] += 1
                Count(Counter, prepo)
    else:  # if structure == 3 there is 2 prepo relative to the subject
        try:
            ind_prep1 = weighted_min_indice(Words[type]['prepositions2'][0]['counter_' + subject])
        except:
            subject, ind_subject = get_subject(Words, type, count=False)
            ind_prep1 = weighted_min_indice(Words[type]['prepositions2'][0]['counter_' + subject])
        prepo1 = Words[type]['prepositions2'][0][subject][ind_prep1]
        ind_prep2 = weighted_min_indice(Words[type]['prepositions2'][1]['counter_' + subject])
        prepo2 = Words[type]['prepositions2'][1][subject][ind_prep2]
        try: # Check if the 2 prepos don't refer to the same proper name.
            if prepo1.split()[1] == prepo2.split()[1]:
                prepo = get_prepo(Words, type, structure, count=False)
                prepo1 = ' '.join([prepo.split()[0], prepo.split()[1]])
                prepo2 = ' '.join([prepo.split()[2], prepo.split()[3]])
                ind_prep1 = Words[type]['prepositions2'][0][subject].index(prepo1)
                ind_prep2 = Words[type]['prepositions2'][1][subject].index(prepo2)
        except:
            pass
        if count:
            Words[type]['prepositions2'][0]['counter_'+subject][ind_prep1] += 1
            Words[type]['prepositions2'][1]['counter_'+subject][ind_prep2] += 1
        prepo = prepo1 + ' ' + prepo2
        ind_prep = [ind_prep1, ind_prep2]
        Count(Counter, prepo1)
        Count(Counter, prepo2)
    add_info(info, 'prepo', prepo, ind_prep, type, anomaly)
    return prepo

def match_det(Words, type, det, noun, sexe, SuborObj, ind, structure, count=True):
    global determinants, ind_det, ind_subject, ind_object, Counter
    if noun[0] in ['a', 'e', 'i', 'o', 'u']:
        if det == 'ce':
            det = 'cet'
        elif (det == 'le') or (det == 'la'):   # if we change "le" for "l'" we change the number of word -> choose another determinant
            ind_Det = ind_det
            if count:
                Counter['counter'][Counter['word'].index(det)] -= 1
            if SuborObj == 'subject':
                ind_subject = ind
                det = get_det(Words, type, structure, ind_subject, count)
            else:
                ind_object = ind
                det = get_det2(Words, type, structure, ind_object, count)
            if count:
                Words[type]['determinants']['counter'][ind_Det] -= 1
        else:
            pass
    else:               
        if det == 'cet':
            det = 'ce'
    return det

def construct_sentence(structure, det, subject, prepo, verb, det2, object):
    global info
    if structure == 1:
        sentence = det + ' '+ subject + ' ' + prepo + ' ' +  verb + ' ' + det2 + ' ' + object# + '.'
    elif structure == 2:
        sentence = det + ' ' + subject + ' ' + verb + ' ' + det2 + ' ' + object + ' ' + prepo# + '.'
    else:
        sentence = det + ' ' + subject + ' ' + prepo + ' ' + verb# + '.'
    # sentence = sentence[0].upper() + sentence[1::]
    sentence = ' '.join(sentence.split())
    return sentence
  
## ANOMALIES
            
def get_anomaly_position(structure, type, anomaly_position_counter):
    
    ind = weighted_min_indice(anomaly_position_counter[structure-1])
    # if structure == 1: 
    #     if type == 0 or type == 3: #all positions for types 0,3
    #         ind = weighted_min_indice(anomaly_position_counter[structure-1])
    #     else: # No position 6 for types 1,4,2,5
    #         ind = weighted_min_indice([anomaly_position_counter[structure-1][0], anomaly_position_counter[structure-1][2]])
    #         if ind == 1:
    #             ind += 1
    # if structure == 2: 
    #     if type == 0 or type == 3: # no position 6,8 for types 0,3
    #         ind = 0
    #     else: # No position 4 for types 1,4,2,5
    #         ind = weighted_min_indice(anomaly_position_counter[structure-1][1::]) 
    #         ind += 1
    #         
    # if structure == 3: 
    #     if type == 3: # all positions for type 3
    #         ind = weighted_min_indice(anomaly_position_counter[structure-1])
    #     else: # no position 8 for types 1,2,4,5
    #         ind = weighted_min_indice(anomaly_position_counter[structure-1][0:-1])
    #counter
    if ind == 0:
        anomaly_position = 3
    elif ind == 1:
        anomaly_position = 5
    elif ind == 2:
        anomaly_position = 7
    anomaly_position_counter[structure-1][ind] += 1
    return ind, anomaly_position, anomaly_position_counter
        
    
vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'é', 'è', 'ê']
consonants = ['q', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'c', 'v', 'b', 'n', 'm']
def word2string(word):
    letters = list(word)
    for ind_letter in range(len(letters)):
        letters[ind_letter] = random.choice(consonants)
    word = ''.join(letters)
    return word

def generate_string_anomaly(sentence, ind_pos, structure):
    splitted = sentence.split()
    if ind_pos == 0:
        splitted[3] = word2string(splitted[3])
        info[-1]['anomaly_position'] = 3
        info[-1]['string_anomaly'] = splitted[3]
    elif ind_pos == 1:
        splitted[5] = word2string(splitted[5])
        info[-1]['anomaly_position'] = 5
        info[-1]['string_anomaly'] = splitted[5]
    elif ind_pos == 2:
        splitted[7] = word2string(splitted[7])
        info[-1]['anomaly_position'] = 7
        info[-1]['string_anomaly'] = splitted[7]
    else:
        print('Pb anomaly position (from generate_string_anomaly)')
    sentence = ' '.join(splitted)
    return sentence

def generate_syntaxic_anomaly(Words, old_type, structure, det, subject, prepo, verb, det2, object, ind_pos, ind_subject):
    #Randomly select a new type from which to select a new word with a different syntaxic role (nouns <-> verbs). 
    global info_syntac_anomaly , sentence
    if old_type == 0 or old_type == 3:
        types = [2,5]
    elif old_type == 1 or old_type ==4:
        types = [2,5]
    elif old_type == 2 or old_type == 5:
        types = [0,1,4]
    type = random.choice(types) # We select a random type to choose the new word
    ind_subject = random.choice([i for i in range(len(Words[type]['subjects']['word']))])
    if structure == 1:
        if ind_pos == 0: #change on the subj_prepo
            splitted = prepo.split()
            splitted[1] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
            prepo = ' '.join(splitted)   
        elif ind_pos == 1: #change on the verb
            splitted = verb.split()
            splitted[1], ind_object = get_object(Words, type, structure, count=False, anomaly='syntaxic')
            verb = ' '.join(splitted)
        elif ind_pos == 2:#change on the object
            if len(object.split()) > 1:
                splitted = object.split()
                splitted[1] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
                object = ' '.join(splitted)
            else:
                object = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
            
    elif structure == 2:
        if ind_pos == 0: #change on the verb
            splitted = verb.split()
            splitted[1], ind_object = get_object(Words, type, structure, count=False, anomaly='syntaxic')
            verb = ' '.join(splitted)
        elif ind_pos == 1: #change on the object
            if len(object.split()) > 1:
                splitted = object.split()
                splitted[1] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
                object = ' '.join(splitted)
            else:
                object = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')#.split()[1]
        elif ind_pos == 2: #Change on the obj_prepo
            splitted = prepo.split()
            splitted[1] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
            prepo = ' '.join(splitted) 
    elif structure == 3:
        if ind_pos == 0: #Change on the 1st prepo
            splitted = prepo.split()
            splitted[1] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
            prepo = ' '.join(splitted)
        if ind_pos == 1: #Change on the 2nd prepo
            splitted = prepo.split()
            splitted[3] = get_verb(Words, type, structure, ind_subject, count=False, anomaly='syntaxic')
            prepo = ' '.join(splitted)
        if ind_pos == 2: #Change on the verb
            splitted = verb.split()
            splitted[1], ind_object = get_object(Words, type, structure, count=False, anomaly='syntaxic')
            verb = ' '.join(splitted)
    sentence = construct_sentence(structure, det, subject, prepo, verb, det2, object)
    return sentence
    
    
## Semantic anomaly

info_syntac_anomaly = []

def choose_subject_accordingly(old_type, old_ind_subject, type): # Accordingly -> the new subject has same sexe and plurality as the old. Also allow the  verb we take is accorded to the old subject (case of types 0 and 3 change of verb)
    if Words[old_type]['subjects']['plurality'][old_ind_subject] == 'sing':
        if Words[old_type]['subjects']['sexe'][old_ind_subject] == 'masc':
            ind_subject = random.choice(np.where(np.logical_and(np.array(Words[type]['subjects']['plurality']) == 'sing', np.array(Words[type]['subjects']['sexe']) == 'masc')==True)[0])
        else:
            ind_subject = random.choice(np.where(np.logical_and(np.array(Words[type]['subjects']['plurality']) == 'sing', np.array(Words[type]['subjects']['sexe']) == 'femi')==True)[0])
    else:
        if Words[old_type]['subjects']['sexe'][old_ind_subject] == 'masc':
            ind_subject = random.choice(np.where(np.logical_and(np.array(Words[type]['subjects']['plurality']) == 'plur', np.array(Words[type]['subjects']['sexe']) == 'masc')==True)[0])
        else:
            ind_subject = random.choice(np.where(np.logical_and(np.array(Words[type]['subjects']['plurality']) == 'plur', np.array(Words[type]['subjects']['sexe']) == 'femi')==True)[0])
    subject = Words[type]['subjects']['word'][ind_subject]
    return subject, ind_subject
    
def choose_object_accordingly(old_type, old_ind_object, type): # Accordingly -> the new object has same sexe and plurality as the old. 
    if old_ind_object == None:
        old_ind_object = weighted_min_indice(Words[old_type]['objects']['counter'])
    if Words[old_type]['objects']['plurality'][old_ind_object] == 'sing':
        if Words[old_type]['objects']['sexe'][old_ind_object] == 'masc':
            ind_object = random.choice(np.where(np.logical_and(np.array(Words[type]['objects']['plurality']) == 'sing', np.array(Words[type]['objects']['sexe']) == 'masc')==True)[0])
        else:
            ind_object = random.choice(np.where(np.logical_and(np.array(Words[type]['objects']['plurality']) == 'sing', np.array(Words[type]['objects']['sexe']) == 'femi')==True)[0])
    else:
        if Words[old_type]['objects']['sexe'][old_ind_object] == 'masc':
            ind_object = random.choice(np.where(np.logical_and(np.array(Words[type]['objects']['plurality']) == 'plur', np.array(Words[type]['objects']['sexe']) == 'masc')==True)[0])
        else:
            ind_object = random.choice(np.where(np.logical_and(np.array(Words[type]['objects']['plurality']) == 'plur', np.array(Words[type]['objects']['sexe']) == 'femi')==True)[0])
    object = Words[type]['objects']['word'][ind_object]
    return object, ind_object

##
def generate_semantic_anomaly(Words, old_type, structure, det, subject, old_ind_subject, prepo, verb, det2, object, old_ind_object, ind_pos):
    global sentence, ind_object, ind_subject
    
    # Types 0 and 3
    if old_type == 0 or old_type == 3: 
        
        if structure == 1:
            
            if ind_pos == 0: #Change on the subj_prepo <- object from inanimate_anomalies
                obj = inanimate_anomalies['word'][weighted_min_indice(inanimate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
            elif ind_pos == 1: #Change the verb <- verb from 2 or 5
                type = random.choice([2,5])
                sub, ind_subject = choose_subject_accordingly(old_type, old_ind_subject, type)
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic')
            elif ind_pos == 2: #change on the object <- object from 2
                type = random.choice([2])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
                
        elif structure == 2:
            if ind_pos == 0: #Change the verb <- verb from 2 or 5
                type = random.choice([2,5])
                sub, ind_subject = choose_subject_accordingly(old_type, old_ind_subject, type)
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic')
            elif ind_pos == 1: #change on the object <- object from 2
                type = random.choice([2])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
            elif ind_pos == 2: #Change on the obj_prepo <- object from animate_anomalies
                obj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
                
        elif structure == 3:
            if ind_pos == 0: 
                if old_type == 0:# Change on the 1st prepo <- objects from inanimate_anomalies
                    obj = inanimate_anomalies['word'][weighted_min_indice(inanimate_anomalies['counter'])]
                    splitted = prepo.split()
                    splitted[1] = obj
                    prepo = ' '.join(splitted)
                elif old_type == 3: # Change on the 1st prepo <- objects from 1,4
                    type = random.choice([1,4])
                    obj, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                    splitted = prepo.split()
                    splitted[1] = obj
                    prepo = ' '.join(splitted)
            elif ind_pos == 1: #Change the 2nd subj_prepo <- object from animate_anomalies
                obj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[3] = obj
                prepo = ' '.join(splitted)
            elif ind_pos == 2: #Change the verb <- verb from 2 or 5
                type = random.choice([2,5])
                sub, ind_subject = choose_subject_accordingly(old_type, old_ind_subject, type)
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic')
    
    # Types 1 and 4
    elif old_type == 1 or old_type == 4:
        
        if structure == 1:
            
            if ind_pos == 0: #Change on the subj_prepo <- object from animate_anomalies
                obj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]                
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
            elif ind_pos == 1: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
            elif ind_pos == 2: #Change on the object <- object from 2
                type = random.choice([2])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
                
        elif structure == 2:
            if ind_pos == 0: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
            elif ind_pos == 1: #Change on the object <- object from 2 
                type = random.choice([2])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
            elif ind_pos == 2: #Change on the obj_prepo <- object from inanimate_anomalies
                obj = boissons_anomalies['word'][weighted_min_indice(boissons_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
                
        elif structure == 3:
            if ind_pos == 0:  #Change on the 1st subj_prepo <- object from animate_anomalies
                subj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = subj
                prepo = ' '.join(splitted)
            elif ind_pos == 1:#Change on the 2nd subj_prepo <- object from animate_anomalies
                subj = inanimate_anomalies['word'][weighted_min_indice(inanimate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[3] = subj
                prepo = ' '.join(splitted)
            elif ind_pos == 2: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
   
   # Types 2 and 5             
    elif old_type == 2 or old_type == 5:
        if structure == 1:
            if ind_pos == 0:#Change on the subj_prepo <- object from animate_anomalies
                obj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]                
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
            elif ind_pos == 1: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
            elif ind_pos == 2: #Change on the object <- object from from 1(type2) or 1,4 (type5)
                if old_type == 5:
                    type = random.choice([1,4])
                elif old_type == 2:
                    type = random.choice([1])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
                
        elif structure == 2:
            if ind_pos == 0: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
            elif ind_pos == 1: #Change on the object <- object from 1(type2) or 1,4 (type5)
                if old_type == 5:
                    type = random.choice([1,4])
                elif old_type == 2:
                    type = random.choice([1])
                object, ind_object = choose_object_accordingly(old_type, old_ind_object, type)
                det2 = match_det(Words, type, det2, object, Words[type]['objects']['sexe'][ind_object], 'object', ind_object, structure, count=False)
            elif ind_pos == 2: #Change on the obj_prepo <- object from lire_bricoler_anomalies
                obj = lire_bricoler_anomalies['word'][weighted_min_indice(lire_bricoler_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = obj
                prepo = ' '.join(splitted)
                
        elif structure == 3:
            if ind_pos == 0:  #Change on the 1st subj_prepo <- object from animate_anomalies
                subj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[1] = subj
                prepo = ' '.join(splitted)
            elif ind_pos == 1:#Change on the 2nd subj_prepo <- object from animate_anomalies
                subj = animate_anomalies['word'][weighted_min_indice(animate_anomalies['counter'])]
                splitted = prepo.split()
                splitted[3] = subj
                prepo = ' '.join(splitted)
            elif ind_pos == 2: # Change on the verb <- verb from anim_verb_anomalies (same type)
                type = old_type
                verb = get_verb(Words, type, structure, ind_subject, count=False, fixed_tense=True, anomaly='semantic', anom_anim=True)
                
    sentence = construct_sentence(structure, det, subject, prepo, verb, det2, object)
    return sentence
        
def check_Counter(sentences):        #check if Counter takes once and only once each word.
    for i in range(len(Counter['word'])):
        Counter['word'][i] = Counter['word'][i].split()
        if len(Counter['word'][i]) > 1:
            Counter['counter'][i] = Counter['counter'][i] * 2
    if sum(Counter['counter']) == len(sentences) * 8:
        print('ok')
    else:
        print('problem')
    return
    
    
def generate_statistics(sentences):
    len_word_position = [[] for i in range(8)]
    for sentence in sentences:
        for iword in range(len(sentence.split())):
            len_word_position[iword].append(len(sentence.split()[iword]))
    moy_word_position = []
    for i in range(8):
        moy_word_position.append(np.mean(len_word_position[i]))
        
## Jabberwocky and wordlist

def generate_jabberwocky_anomaly(sentence, ind_pos, word2jab, structure):
    splitted = sentence.split()    
    for i_word in [1,3,5,7]:
        splitted[i_word] = word2jab[splitted[i_word]]

    # info[-1]['anomaly_position'] = 'Jab'
    # info[-1]['jabberwocky_anomaly'] = splitted[real_pos]
    
    sentence = ' '.join(splitted)
    
    return sentence

def generate_wordlist():
    sentence_wordlist = ''
    for i_2_word in range(4):
        
        word1 = random.choice(list(all_even_words.keys()))
        while word1 in sentence_wordlist.split(): #no repetition
            word1 = random.choice(list(all_even_words.keys()))
            
        word2 = random.choice(list(all_odd_words.keys()))
        while any(param in all_odd_words[word2] for param in all_even_words[word1]) or word2 in sentence_wordlist.split(): # if the second word has a caracteristic (sexe, plurality, aux-verb), or if there is a repetition, we choose another second word.
            word2 = random.choice(list(all_odd_words.keys()))
        sentence_wordlist = sentence_wordlist + word1 + ' ' + word2 + ' '
    return sentence_wordlist