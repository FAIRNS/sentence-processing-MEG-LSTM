info = [] # info will contain all information about every new word in every sentence

Words = []

determinants = {}
determinants['masc'] = ['un', 'le', 'ce']
determinants['femi'] = ['une', 'la', 'cette']
determinants['counter'] = [0,0,0]

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les', 'ces']
determinants_plural['femi'] = ['des', 'les', 'ces']
determinants_plural['counter'] = [0,0,0]

structures = {}
structures['structure'] = [1,2,3]#['X', 'prepo', 'V', 'Y']], ['X', 'V', 'Y', 'prepo'], ['X', 'prepo', 'Y', 'V']
structures['counter'] = [0,0,0]


def make_counter(dic, name=None):
    if name==None:
        dic['counter'] = [0 for i in range(len(dic['word']))]
    else:
        dic['counter_'+name] = [0 for i in range(len(dic[name]))]
    return 


## GENERAL : 

Inanim_subject = ['fruits', 'pommes', 'citrons', 'poires', 'raisins', 'figues', 'cerises', 'pruneaux', 'noix']
Inanim_subject_sexe = ['masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'femi', 'masc', 'femi']
Inanim_subject_plurality = ['plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']

Inanim_object = ['fruit', 'pomme', 'citron', 'poire', 'figue', 'cerise', 'pruneau', 'fruits', 'pommes', 'citrons', 'poires', 'raisins', 'figues', 'cerises', 'pruneaux'] #orange, noix
Inanim_object_sexe = ['masc', 'femi', 'masc', 'femi', 'femi', 'femi', 'masc', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'femi', 'masc']
Inanim_object_plurality = ['sing', 'sing' , 'sing' , 'sing', 'sing' , 'sing', 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']


Anim =  ['collègue', 'frère', 'soeur', 'voisin', 'voisine', 'ami', 'amie', 'oncle', 'tante', 'cousin', 'cousine', 'collègues', 'frères', 'soeurs', 'amis', 'amies', 'oncles', 'tantes', 'cousins', 'cousines', 'voisins', 'voisines'] # frère soeur père mère collègue?
Anim_sexe = ['masc', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi']
Anim_plurality = ['sing' , 'sing', 'sing' , 'sing' , 'sing', 'sing' , 'sing', 'sing', 'sing', 'sing', 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']


prepo_anim = ['du coiffeur', 'du médecin', 'du boulanger', 'du libraire', 'du dentiste', 'du facteur', 'du plombier', 'du curé'] 
prepo2_0anim = ['du coiffeur', 'du médecin', 'du boulanger', 'du libraire', 'du dentiste', 'du facteur', 'du plombier', 'du curé'] 
prepo2_1anim = ['du village', 'du patelin', 'du quartier', 'du coin']

prepo_fruits= ['du marché', 'du magasin', 'du commerce', 'du jardin', 'du verger']
prepo2_0fruits = ['du marché', 'du magasin', 'du verger']
prepo2_1fruits = ['du village', 'du patelin', 'du coin']

prepo2_1graines = prepo_fruits

prepo_obj_boire = ['du bar', 'du bistrot', 'du magasin']

animate_anomalies = {} #anomalies for animate words
animate_anomalies['word'] = ['vélo', 'pépin', 'sirop', 'soda', 'thé', 'meuble', 'scooter', 'fusil', 'fruit', 'citron', 'raisin', 'pruneau', 'volet', 'carnet', 'manuel', 'papier']
make_counter(animate_anomalies)

inanimate_anomalies = {}
inanimate_anomalies['word'] = ['vélo', 'thé', 'café', 'volet', 'fusil', 'scooter', 'soda']
make_counter(inanimate_anomalies)

boissons_anomalies = {}
boissons_anomalies['word'] = ['vélo', 'volet', 'fusil', 'scooter']
make_counter(boissons_anomalies)

lire_bricoler_anomalies = {}
lire_bricoler_anomalies['word'] = ['pépin', 'fruit', 'citron', 'raisin', 'pruneau', 'volet']
make_counter(lire_bricoler_anomalies) #for struct 2, ind_pos 7, types 2 & 5

anim_verbs_anomalies = {'tenses': ['past', 'future'], 'word': ['moisir', 'germer'], 'counter': [0, 0], 'future': {'sing': ['va moisir', 'va germer'], 'plur': ['vont moisir', 'vont germer']}, 'counter_tenses': [0, 0], 'past': {'sing': ['a moisi', 'a germé'], 'plur': ['ont moisi', 'ont germé']}} #pourrir ? "un oncle a pourri la carte du facteur...


## 0 INANIM 


subjects = {}
subjects['word'] = Inanim_subject
subjects['sexe'] = Inanim_subject_sexe
subjects['plurality'] = Inanim_subject_plurality
make_counter(subjects)

objects = {}        # Complement in place of an object
objects['word'] = Anim
objects['sexe'] = Anim_sexe
objects['plurality'] = Anim_plurality
make_counter(objects)
objects['except_struct'] = [0,0,0] # except for structure 2 : there is a complement relative to object
# objects['except_structure'] = {'word':['très vite', 'chez moi', 'chez toi', 'chez Michel', 'chez Jean', 'chez Suzanne', 'chez Marie'], 'sexe':['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'], 'plurality':['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']}
# make_counter(objects['except_structure'])

verbs = {}
verbs['word'] = ['nourrir', 'rassasier'] # alimenter?
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a nourri', 'a rassasié']
verbs['future']['sing'] = ['va nourrir', 'va rassasier']
verbs['past']['plur'] = ['ont nourri', 'ont rassasié']
verbs['future']['plur'] = ['vont nourrir', 'vont rassasier']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_struct'][2] = 1
verbs['except_structure'] = {'tenses': ['past', 'future'], 'word': ['pourrir', 'moisir'], 'counter': [0, 0], 'future': {'sing': ['va pourrir', 'va moisir'], 'plur': ['vont pourrir', 'vont moisir']}, 'counter_tenses': [0, 0], 'past': {'sing': ['a pourri', 'a moisi'], 'plur': ['ont pourri', 'ont moisi']}}

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_fruits

for obj in objects['word']:
    prepositions[obj] = prepo_anim

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[0][sub] = prepo2_0fruits
    prepositions2[1][sub] = prepo2_1fruits

keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)


## 1 Manger

subjects = {}
subjects['word'] = Anim
subjects['sexe'] = Anim_sexe
subjects['plurality'] = Anim_plurality
make_counter(subjects)

objects = {}   
objects['word'] = Inanim_object
objects['sexe'] = Inanim_object_sexe
objects['plurality'] = Inanim_object_plurality
make_counter(objects)
objects['except_struct'] = [0,0,0]

verbs = {}
verbs['word'] = ['manger', 'dévorer']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a mangé', 'a dévoré']
verbs['future']['sing'] = ['va manger', 'va dévorer']
verbs['past']['plur'] = ['ont mangé', 'ont dévoré']
verbs['future']['plur'] = ['vont manger', 'vont dévorer']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_struct'][2] = 1 # except for the verb ending the sentence (structure3)
verbs['except_structure'] = {'tenses': ['future', 'past'], 'future': {'sing': ['va manger'], 'plur': ['vont manger']}, 'past': {'sing': ['a mangé'], 'plur': ['ont mangé']}, 'word': ['manger'], 'counter': [0], 'counter_tenses':[0, 0]}

verbs['semantic_anom'] = anim_verbs_anomalies

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_fruits

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[0][sub] = prepo2_0anim
    prepositions2[1][sub] = prepo2_1anim
            
keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)


## 2 Bricoler


subjects = {}
subjects['word'] = Anim
subjects['sexe'] = Anim_sexe
subjects['plurality'] = Anim_plurality
make_counter(subjects)

objects = {}        
objects['word'] = ['chariot', 'serrure', 'scooter', 'chaise', 'volet', 'voiture', 'meuble', 'radio', 'vélo', 'moto', 'fusil', 'chariots', 'scooters', 'chaises', 'volets', 'vélos', 'motos', 'meubles', 'serrures', 'fusils']
objects['sexe'] = ['masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc','masc', 'masc', 'femi', 'masc', 'masc', 'femi', 'masc', 'femi', 'masc']
objects['plurality'] = ['sing', 'sing', 'sing', 'sing', 'sing' , 'sing', 'sing' , 'sing', 'sing', 'sing' , 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']
make_counter(objects)
objects['except_struct'] = [0,0,0] 

verbs = {}
verbs['word'] = ['réparer', 'bricoler']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a réparé', 'a bricolé']
verbs['future']['sing'] = ['va réparer', 'va bricoler']
verbs['past']['plur'] = ['ont réparé', 'ont bricolé']
verbs['future']['plur'] = ['vont réparer', 'vont bricoler']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['semantic_anom'] = anim_verbs_anomalies

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_struct'][2] = 1 # except for the verb ending the sentence (structure3)
verbs['except_structure'] = {'tenses': ['future', 'past'], 'future': {'sing': ['va bricoler'], 'plur': ['vont bricoler']}, 'past': {'sing': ['a bricolé'], 'plur': ['ont bricolé']}, 'word': ['bricoler'], 'counter': [0], 'counter_tenses':[0, 0]}

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_anim
 
keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[0][sub] = prepo2_0anim
    prepositions2[1][sub] = prepo2_1anim

keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)


## 3 Graines

subjects = {}
subjects['word'] = ['graine', 'noyau', 'pépin', 'graines', 'noyaux', 'pépins']
subjects['sexe'] = ['femi', 'masc', 'masc', 'femi', 'masc', 'masc']
subjects['plurality'] = ['sing', 'sing', 'sing', 'plur', 'plur', 'plur']
make_counter(subjects)

objects = {}
objects['word'] = ['plante', 'arbre', 'pousse', 'arbuste', 'plantes', 'arbres', 'pousses', 'arbustes']  
objects['sexe'] = ['femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc']
objects['plurality'] = ['sing', 'sing', 'sing', 'sing', 'plur', 'plur', 'plur', 'plur']
objects['sing'] = objects['word'][0:int(len(objects['word'])/2)]
objects['plur'] = objects['word'][int(len(objects['word'])/2)::]
make_counter(objects)
make_counter(objects,'sing'), make_counter(objects, 'plur')
objects['except_struct'] = [0,0,0] 

verbs = {}
verbs['word'] = ['donner', 'devenir']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a donné']
verbs['future']['sing'] = ['va donner', 'va devenir']
verbs['past']['plur'] = ['ont donné']
verbs['future']['plur'] = ['vont donner', 'vont devenir']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_struct'][2] = 1
verbs['except_structure'] = {'future': {'sing': ['va germer'], 'plur': ['vont germer']}, 'counter': [0], 'tenses': ['past', 'future'], 'counter_tenses': [0, 0], 'word': ['germer'], 'past': {'sing': ['a germé'], 'plur': ['ont germé']}}

prepositions = {}
prepositions['graine'] = ['de figue', 'de fruit']
prepositions['graines'] = ['de figue', 'de fruit']
prepositions['noyau'] = ['de pruneau', 'de cerise']
prepositions['noyaux'] = ['de pruneau', 'de cerise']
prepositions['pépin'] = ['de pomme', 'de poire', 'de citron', 'de raisin']
prepositions['pépins'] = ['de pomme', 'de poire', 'de citron', 'de raisin']

for obj in objects['word']:
        prepositions[obj] = ['du jardin', 'du verger', 'du parc', 'du potager', 'du pré']    
        
prepositions['arbre'], prepositions['arbre'] = ['du jardin', 'du verger', 'du parc', 'du pré'], ['du jardin', 'du verger', 'du parc', 'du pré']
prepositions['arbuste'], prepositions['arbustes'] = ['du jardin', 'du verger', 'du parc', 'du pré'],   ['du jardin', 'du verger', 'du parc', 'du pré']

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[1][sub] = prepo2_1graines
prepositions2[0]['graine'] = prepositions['graine']
prepositions2[0]['graines'] = prepositions['graines']
prepositions2[0]['noyau'] = prepositions['noyau']
prepositions2[0]['noyaux'] = prepositions['noyaux']
prepositions2[0]['pépin'] = prepositions['pépin']
prepositions2[0]['pépins'] = prepositions['pépins']

keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

determinants = {}   # we cannot have '...va donner ces plantes'
determinants['masc'] = ['un']
determinants['femi'] = ['une']
determinants['counter'] = [0]

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les']
determinants_plural['femi'] = ['des', 'les']
determinants_plural['counter'] = [0,0]


words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)


## 4 Boire


subjects = {}
subjects['word'] = Anim
subjects['sexe'] = Anim_sexe
subjects['plurality'] = Anim_plurality
make_counter(subjects)


objects = {}      
objects['word'] = ['apéritif', 'boisson', 'sirop', 'liqueur', 'soda', 'limonade', 'thé', 'tisane', 'café', 'infusion', 'sodas', 'tisanes', 'apéritifs', 'boissons']
objects['sexe'] = ['masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi']
objects['plurality'] = ['sing', 'sing' , 'sing', 'sing' , 'sing', 'sing', 'sing' , 'sing', 'sing' , 'sing', 'plur', 'plur', 'plur', 'plur']
make_counter(objects)
objects['except_struct'] = [0,0,0]

verbs = {}
verbs['word'] = ['boire', 'avaler']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a bu', 'a avalé']
verbs['future']['sing'] = ['va boire', 'va avaler']
verbs['past']['plur'] = ['ont bu', 'ont avalé']
verbs['future']['plur'] = ['vont boire', 'vont avaler']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['semantic_anom'] = anim_verbs_anomalies

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_struct'][2] = 1 # except for the verb ending the sentence (structure3)
verbs['except_structure'] = {'tenses': ['future', 'past'], 'future': {'sing': ['va boire'], 'plur': ['vont boire']}, 'past': {'sing': ['a bu'], 'plur': ['ont bu']}, 'word': ['boire'], 'counter': [0], 'counter_tenses':[0, 0]}

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_obj_boire

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[0][sub] = prepo2_0anim
    prepositions2[1][sub] = prepo2_1anim

keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

determinants = {}
determinants['masc'] = ['un', 'le', 'ce']
determinants['femi'] = ['une', 'la', 'cette']
determinants['counter'] = [0,0,0]

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les', 'ces']
determinants_plural['femi'] = ['des', 'les', 'ces']
determinants_plural['counter'] = [0,0,0]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)

