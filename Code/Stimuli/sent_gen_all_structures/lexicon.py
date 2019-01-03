Words = []

determinants = {}
determinants['masc'] = ['un', 'le', 'ce']
determinants['femi'] = ['une', 'la', 'cette']

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les', 'ces']
determinants_plural['femi'] = ['des', 'les', 'ces']

def make_counter(dic, name=None):
    if name==None:
        dic['counter'] = [0 for i in range(len(dic['word']))]
    else:
        dic['counter_'+name] = [0 for i in range(len(dic[name]))]
    return 


## GENERAL : 

Inanim_object = ['fruit', 'pomme', 'citron', 'poire', 'figue', 'cerise', 'pruneau', 'fruits', 'pommes', 'citrons', 'poires', 'raisins', 'figues', 'cerises', 'pruneaux']
Inanim_object_sexe = ['masc', 'femi', 'masc', 'femi', 'femi', 'femi', 'masc', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'femi', 'masc']
Inanim_object_plurality = ['sing', 'sing' , 'sing' , 'sing', 'sing' , 'sing', 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur']

Inanim_subject, Inanim_subject_sexe, Inanim_subject_plurality = Inanim_object, Inanim_object_sexe, Inanim_object_plurality

Anim =  ['frère', 'soeur', 'voisin', 'voisine', 'ami', 'amie', 'oncle', 'tante', 'cousin', 'cousine', 'frères', 'soeurs', 'amis', 'amies', 'oncles', 'tantes', 'cousins', 'cousines', 'voisins', 'voisines'] # collègue, collègues
Anim_sexe = ['masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi'] # masc, masc
Anim_plurality = ['sing', 'sing' , 'sing' , 'sing', 'sing' , 'sing', 'sing', 'sing', 'sing', 'sing', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur', 'plur'] # sing, plur

# prepo_anim = ['du coiffeur', 'du médecin', 'du boulanger', 'du libraire', 'du dentiste', 'du facteur', 'du plombier', 'du curé'] 

prepo_obj_boire = ['du bar', 'du bistrot', 'du magasin']

##### ADDED by Yair
prepo_anim = {}
prepo_anim['masc'] = {}
prepo_anim['femi'] = {}
prepo_anim['masc']['sing'] = ['du coiffeur', 'du boulanger', 'du plombier', 'du facteur']
prepo_anim['masc']['plur'] = ['des coiffeurs', 'des boulangers', 'des plombiers', 'des facteurs']
prepo_anim['femi']['sing'] = ['de la coiffeure', 'de la boulangère', 'de la plombière', 'de la factrice']
prepo_anim['femi']['plur'] = ['des coiffeures', 'des boulangères', 'des plombières', 'des factrices']

prepo_fruits = {}
prepo_fruits['masc'] = {}
prepo_fruits['femi'] = {}
prepo_fruits['masc']['sing'] = ['du marché', 'du magasin', 'du commerce', 'du jardin', 'du verger']
prepo_fruits['masc']['plur'] = ['des marchés', 'des magasins', 'des commerces', 'des jardins', 'des vergers']
prepo_fruits['femi']['sing'] = ['de la X', 'de la Y', 'de la Z', 'de la A', 'de la B']
prepo_fruits['femi']['plur']  = ['des Xes', 'des Yes', 'des Zes', 'des Aes', 'des Bes']


adjectives_inanim = {}
adjectives_inanim['masc'] = {}
adjectives_inanim['femi'] = {}
adjectives_inanim['masc']['sing'] = ['vert', 'lointain']
adjectives_inanim['masc']['plur'] = ['verts', 'lointains']
adjectives_inanim['femi']['sing'] = ['verte', 'lointaine']
adjectives_inanim['femi']['plur']  = ['vertes', 'lointaines']

adjectives_anim = {}
adjectives_anim['masc'] = {}
adjectives_anim['femi'] = {}
adjectives_anim['masc']['sing'] = ['méchant', 'gentil']
adjectives_anim['masc']['plur'] = ['méchants', 'gentils']
adjectives_anim['femi']['sing'] = ['méchante', 'gentille']
adjectives_anim['femi']['plur']  = ['méchantes', 'gentilles']


######

## 0 INANIM = RASSASIER


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

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_fruits

for obj in objects['word']:
    prepositions[obj] = prepo_anim

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]


words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'adjectives':adjectives_inanim.copy()}
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

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_fruits

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]
            
words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy()}
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

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_anim
 
keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'adjectives':adjectives_anim.copy(), 'adjectives':adjectives_anim.copy()}
Words.append(words)


## 3 Graines

subjects = {}
subjects['word'] = ['graine', 'noyau', 'graines', 'noyaux']
subjects['sexe'] = ['femi', 'masc', 'femi', 'masc']
subjects['plurality'] = ['sing', 'sing', 'plur', 'plur']
make_counter(subjects)

objects = {}
objects['word'] = ['plante', 'arbre', 'pousse', 'arbuste', 'plantes', 'arbres', 'pousses', 'arbustes']  
objects['sexe'] = ['femi', 'masc', 'femi', 'masc', 'femi', 'masc', 'femi', 'masc']
objects['plurality'] = ['sing', 'sing', 'sing', 'sing', 'plur', 'plur', 'plur', 'plur']
objects['sing'] = objects['word'][0:int(len(objects['word'])/2)]
objects['plur'] = objects['word'][int(len(objects['word'])/2)::]
make_counter(objects)
make_counter(objects,'sing'), make_counter(objects, 'plur')

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

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_anim

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

determinants = {}   # we cannot have '...va donner ces plantes'
determinants['masc'] = ['un']
determinants['femi'] = ['une']
determinants['counter'] = [0]

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les']
determinants_plural['femi'] = ['des', 'les']
determinants_plural['counter'] = [0,0]


words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'adjectives':adjectives_anim.copy()}
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

verbs = {}
verbs['word'] = ['boire']
verbs['past'], verbs['future'] = {}, {}
verbs['past']['sing'] = ['a bu']
verbs['future']['sing'] = ['va boire']
verbs['past']['plur'] = ['ont bu']
verbs['future']['plur'] = ['vont boire']
verbs['tenses'] = ['past', 'future']
make_counter(verbs)
make_counter(verbs, 'tenses')

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_obj_boire

keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]

determinants = {}
determinants['masc'] = ['un', 'le', 'ce']
determinants['femi'] = ['une', 'la', 'cette']
determinants['counter'] = [0,0,0]

determinants_plural = {}
determinants_plural['masc'] = ['des', 'les', 'ces']
determinants_plural['femi'] = ['des', 'les', 'ces']
determinants_plural['counter'] = [0,0,0]

words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'adjectives':adjectives_anim.copy()}
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

prepositions = {}
for sub in subjects['word']:
    prepositions[sub] = prepo_anim
for obj in objects['word']:
    prepositions[obj] = prepo_anim
    #['de Jean', 'de Michel', 'de Suzanne', 'de Marie', 'avec attention', 'avec hâte', 'sans hâte', 'très rapidement', 'très lentement']
 
keys = list(prepositions.keys())
[make_counter(prepositions, entry) for entry in keys]
    
words = {'subjects':subjects.copy(), 'objects':objects.copy(), 'verbs':verbs.copy(), 'prepositions':prepositions.copy(), 'determinants':determinants.copy(), 'determinants_plural':determinants_plural.copy(), 'adjectives':adjectives_anim.copy()}
Words.append(words)