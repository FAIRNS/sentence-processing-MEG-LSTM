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
    ind_struct = 1 # weighted_min_indice(structures['counter'])
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




## Generate new NP - VP transitions, added the 14th of April 2018

def get_old_NP( sentence, sent_info):
    if sent_info['structure'] == 1:
        NP = sentence.split()[0:4]
    elif sent_info['structure'] == 2:
        NP = sentence.split()[0:2]
    elif sent_info['structure'] == 3:
        NP = sentence.split()[0:6]
    return NP

def get_NP_pronoun( sent_info ):
    if sent_info['subject_sexe'] == 'femi':
        pronoun = 'elle'
    elif sent_info['subject_sexe'] == 'masc':
        pronoun = 'il'
    else: 
        print("Error: unknown subject sexe\n")

    if sent_info['subject_plurality'] == 'plur':
        pronoun += 's'
    return [ pronoun ]  

def get_NP_proper_noun( sent_info ):
    from random import choice

    if sent_info['subject_sexe'] == 'masc':
        names = ['Jean', 'Pierre', 'Paul', 'Jean-Pierre', 'Jean-Paul']
    elif sent_info['subject_sexe'] == 'femi':
        names = ['Anne', 'Claire', 'Sophie', 'Anne-Claire', 'Anne-Sophie']

    if sent_info['subject_plurality'] == 'plur':
        pro1 = choice( names )
        pro2 = choice( names )
        while pro2 in pro1 or pro1 in pro2:
            pro2 = choice( names )
        proper_noun = [ pro1, 'et', pro2 ]
    elif sent_info['subject_plurality'] == 'sing':
        proper_noun = [ choice( names ) ]
    else:   
        print("Error: unknown subject plurality\n")
    return proper_noun

def get_NP_adj( old_NP, sent_info ):
    from random import choice
    if len(old_NP) == 2: # adjective should qualify the subject, so we need to add the right terminaison
        adj = choice( ['malade', 'aimable', 'nerveux', 'timide' ] )
        if sent_info['subject_sexe'] == 'femi' and adj[-1] != 'e' and adj[-1] != 'x':
            adj += 'e'
        elif sent_info['subject_sexe'] == 'femi' and adj == 'nerveux':
            adj = 'nerveuse'
        if sent_info['subject_plurality'] == 'plur' and adj[-1] != 's' and adj[-1] != 'x':
            adj += 's'
    elif len( old_NP ) == 4: # adjective qualifies the first complement
        adj = choice( ['français', 'anglais', 'aimable', 'timide' ] )

    elif len( old_NP ) == 6: # adjective qualifies the second complement
        adj = choice( [ 'moderne', 'minuscule', 'accueillant', 'crasseux' ] )
    else:
        print("Error: unknown NP length\n")
    return old_NP + [ adj ]

def get_NP_prepo( ):
    from random import choice
    if choice([0,1]): # femi or masc object
        begin_prepo = choice( [['près', 'de'], ['à', 'droite', 'de'], ['à', 'gauche', 'de'], ['devant'] ] )
        end_prepo = choice( [['la', 'fenêtre'], ['la', 'porte'], ['la', 'table']] )
    else:
        begin_prepo = choice( [['près', 'du'], ['à', 'droite', 'du'], ['à', 'gauche', 'du'], ['devant', 'le']] )
        end_prepo = choice( [['bureau'], ['portail'], ['fauteuil']] )
    return begin_prepo + end_prepo

def vary_NP( old_NP, NP_end, sent_info ):
    if NP_end == 'noun': # then do nothing we already have the good ending
        new_NP = old_NP
    elif NP_end == 'adj': # add an adjective to the end of the NP
        new_NP = get_NP_adj( old_NP, sent_info )
    elif NP_end == 'pronoun': # Replace the NP by a pronoun
        new_NP = get_NP_pronoun( sent_info )
    elif NP_end == 'proper_noun':
        new_NP = get_NP_proper_noun( sent_info )
    elif NP_end == 'prepo_noun':
        new_NP = old_NP + get_NP_prepo( )
    return new_NP