## 5 Lire


subjects = {}
subjects['word'] = Anim
subjects['sexe'] = Anim_sexe
subjects['plurality'] = Anim_plurality
make_counter(subjects)

objects = {} 
objects['word'] = ['lettre', 'note', 'carte', 'carnet', 'liste', 'manuel', 'fiche', 'papier', 'lettres', 'notes', 'cartes', 'carnets', 'fiches', 'manuels', 'papiers'] #roman méthode procédé?
objects['sexe'] = ['femi', 'femi', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'femi', 'femi', 'masc', 'femi', 'masc', 'masc']
objects['plurality'] = ['sing', 'sing' , 'sing', 'sing' , 'sing', 'sing' , 'sing', 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']
make_counter(objects)
objects['except_struct'] = [0,0,0]

# verbs = {}
# verbs['word'] = ['lire']
# verbs['past'], verbs['future'] = {}, {}
# verbs['past']['sing'] = ['a lu']
# verbs['future']['sing'] = ['va lire']
# verbs['past']['plur'] = ['ont lu']
# verbs['future']['plur'] = ['vont lire']
# verbs['tenses'] = ['past', 'future']
# make_counter(verbs)
# make_counter(verbs, 'tenses')

verbs = {}
verbs['word'] = ['lire', 'consulter']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a lu', 'a consulté']
verbs['future']['sing'] = ['va lire', 'va consulter']
verbs['past']['plur'] = ['ont lu', 'ont consulté']
verbs['future']['plur'] = ['vont lire', 'vont consulter']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

verbs['except'] = [0 for i in range(len(subjects['word']))]
verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
verbs['except_structure'] = {'past': {'plur': ['ont lu'], 'sing': ['a lu']}, 'future': {'plur': ['vont lire'], 'sing': ['va lire']}, 'word': ['lire'], 'counter': [0], 'tenses': ['past', 'future'], 'counter_tenses': [0, 0]}

verbs['semantic_anom'] = anim_verbs_anomalies

# 
# verbs['except'] = [0 for i in range(len(subjects['word']))]
# verbs['except_struct'] = [0 for i in range(len(structures['structure']))]
# verbs['except_structure'] = {'past': {'plur': ['ont lu', 'ont étudié'], 'sing': ['a lu', 'a étudié']}, 'future': {'plur': ['vont lire', 'vont étudier'], 'sing': ['va lire', 'va étudier']}, 'word': ['lire', 'étudier'], 'counter': [0, 0], 'tenses': ['past', 'future'], 'counter_tenses': [0, 0]}


prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_anim
    #['de Jean', 'de Michel', 'de Suzanne', 'de Marie', 'avec attention', 'avec hâte', 'sans hâte', 'très rapidement', 'très lentement']
 
keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

prepositions2 = [{}, {}]
for sub in subjects['word']:
    prepositions2[0][sub] = prepo2_0anim
    prepositions2[1][sub] = prepo2_1anim	
    
keys = list(prepositions2[0].keys())
[make_counter(prepositions2[0], entry) for entry in keys]
keys = list(prepositions2[1].keys())
[make_counter(prepositions2[1], entry) for entry in keys]

exceptions = {}
exceptions['subjects'] = [0 for i in range(len(subjects['word']))]
exceptions['objects'] = [0 for i in range(len(objects['word']))]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'exceptions':exceptions.copy(), 'prepositions2':prepositions2.copy()}

