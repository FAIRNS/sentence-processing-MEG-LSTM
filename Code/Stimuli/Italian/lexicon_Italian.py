###################
###### DET ########
###################

# DEFINITE
# --------
# Initialization
determinants = {}
definit = {}
a = {}
for gender in ['masc', 'femi']:
    definit[gender] = {}
    a[gender] = {}
# Tokens
definit['masc']['sing'] = ['il', 'lo', "l'"]
definit['masc']['plur'] = ['i', 'gli']
definit['femi']['sing'] = ['la', "l'"]
definit['femi']['plur'] = ['le']

a['masc']['sing'] = ['al', 'allo', 'all']
a['masc']['plur'] = ['ai', 'agli']
a['femi']['sing'] = ['alla', 'all']
a['femi']['plur'] = ['alle']

determinants = {'definit':definit, 'a':a}

###################
###### NOUNS ######
###################

# NOUNS
# -----
# Initialization
nouns = {}
for gender in ['masc', 'femi']:
    nouns[gender] = {}
# Tokens
nouns['masc']['sing'] = ['fratello', 'studente', 'padre', 'figlio', 'ragazzo', 'bambino', 'amico', 'uomo', 'attore', 'contadino']
nouns['masc']['plur'] = ['fratelli', 'studenti', 'padri', 'figli', 'ragazzi', 'bambini', 'amici', 'uomini', 'attori', 'contadini']
nouns['femi']['sing'] = ['sorella', 'studentessa', 'madre', 'figlia', 'ragazza', 'bambina', 'amica', 'donna', 'attrice', 'contadina']
nouns['femi']['plur'] = ['sorelle', 'studentesse', 'madri', 'figlie', 'ragazze', 'bambine', 'amiche', 'donne', 'attrici', 'contadine']
# nouns['masc']['sing'] = ['atleta', 'zio', 'ragazzo', 'falegname', 'dottore', 'contadino', 'padre', 'amico', 'avvocato', 'uomo', 'poeta', 'cantante', 'insegnante']
# nouns['femi']['sing'] = ['zia', 'ragazza', 'madre', 'donna', 'vittima']
# nouns['masc']['plur'] = ['atleti', 'zii', 'ragazzi', 'falegnami', 'dottori', 'contandini', 'padri', 'amici', 'avvocati', 'uomini', 'poeti', 'cantanti', 'insegnanti']
# nouns['femi']['plur'] = ['zie', 'ragazze', 'madri', 'donne', 'vittime']

# LOCATION NOUNS
# --------------
# Initialization
location_nouns = {}
for gender in ['masc', 'femi']:
    location_nouns[gender] = {}
# Tokens
location_nouns['masc']['sing'] = ['gatto', 'cane', 'tavolo', 'albero']
location_nouns['masc']['plur'] = ['gatti', 'cani', 'tavoli', 'alberi']
location_nouns['femi']['sing'] = ['gatta', 'cagna', 'macchina', 'sedia']
location_nouns['femi']['plur'] = ['gatte', 'cagne', 'macchine', 'sedie']
# location_nouns['masc']['sing'] = ['gatto', 'cane', 'tavolo', 'albero', 'camion']
# location_nouns['masc']['plur'] = ['gatti', 'cani', 'tavoli', 'alberi', 'camion']
# location_nouns['femi']['sing'] = ['macchina', 'bicicletta', 'sedia', 'gatta', 'cagna', 'scrivania', 'finestra' ]
# location_nouns['femi']['plur'] = ['macchine', 'bici', 'sedie', 'gatte', 'cagne', 'scrivanie', 'finestre']


###################
###### VERBS ######
###################

# VERBS
# -----
# Initialization
verbs = {}
# Tokens
verbs['sing'] = ['accoglie', 'ama', 'attrae', 'blocca', 'conosce', 'critica', 'difende', 'evita', 'ferma', 'guarda', 'ignora', 'incontra', 'indica', 'interrompe', 'osserva', 'ricorda', 'saluta']
verbs['plur'] = ['accolgono', 'amano', 'attraggono', 'bloccano', 'conoscono', 'criticano', 'difendono', 'evitano', 'fermano', 'guardano', 'ignorano', 'incontrano', 'indicano', 'interrompono', 'osservano', 'ricordano', 'salutano']
#@{$verbs{"singular"}}=("admires",
		       # "approves",
		       # "avoids",
		       # "confuses",
		       # "criticizes",
		       # "discourages",
		       # "encourages",
		       # "engages",
		       # "greets",
		       # "inspires",
		       # "knows",
		       # "observes",
		       # "remembers",
		       # "stimulates",
		       # "understands");

# MATRIX VERBS
# -----
# Initialization
matrix_verbs = {}
# Tokens
matrix_verbs['sing'] = ['crede', 'dice', 'pensa']
matrix_verbs['plural'] = ['credono', 'dicono', 'pensano']


##########################
###### PREPOSITIONS ######
##########################

# LOCATION PREPOSITIONS
# -----
# Initialization
loc_preps = {}
for gender in ['masc', 'femi']:
    loc_preps[gender] = {}
# Tokens (second word will be used to choose the right article from determinats{} - 'a'/'definit'/)
loc_preps = ['vicino_a a', 'dietro_a a', 'davanti_a a', 'accanto_a a']
#loc_preps = ['vicino a', 'dietro definit', 'oltre a', 'sopra definit', 'sotto definit']


Words = {'determinants':determinants.copy(), 'nouns':nouns.copy(), 'location_nouns':location_nouns.copy(), 'verbs':verbs.copy(), 'matrix_verbs':matrix_verbs.copy(), 'loc_preps':loc_preps.copy()}