def get_old_VP( sentence, sent_info):
    if sent_info['structure'] == 1:
        VP = sentence.split()[4::]
    elif sent_info['structure'] == 2:
        VP = sentence.split()[2::]
    elif sent_info['structure'] == 3:
        VP = sentence.split()[6::]
    return VP

def get_VP_verb( old_VP ):
    if ' '.join( old_VP[0:2] ) == 'ont mangé':
        new_VP = [ 'préparèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'ont dévoré':
        new_VP = [ 'refusèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont manger':
        new_VP = [ 'mangent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont dévorer':
        new_VP = [ 'dévorent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a mangé':
        new_VP = [ 'mangea' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a dévoré':
        new_VP = [ 'refusa' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va manger':
        new_VP = [ 'mange' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va dévorer':
        new_VP = [ 'dévore' ] + old_VP[2::]

    elif ' '.join( old_VP[0:2] ) == 'ont réparé':
        new_VP = [ 'portèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'ont bricolé':
        new_VP = [ 'jetèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont réparer':
        new_VP = [ 'réparent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont bricoler':
        new_VP = [ 'jettent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a réparé':
        new_VP = [ 'porta' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a bricolé':
        new_VP = [ 'jeta' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va réparer':
        new_VP = [ 'répare' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va bricoler':
        new_VP = [ 'bricole' ] + old_VP[2::]

    elif ' '.join( old_VP[0:2] ) == 'ont bu':
        new_VP = [ 'burent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'ont avalé':
        new_VP = [ 'avalèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont boire':
        new_VP = [ 'boivent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont avaler':
        new_VP = [ 'avalent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a bu':
        new_VP = [ 'but' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a avalé':
        new_VP = [ 'avala' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va boire':
        new_VP = [ 'boit' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va avaler':
        new_VP = [ 'avale' ] + old_VP[2::]

    elif ' '.join( old_VP[0:2] ) == 'ont lu':
        new_VP = [ 'jetèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'ont consulté':
        new_VP = [ 'cherchèrent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont lire':
        new_VP = [ 'lisent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'vont consulter':
        new_VP = [ 'consultent' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a lu':
        new_VP = [ 'lut' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'a consulté':
        new_VP = [ 'consulta' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va lire':
        new_VP = [ 'lit' ] + old_VP[2::]
    elif ' '.join( old_VP[0:2] ) == 'va consulter':
        new_VP = [ 'consulte' ] + old_VP[2::]

    else:
        print( "Error, unknown old VP: %s \n", old_VP)

    info[-1]['VP_PoS'] = [ 'verb' ] + [ 'verbPreposition' for i in range(len(old_VP[2::])) ]
    return new_VP

def get_VP_pronoun( old_VP, sent_info ):
    from random import choice
    old_VP = get_VP_verb( old_VP ) # change to présent and passé simple to get better results with pronouns
    new_VP = [ choice( ['le', 'la', 'les'] ) ] + old_VP
    # now we need to remove the complements after the verb
    if sent_info['structure'] == 1:
        new_VP = new_VP[0:-2]
    elif sent_info['structure'] == 2:
        new_VP = new_VP[0:-4]
    elif sent_info['structure'] == 3:
        pass
    sent_info['VP_PoS'] = [ 'pronoun', 'verb' ]
    return new_VP

def get_VP_negation( old_VP, sent_info ):
    from random import choice
    if sent_info['tense'] == 'past': 
        # We need to remove the complements after the verb
        if sent_info['structure'] == 1:
            old_VP = old_VP[0:-2]
        elif sent_info['structure'] == 2:
            old_VP = old_VP[0:-4]
        elif sent_info['structure'] == 3:
            pass
        old_VP = get_VP_verb( old_VP ) # change to passé simple to avoid having "n'" as the negation
        new_VP = [ 'ne' ] + old_VP + [ 'pas' ]
    elif sent_info['tense'] == 'future':
        new_VP = [ 'ne' ] + [ old_VP[0] ] + [ 'pas' ] + old_VP[1::]
    else:
        print( "Error, unknown tense\n" )
    sent_info['VP_PoS'] = [ 'neg', 'verb', 'pas' ] + [ 'verbPreposition' for i in range(len(old_VP[2::])) ]
    return new_VP

def vary_VP( old_VP, VP_end, sent_info ):
    if VP_end == 'aux': # then do nothing we already have the good ending
        new_VP = old_VP
        sent_info['VP_PoS'] = [ 'aux', 'verb' ] + [ 'verbPreposition' for i in range(len(old_VP[2::])) ]
    elif VP_end == 'verb': # change to a verb with no auxiliary
        new_VP = get_VP_verb( old_VP )
    elif VP_end == 'pronoun': # add a pronoun to the VP
        new_VP = get_VP_pronoun( old_VP, sent_info )
    elif VP_end == 'negation':
        new_VP = get_VP_negation( old_VP, sent_info )
    return new_VP

def  generate_NP_VP_transition_variation( sentence, NP_end_counter, VP_begin_counter ):
    global info
    # change the end of the NP
    NP_end_types = ['noun', 'adj', 'prepo_noun']#, 'pronoun', 'proper_noun'] # here we want only relative clause sentences
    new_NP_end_type = NP_end_types[ weighted_min_indice( NP_end_counter ) ]
    NP_end_counter[ NP_end_types.index(new_NP_end_type) ] += 1
    old_NP = get_old_NP( sentence, info[-1] )
    new_NP = vary_NP( old_NP, new_NP_end_type, info[-1] )
    info[-1]['NP_ends_with'] = new_NP_end_type
    info[-1]['NP_length'] = len( new_NP )

    # change the beginning of the VP
    VP_begin_types = ['aux', 'verb', 'pronoun', 'negation']
    new_VP_begin_type = VP_begin_types[ weighted_min_indice( VP_begin_counter ) ]
    VP_begin_counter[ VP_begin_types.index(new_VP_begin_type) ] += 1
    old_VP = get_old_VP( sentence, info[-1] )
    new_VP = vary_VP( old_VP, new_VP_begin_type, info[-1] )
    info[-1]['VP_begins_with'] = new_VP_begin_type
    info[-1]['VP_length'] = len( new_VP )

    new_sentence = ' '.join( new_NP + new_VP )

    return new_sentence


## Incorporate relative clauses, added the 26th of May 2018 -- modified the 5th of Jun 2018 -- modified 8th of October 2018

def get_relative_clause_qui( sentence, sent_info ):
    que_variations = ['aux', 'vb'] # 'neg'
    var = np.random.choice( que_variations )

    # get the object inside the relative close
    proper_names = ['Jean', 'Pierre', 'Paul', 'Claire', 'Sophie', 'Cécile']
    proper_names_sex = ['masc', 'masc', 'masc', 'femi', 'femi', 'femi']
    names = ['coiffeur', 'boulanger', 'plombier', 'coiffeuse', 'boulangère', 'plombière']
    names_sex = ['masc', 'masc', 'masc', 'femi', 'femi', 'femi']
    
    if np.random.choice([True, False]): # proper or regular noun
        name1 = np.random.choice( proper_names )
        while name1 in sentence:
            name1 = np.random.choice( proper_names ) # get a proper name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
        if np.random.choice([True, False]):     # one or two proper names
            name2 = np.random.choice( proper_names )
            while (name2 in sentence) or (name1 == name2) or proper_names_sex[proper_names.index(name2)] != proper_names_sex[proper_names.index(name1)]:
                name2 = np.random.choice( proper_names ) # get a proper name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
            obj = name1 + ' et ' + name2
            sent_info['relative_clause'] += "_properPlur"
            PoSN = [ 'relativeNoun', 'relativeNounJoiner', 'relativeNoun2' ]
            sent_info['relative_subject_plurality'] = 'plur'
            sent_info['relative_subject_sexe'] = 'masc' if ('masc' in [proper_names_sex[proper_names.index(name1)], proper_names_sex[proper_names.index(name2)]] ) else 'femi'
            
            if proper_names_sex[proper_names.index(name1)] != proper_names_sex[proper_names.index(name2)]: raise Error
            
        else:
            obj = name1
            sent_info['relative_clause'] += "_properSing"
            PoSN = [ 'relativeNoun' ]
            sent_info['relative_subject_plurality'] = 'sing'
            sent_info['relative_subject_sexe'] = proper_names_sex[ proper_names.index(name1) ]
    else: #regular noun
        name = np.random.choice( names )
        while name in sentence:
            name = np.random.choice( names ) # get a common name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
        if np.random.choice( [True, False] ):
            obj = 'les ' + name + 's'
            sent_info['relative_clause'] += "_commonPlur"
            PoSN = [ 'relativeDet', 'relativeNoun']
            sent_info['relative_subject_plurality'] = 'plur'
            sent_info['relative_subject_sexe'] = names_sex[names.index(name)]
        else:
            det = 'le ' if names_sex[names.index(name)] == 'masc' else 'la '
            obj = det + name
            sent_info['relative_clause'] += "_commonSing"
            PoSN = [ 'relativeDet', 'relativeNoun']
            sent_info['relative_subject_plurality'] = 'sing'
            sent_info['relative_subject_sexe'] = names_sex[names.index(name)]

    verbs = ['chercher', 'juger', 'croiser', 'rencontrer', 'former', 'laisser', 'convoiter', 'mener']  # connaitre , 
    verb = np.random.choice( verbs )

    verb_pp = (verb[0:-2]+'é')

    if var == 'aux':
        tense = np.random.choice( ['past', 'future'] )
        if tense == 'future':
            if sent_info['subject_plurality'] == 'sing':
                relative_clause = ['va', verb]
            elif sent_info['subject_plurality'] == 'plur':
                relative_clause = ['vont', verb]
            else:
                print( "error code qui aux" )
        elif tense == 'past':
            if sent_info['subject_plurality'] == 'sing':
                relative_clause = ['a', verb_pp]
            elif sent_info['subject_plurality'] == 'plur':
                relative_clause = ['ont', verb_pp]
            else:
                print( "error code qui aux" )
        sent_info['relative_clause'] += '_aux'
        PoSV = [ 'relativeAux', 'relativeVerb']

    elif var == 'vb':
        tense = np.random.choice( ['past', 'present'] )
        if tense == 'present':
            if sent_info['subject_plurality'] == 'sing':
                conj_vb = verb[0:-1]
            else: 
                conj_vb = verb[0:-1] + 'nt'
        else:
            if sent_info['subject_plurality'] == 'sing':
                conj_vb = (verb[0:-2] + 'a') if (verb != 'juger') else (verb[0:-1] + 'a')
            else: 
                conj_vb = verb[0:-2] + 'èrent'
        relative_clause = [conj_vb]
        sent_info['relative_clause'] += '_vb'
        PoSV = [ 'relativeVerb']

    # elif var == 'neg':
    #     if sent_info['subject_plurality'] == 'sing':
    #         conj_vb = verb[0:-1]
    #     else:
    #         conj_vb = verb[0:-1] + 'nt'
    #     neg = 'ne' #"n'" if verb[0] in ['a', 'e'] else "ne" # on ne veut pas de liaison
    #     relative_clause = [neg, conj_vb, 'pas']
    #     sent_info['relative_clause'] += '_neg'

    relative_clause = ['qui'] + relative_clause + [obj]

    sent_info['PoS'] += PoSV + PoSN
    sent_info['relative_clause_ends_with'] = 'noun'

    sent_info['relative_clause_length'] = len( (' '.join(relative_clause)).split() )

    return relative_clause    


def get_relative_clause_que( sentence, sent_info ):
    proper_names = ['Jean', 'Pierre', 'Paul', 'Claire', 'Sophie', 'Cécile']
    proper_names_sex = ['masc', 'masc', 'masc', 'femi', 'femi', 'femi']
    names = ['coiffeur', 'boulanger', 'plombier', 'coiffeuse', 'boulangère', 'plombière']
    names_sex = ['masc', 'masc', 'masc', 'femi', 'femi', 'femi']

    que_variations_np = ['proper', 'noun']
    que_variations_vp = ['aux', 'vb']
    vp = np.random.choice( que_variations_vp )
    NP = np.random.choice( que_variations_np )

    if NP == 'proper':
        name1 = np.random.choice( proper_names )
        while name1 in sentence:
            name1 = np.random.choice( proper_names ) # get a proper name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
        if np.random.choice([True, False]):     # one or two proper names
            name2 = np.random.choice( proper_names )
            while (name2 in sentence) or (name1 == name2) or (proper_names_sex[proper_names.index(name2)] != proper_names_sex[proper_names.index(name1)]):
                name2 = np.random.choice( proper_names ) # get a proper name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
            NP_plurality = 'plur'
            NAME = [name1 + ' et ' + name2]
            sent_info['relative_clause'] += "_properPlur"
            PoSN = [ 'relativeNoun', 'relativeNounJoiner', 'relativeNoun2' ]
            sent_info['relative_subject_plurality'] = 'plur'
            sent_info['relative_subject_sexe'] = 'masc' if ('masc' in [proper_names_sex[proper_names.index(name1)], proper_names_sex[proper_names.index(name2)]] ) else 'femi'
        else:
            NP_plurality = 'sing'
            NAME = [name1]
            sent_info['relative_clause'] += "_properSing"
            PoSN = [ 'relativeNoun' ]
            sent_info['relative_subject_plurality'] = 'sing'
            sent_info['relative_subject_sexe'] = proper_names_sex[ proper_names.index(name1) ]
    else: #regular noun
        name = np.random.choice( names )
        while name in sentence:
            name = np.random.choice( names ) # get a common name that is not in the sentence, and do it right at the begining in order not to screw up the sampling
        if np.random.choice( [True, False] ):
            NP_plurality = 'plur'
            NAME = ['les ' + name + 's']
            sent_info['relative_clause'] += "_commonPlur"
            PoSN = [' relativeDet', 'relativeNoun' ]
            sent_info['relative_subject_plurality'] = 'plur'
            sent_info['relative_subject_sexe'] = names_sex[names.index(name)]
        else:
            NP_plurality = 'sing'
            det = 'le ' if names_sex[names.index(name)] == 'masc' else 'la '
            NAME = [det + name]
            sent_info['relative_clause'] += "_commonSing"
            PoSN = [' relativeDet', 'relativeNoun' ]
            sent_info['relative_subject_plurality'] = 'sing'
            sent_info['relative_subject_sexe'] = names_sex[names.index(name)]

    verbs = ['chercher', 'juger', 'croiser', 'rencontrer', 'former', 'laisser', 'libérer', 'mener']  # aborder , 
    verb = np.random.choice( verbs )

    verb_pp = (verb[0:-2]+'é')

    if vp == 'aux':
        tense = np.random.choice( ['past', 'future'] )
        if tense == 'future':
            if NP_plurality == 'sing':
                VERB = ['va', verb]
            elif NP_plurality == 'plur':
                VERB = ['vont', verb]
            else:
                print( "error code qui aux" )
        elif tense == 'past':
            if NP_plurality == 'sing':
                VERB = ['a', verb_pp]
            elif NP_plurality == 'plur':
                VERB = ['ont', verb_pp]
            else:
                print( "error code qui aux" )
        sent_info['relative_clause'] += '_aux'
        PoSV = [' relativeAux', 'relativeVerb' ]

    elif vp == 'vb':
        tense = np.random.choice( ['past', 'present'] )
        if tense == 'present':
            if NP_plurality == 'sing':
                conj_vb = verb[0:-1]
            else: 
                conj_vb = verb[0:-1] + 'nt'
        else:
            if NP_plurality == 'sing':
                conj_vb = (verb[0:-2] + 'a') if (verb != 'juger') else (verb[0:-1] + 'a')
            else: 
                conj_vb = verb[0:-2] + 'èrent'
        VERB = [conj_vb]
        sent_info['relative_clause'] += '_vb'
        PoSV = [' relativeVerb' ]

    # elif vp == 'neg':
    #     conj_vb = np.random.choice( ['connait', 'connu'] )
    #     VERB = ['ne', conj_vb, 'pas']
    #     ending = ''
    #     sent_info['relative_clause'] += '_neg'

    if np.random.choice( [True, False] ): # whether to reverse np and vp
        relative_clause = ['que'] + VERB + NAME 
        sent_info['relative_clause'] += '_rev'
        sent_info['PoS'] += PoSV + PoSN 
        sent_info['relative_clause_ends_with'] = 'noun'
    else:
        relative_clause = ['que'] + NAME + VERB 
        sent_info['PoS'] += PoSN + PoSV
        sent_info['relative_clause_ends_with'] = 'verb'

    # make elisions
    relative_clause = ' '.join( ' '.join(relative_clause).split() ) # make a full string and remove spaces
    if 'que a' in relative_clause:
        relative_clause = relative_clause.replace( "que a", "qu'a")
    if 'que ont' in relative_clause:
        relative_clause = relative_clause.replace( "que ont", "qu'ont")
    if 'que A' in relative_clause:
        relative_clause = relative_clause.replace( "que A", "qu'A")
    relative_clause = relative_clause.split() # back to list

    sent_info['relative_clause_length'] = len( (' '.join(relative_clause)).split() )

    if "'" in ' '.join(relative_clause): # if we have a ', then we count the 2 element as separate words.
        sent_info['relative_clause_length'] += 1

    return relative_clause    

def generate_relative_clauses( old_sentence, counter ):

    add_PoS_to_info_start( info[-1] )

    rel_clause = ['que', 'qui'][ weighted_min_indice( counter )]
    if rel_clause == 'qui':
        info[-1]['relative_clause'] = 'qui'
        info[-1]['PoS'].append('qui')
        relative_clause = get_relative_clause_qui( old_sentence, info[-1] )
    else:
        info[-1]['relative_clause'] = 'que'
        info[-1]['PoS'].append('que')
        relative_clause = get_relative_clause_que( old_sentence, info[-1] )

    # info[-1]['NP_ends_with'] = info[-1]['PoS']

    add_PoS_to_info_end( info[-1] )

    new_sentence = old_sentence.split()[0:info[-1]['NP_length']] + relative_clause + old_sentence.split()[info[-1]['NP_length']::]
    new_sentence = ' '.join( new_sentence )
    return new_sentence

def add_PoS_to_info_start( info ):
    info['PoS'] = ['Det', 'Noun']
    if info['NP_length'] == 3: ## NOTE TODO: if added to version that use all structures, we need to take that into account here
        info['PoS'].append( 'Adj' )
    elif info['NP_length'] > 3:
        for i_prep in range(info['NP_length'] -2 -1): info['PoS'].append('subject_prepo')
        info['PoS'].append('subject_prepo_noun')
    return 

def add_PoS_to_info_end( info ):
    info['PoS'] += info['VP_PoS']
    del info['VP_PoS']
    return 

# def generate_one_adverb(old_sentence):


## ADD ADVERB STRUCTURES
def generate_adverb_structure( old_sentence, counter ):

    add_PoS_to_info_start( info[-1] )

    adverbs = ['souvent', 'correctement', 'totalement', 'parfaitement', 'délicatement', 'rapidement']

    struct = ['one', 'two'][weighted_min_indice(counter)]
    if struct == 'one': 
        adv = [np.random.choice(adverbs)]
        adv_PoS = ['adverb']
    elif struct == 'two':
        adv = [np.random.choice(adverbs), 'et', np.random.choice(adverbs)]
        while (adv[-1] == adv[0]): adv[-1] = np.random.choice(adverbs)
        adv_PoS = ['adverb', 'et', 'adverb']

    # check for the presence of auxiliary as this will decide whether the adverb(s) is before or after the verb
    aux_present = 'aux' in info[-1]['VP_PoS']

    if aux_present: # put the adverb(s) between aux and verb , except if there is a negation, then between 'pas' and the verb
        if 'pas'in info[-1]['VP_PoS']:
            new_sentence = old_sentence.split()[ 0:(info[-1]['NP_length'] + info[-1]['VP_PoS'].index('pas')) + 1 ] + adv + old_sentence.split()[ (info[-1]['NP_length'] + info[-1]['VP_PoS'].index('pas')) + 1 ::]
            info[-1]['VP_PoS'] = info[-1]['VP_PoS'][ 0:info[-1]['VP_PoS'].index('pas') + 1 ] + adv_PoS + info[-1]['VP_PoS'][ info[-1]['VP_PoS'].index('pas') + 1 :: ]
        else:
            new_sentence = old_sentence.split()[ 0:(info[-1]['NP_length'] + info[-1]['VP_PoS'].index('aux')) + 1 ] + adv + old_sentence.split()[ (info[-1]['NP_length'] + info[-1]['VP_PoS'].index('aux')) + 1 ::]
            info[-1]['VP_PoS'] = info[-1]['VP_PoS'][ 0:info[-1]['VP_PoS'].index('aux') + 1 ] + adv_PoS + info[-1]['VP_PoS'][ info[-1]['VP_PoS'].index('aux') + 1 :: ]
    else: # no auxiliary, adverb(s) after the verb, or after 'pas' if there is a negation
        if 'pas'in info[-1]['VP_PoS']:
            new_sentence = old_sentence.split()[ 0:(info[-1]['NP_length'] + info[-1]['VP_PoS'].index('pas')) + 1 ] + adv + old_sentence.split()[ (info[-1]['NP_length'] + info[-1]['VP_PoS'].index('pas')) + 1 ::]
            info[-1]['VP_PoS'] = info[-1]['VP_PoS'][ 0:info[-1]['VP_PoS'].index('pas') + 1 ] + adv_PoS + info[-1]['VP_PoS'][ info[-1]['VP_PoS'].index('pas') + 1 :: ]
        else:
            new_sentence = old_sentence.split()[ 0:(info[-1]['NP_length'] + info[-1]['VP_PoS'].index('verb')) + 1 ] + adv + old_sentence.split()[ (info[-1]['NP_length'] + info[-1]['VP_PoS'].index('verb')) + 1 ::]
            info[-1]['VP_PoS'] = info[-1]['VP_PoS'][ 0:info[-1]['VP_PoS'].index('verb') + 1 ] + adv_PoS + info[-1]['VP_PoS'][ info[-1]['VP_PoS'].index('verb') + 1 :: ]
    
    info[-1]['VP_length'] += len(adv)
    add_PoS_to_info_end( info[-1] )
    new_sentence = ' '.join( new_sentence )
    return new_sentence

## master structure -> choose structure and call relevant function

def master_structure( old_sentence, struct_counter, rel_clause_counter, adverb_struct_counter ):
	struct = ['unchanged', 'rel_clause', 'adverb'][weighted_min_indice(struct_counter)]
	struct_counter[struct.index(struct)] += 1

	if struct == 'unchanged':
		add_PoS_to_info_start( info[-1] )
		add_PoS_to_info_end( info[-1] )
		return old_sentence
	elif struct == 'rel_clause':
		return generate_relative_clauses( old_sentence, rel_clause_counter )
	elif struct == 'adverb':
		return generate_adverb_structure( old_sentence, adverb_struct_counter )
	else:
		print("Error -- unknown structure \n"); raise Error 