Words.append(words)

## Types

# Types are the 6 different possibilities for sentences: about manger, bricoler, graines, boire and lire.

Types = [i for i in range(len(Words))]
Types_counter = [0 for i in range(len(Words))]

## Counter

# the structure Counter contains all words, all word category, and all characteristic (femi/masc, sing/plur), along with a counter of overall occurences.

Counter = {}
Counter['word'] = []
Counter['infinitive_verbs'] = [] # remember all occurences of a verb regardless of the tense and plurality

for type in Types:
    for word_type in Words[type].keys():
        if (word_type == 'objects') or (word_type == 'subjects'):
            for word in Words[type][word_type]['word']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            try:
                for word in Words[type][word_type]['except_structure']['word']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
            except:
                pass
        elif word_type == 'prepositions':
            for word in Words[type][word_type].keys():
                for prepo in Words[type][word_type][word]:
                    if prepo not in Counter['word']:
                        Counter['word'].append(prepo)
        elif word_type == 'prepositions2':
            for i in range(2):
                for word in Words[type][word_type][i].keys():
                    for prepo in Words[type][word_type][i][word]:
                        if prepo not in Counter['word']:
                            Counter['word'].append(prepo)
        elif word_type == 'verbs':
            for word in Words[type][word_type]['word']:
                if word not in Counter['infinitive_verbs']:
                    Counter['infinitive_verbs'].append(word)
            for word in Words[type][word_type]['future']['sing']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            for word in Words[type][word_type]['future']['plur']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            for word in Words[type][word_type]['past']['sing']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            for word in Words[type][word_type]['past']['plur']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            try:
                for word in Words[type][word_type]['except_structure']['word']:
                    if word not in Counter['infinitive_verbs']:
                        Counter['infinitive_verbs'].append(word)
                for word in Words[type][word_type]['except_structure']['future']['sing']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_structure']['future']['plur']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_structure']['past']['sing']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_structure']['past']['plur']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
            except:
                pass
            try:
                for word in Words[type][word_type]['except_verbs']['word']:
                    if word not in Counter['infinitive_verbs']:
                        Counter['infinitive_verbs'].append(word)
                for word in Words[type][word_type]['except_verbs']['future']['sing']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_verbs']['future']['plur']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_verbs']['past']['sing']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
                for word in Words[type][word_type]['except_verbs']['past']['plur']:
                    if word not in Counter['word']:
                        Counter['word'].append(word)
            except:
                pass
        elif word_type == 'determinants':
            for word in Words[type][word_type]['masc']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            for word in Words[type][word_type]['femi']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
        elif word_type == 'determinants_plural':
            for word in Words[type][word_type]['masc']:
                if word not in Counter['word']:
                    Counter['word'].append(word)
            for word in Words[type][word_type]['femi']:
                if word not in Counter['word']:
                    Counter['word'].append(word)

