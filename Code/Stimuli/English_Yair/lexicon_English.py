###################
###### DET ########
###################
# DEFINITE
# --------
# Initialization

determinants = {}
definit = {}
a = {}
for gender in ['masculine', 'feminine']:
    definit[gender] = {}
    a[gender] = {}
# Tokens
definit['masculine']['singular'] = ['The']
definit['masculine']['plural'] = ['The']
definit['feminine']['singular'] = ['The']
definit['feminine']['plural'] = ['The']

a['masculine']['singular'] = ['a', 'an']
a['masculine']['plural'] = ['']
a['feminine']['singular'] = ['a', 'an']
a['feminine']['plural'] = ['']

determinants = {'definit':definit, 'a':a}

###################
###### NOUNS ######
###################
# Initialization
nouns = {}
for gender in ['masculine', 'feminine']:
    nouns[gender] = {}
# Tokens
nouns['masculine']['singular'] = ['brother', 'student', 'father', 'son', 'boy', 'friend', 'man', 'actor', 'farmer']
nouns['masculine']['plural'] = ['brothers', 'students', 'fathers', 'sons', 'boys', 'friends', 'men', 'actors', 'farmers']
nouns['feminine']['singular'] = ['sister', 'student', 'mother', 'daughter', 'girl', 'friend', 'woman', 'actress', 'farmer']
nouns['feminine']['plural'] = ['sisters', 'students', 'mothers', 'daughters', 'girls', 'friends', 'women', 'actresses', 'farmers']

# LOCATION NOUNS
# --------------
# Initialization
location_nouns = {}
for gender in ['masculine', 'feminine']:
    location_nouns[gender] = {}
# Tokens
location_nouns['masculine']['singular'] = nouns['masculine']['singular']
location_nouns['masculine']['plural'] = nouns['masculine']['plural']
location_nouns['feminine']['singular'] = nouns['feminine']['singular']
location_nouns['feminine']['plural'] = nouns['feminine']['plural']

###################
###### VERBS ######
###################
# Initialization
verbs = {}
# Tokens
verbs['singular'] = ['welcomes', 'watches', 'attracts', 'blocks', 'knows', 'defends', 'avoids', 'stops', 'ignores', 'meets', 'interrupts', 'observes', 'greets']
verbs['plural'] =  ['welcome',   'watch',  'attract',  'block',  'know',   'defend',  'avoid',   'stop', 'ignore', 'meet', 'interrupt', 'observe', 'greet']

copula = {}
copula['singular'] = 'is'
copula['plural'] = 'are'

# MATRIX VERBS
# -----
# Initialization
matrix_verbs = {}
# Tokens
matrix_verbs['singular'] = ['remembers', 'says', 'declares']
matrix_verbs['plural'] =   ['remember' , 'say', 'declare']


##########################
###### PREPOSITIONS ######
##########################

# LOCATION PREPOSITIONS
# -----
# Tokens (second word will be used to choose the right article from determinats{} - 'a'/'definit'/)
loc_preps = ['near', 'behind', 'before', 'next to']


##########################
####### ADJECTIVES #######
##########################
adjectives = {}
#for gender in ['masculine', 'feminine']:
#    adjectives[gender] = {}
#adjectives['masculine']['singular'] = ['bello', 'famoso', 'brutto', 'ricco', 'povero', 'basso', 'alto', 'grasso', 'cattivo', 'buono', 'lento', 'nuovo']
#adjectives['masculine']['plural'] = ['belli', 'famosi', 'brutti', 'ricchi', 'poveri', 'bassi', 'alti', 'grassi', 'cattivi', 'buoni', 'lenti', 'nuovi']
#adjectives['feminine']['singular'] = ['bella', 'famosa', 'brutta', 'ricca', 'povera', 'bassa', 'alta', 'grassa', 'cattiva', 'buona', 'lenta', 'nuova']
#adjectives['feminine']['plural'] = ['belle', 'famose', 'brutte', 'ricche', 'povere', 'basse', 'alte', 'grasse', 'cattive', 'buone', 'lente', 'nuove']


Words = {'determinants':determinants.copy(), 'nouns':nouns.copy(), 'location_nouns':location_nouns.copy(), 'verbs':verbs.copy(), 'copula':copula.copy(), 'matrix_verbs':matrix_verbs.copy(), 'loc_preps':loc_preps.copy(), 'adjectives':adjectives.copy()}
