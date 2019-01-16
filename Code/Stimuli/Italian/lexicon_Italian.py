###################
###### DET ########
###################

# DEFINITE
# --------
# Initialization
determinants = {}
for gender in ['masc', 'femi']:
    determinants[gender] = {}
# Tokens
determinants['masc']['sing'] = ['il', 'lo', "l'"]
determinants['masc']['plur'] = ['i', 'gli']
determinants['femi']['sing'] = ['la', "l'"]
determinants['femi']['plur'] = ['le']



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
nouns['masc']['sing'] = ['zio', 'ragazzo']
nouns['masc']['plur'] = ['zii', 'ragazzi']
nouns['femi']['sing'] = ['zia', 'ragazza']
nouns['femi']['plur'] = ['zie', 'ragazze']
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
location_nouns['masc']['sing'] = ['gatto', 'cane', 'tavolo', 'albero', 'camion']
location_nouns['masc']['plur'] = ['gatti', 'cani', 'tavoli', 'alberi', 'camion']
location_nouns['femi']['sing'] = ['gatta', 'cagna', 'macchina', 'sedia','bicicletta']
location_nouns['femi']['plur'] = ['gatte', 'cagne', 'macchine', 'sedie', 'bici']
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
verbs['sing'] = ['ammira', 'approva']
verbs['plur'] = ['ammirano', 'approvano']
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
# Tokens
loc_preps['masc']['sing'] = ['vicino al', 'vicino allo', 'vicino all']
loc_preps['masc']['plur'] = ['vicino ai', 'vicino agli']
loc_preps['femi']['sing'] = ['vicino alla', 'vicino all']
loc_preps['femi']['plur'] = ['vicino alle']
# ("near",
#   "behind",
#   "beside",
#   "above",
#   "under");


Words = {'determinants':determinants.copy(), 'nouns':nouns.copy(), 'location_nouns':location_nouns.copy(), 'verbs':verbs.copy(), 'matrix_verbs':matrix_verbs.copy(), 'loc_preps':loc_preps.copy()}