Counter['word'].remove(0)

make_counter(Counter)
make_counter(Counter, 'infinitive_verbs')

## Word2Jab

word2jab = {'fruit': 'gluit', 'pépin': 'nénin', 'scooters': 'plouners', 'voisine': 'moidine', 'magasin': 'lapadin', 'lu': 'ju', 'note': 'bope', 'curé': 'vubé', 'plombier':'glompier', 'serrure': 'pessure', 'boisson': 'voiffon', 'chariot': 'churiat', 'avalé': 'abaté', 'sirop': 'bidop', 'citron': 'piglon', 'scooter': 'plouner', 'apéritif': 'abulotin', 'figues': 'siques', 'mangé': 'fanlé', 'potager': 'bomager','figue': 'sique', 'serrures': 'pessures', 'tisane': 'ripane', 'fusil': 'gunil','coiffeur': 'boilleur', 'cerises': 'cirases', 'jardin': 'barjin', 'tisanes': 'ripanes', 'citrons': 'piglons', 'facteur': 'tarbeur', 'cartes': 'daptes', 'noyau': 'goyau', 'vélo': 'béno', 'radio': 'balio', 'pousse': 'noutte', 'pruneaux': 'grupeaux', 'lire': 'jire', 'meubles': 'peurles', 'patelin': 'bamelin', 'poires': 'loives', 'bu': 'gu', 'arbre': 'ospre', 'lettres': 'bestres', 'parc': 'tolc', 'manger': 'fanler', 'meuble': 'peurle', 'volets': 'mofets', 'collègue': 'goffègue','rassasier': 'labbagier', 'pommes': 'gonnes', 'pourri': 'loubbi', 'arbuste': 'altupte', 'cousin': 'poumin', 'moisi': 'noigi', 'boire': 'goire', 'dévoré': 'géboné', 'pousses': 'nouttes', 'café': 'gapé', 'pré': 'glé', 'bistrot': 'tisprot', 'plante': 'glanbe', 'soeur': 'siour', 'pourrir': 'loubbir', 'bricolé': 'triboné','avaler': 'abater', 'frères': 'trules', 'pépins': 'nénins', 'donné': 'toffé', 'lettre': 'bestre', 'carnets': 'marbets', 'pruneau': 'grupeau', 'réparé': 'bélapé', 'raisins': 'laibins', 'voisines': 'moidines', 'réparer': 'bélaper', 'coin': 'boid', 'raisin': 'laibin', 'carnet': 'marbet', 'papier': 'babier', 'fiches': 'giches', 'moisir': 'noigir', 'devenir': 'nepelir', 'fusils': 'gunils', 'verger': 'pelber', 'listes': 'birles', 'chariots': 'churiats', 'manuel': 'bamuel', 'infusion': 'invulion', 'arbustes': 'altuptes', 'nourri': 'bounni', 'fruits': 'gluits','graines': 'braipes', 'quartier': 'quablier', 'voisin': 'moidin', 'liste': 'birle', 'nourrir': 'bounnir', 'noyaux': 'goyaux', 'soda': 'doba', 'dentiste': 'lenriste', 'amies': 'opies', 'germé': 'perné', 'tantes': 'dandes', 'voiture': 'goimure', 'boulanger': 'roulinger', 'oncle': 'ancte', 'fiche': 'giche', 'rassasié': 'labbagié', 'bricoler': 'triboner', 'village': 'volluge', 'thé': 'flé', 'commerce': 'gopperce', 'poire': 'loibe', 'sodas': 'dobas', 'graine': 'braipe', 'cerise':'cirase', 'notes': 'bopes', 'oncles': 'anctes', 'volet': 'mofet', 'cousines': 'poumines', 'plantes': 'glanbes', 'dévorer': 'géboner', 'ami': 'opi', 'amie': 'opie', 'médecin': 'balurin', 'vélos': 'bénos', 'chaise': 'flaise', 'apéritifs': 'abulotins', 'consulter': 'ronserper', 'consulté': 'ronsulpé', 'arbres': 'ospres','manuels': 'bamuels', 'moto': 'podo', 'collègues': 'goffègues', 'cousins': 'poumins', 'pomme': 'gonne', 'amis': 'opis', 'liqueur': 'tigueur', 'bar': 'tur', 'limonade': 'bimolade', 'motos': 'podos', 'libraire': 'biltaire', 'soeurs': 'siours', 'voisins': 'moidins', 'marché': 'palché', 'germer': 'perner', 'tante': 'dande', 'frère': 'trule', 'donner': 'toffer', 'chaises': 'flaises', 'carte': 'dapte','noix': 'gois', 'boissons': 'voiffons', 'papiers': 'babiers', 'cousine': 'poumine'}

