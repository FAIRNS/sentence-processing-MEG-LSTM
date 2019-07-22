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
definit['masculine']['singular'] = ['il', 'lo', "l'"]
definit['masculine']['plural'] = ['i', 'gli']
definit['feminine']['singular'] = ['la', "l'"]
definit['feminine']['plural'] = ['le']

a['masculine']['singular'] = ['al', 'allo', "all'"]
a['masculine']['plural'] = ['ai', 'agli']
a['feminine']['singular'] = ['alla', "all'"]
a['feminine']['plural'] = ['alle']

determinants = {'definit':definit, 'a':a}

###################
###### NOUNS ######
###################
# Initialization
nouns = {}
for gender in ['masculine', 'feminine']:
    nouns[gender] = {}
# Tokens
nouns['masculine']['singular'] = ['fratello', 'studente', 'padre', 'figlio', 'ragazzo', 'bambino', 'amico', 'uomo', 'attore', 'contadino']
nouns['masculine']['plural'] = ['fratelli', 'studenti', 'padri', 'figli', 'ragazzi', 'bambini', 'amici', 'uomini', 'attori', 'contadini']
nouns['feminine']['singular'] = ['sorella', 'studentessa', 'madre', 'figlia', 'ragazza', 'bambina', 'amica', 'donna', 'attrice', 'contadina']
nouns['feminine']['plural'] = ['sorelle', 'studentesse', 'madri', 'figlie', 'ragazze', 'bambine', 'amiche', 'donne', 'attrici', 'contadine']

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
verbs['singular'] = ['accoglie', 'ama', 'attrae', 'blocca', 'conosce', 'critica', 'difende', 'evita', 'ferma', 'guarda', 'ignora', 'incontra', 'indica', 'interrompe', 'osserva', 'saluta']
verbs['plural'] = ['accolgono', 'amano', 'attraggono', 'bloccano', 'conoscono', 'criticano', 'difendono', 'evitano', 'fermano', 'guardano', 'ignorano', 'incontrano', 'indicano', 'interrompono', 'osservano', 'salutano']

copula = {}
copula['singular'] = 'è'
copula['plural'] = 'sono'

# MATRIX VERBS
# -----
# Initialization
matrix_verbs = {}
# Tokens
matrix_verbs['singular'] = ['ricorda', 'dice', 'dichiara']
matrix_verbs['plural'] = ['ricordano', 'dicono', 'dichiarano']


##########################
###### PREPOSITIONS ######
##########################

# LOCATION PREPOSITIONS
# -----
# Tokens (second word will be used to choose the right article from determinats{} - 'a'/'definit'/)
loc_preps = ['vicino a', 'dietro a', 'davanti a', 'accanto a']


##########################
####### ADJECTIVES #######
##########################
adjectives = {}
for gender in ['masculine', 'feminine']:
    adjectives[gender] = {}
adjectives['masculine']['singular'] = ['bello', 'famoso', 'brutto', 'ricco', 'povero', 'basso', 'alto', 'grasso', 'cattivo', 'buono', 'lento', 'nuovo']
adjectives['masculine']['plural'] = ['belli', 'famosi', 'brutti', 'ricchi', 'poveri', 'bassi', 'alti', 'grassi', 'cattivi', 'buoni', 'lenti', 'nuovi']
adjectives['feminine']['singular'] = ['bella', 'famosa', 'brutta', 'ricca', 'povera', 'bassa', 'alta', 'grassa', 'cattiva', 'buona', 'lenta', 'nuova']
adjectives['feminine']['plural'] = ['belle', 'famose', 'brutte', 'ricche', 'povere', 'basse', 'alte', 'grasse', 'cattive', 'buone', 'lente', 'nuove']


Words = {'determinants':determinants.copy(), 'nouns':nouns.copy(), 'location_nouns':location_nouns.copy(), 'verbs':verbs.copy(), 'copula':copula.copy(), 'matrix_verbs':matrix_verbs.copy(), 'loc_preps':loc_preps.copy(), 'adjectives':adjectives.copy()}