## Wordlist

all_odd_words = {}
all_even_words = {'un':['sing', 'masc'], 'le':['sing', 'masc'], 'ce':['sing', 'masc'], 'une':['sing', 'femi'], 'la':['sing', 'femi'], 'cette':['sing', 'femi'], 'des':['plur'], 'les':['plur'], 'ces':['plur'], 'de':['poss'], 'du':['poss'], 'a':['verb'], 'va':['verb'], 'ont':['verb'], 'vont':['verb']}

for i_type in range(len(Words)):
    for key in ['objects', 'subjects']:
        for i_word in range(len(Words[i_type][key]['word'])):
            all_odd_words[Words[i_type][key]['word'][i_word]] = [Words[i_type][key]['plurality'][i_word], Words[i_type][key]['sexe'][i_word]]
            
    for key in ['verbs']:
        for i_word in range(len(Words[i_type][key]['word'])):
            try:
                all_odd_words[Words[i_type][key]['past']['sing'][i_word].split()[-1]] = ['verb']
                all_odd_words[Words[i_type][key]['future']['sing'][i_word].split()[-1]] = ['verb']
            except:
                pass

all_prepo = {'anim':prepo_anim, '2anim':prepo2_1anim, 'fruit':prepo_fruits, '2fruit':prepo2_1fruits}

for key in all_prepo.keys():
    for word in all_prepo[key]:
        all_odd_words[word.split()[-1]] = [key]
        