



%%%%% additional knowledge of conjugation
past = {
    { 'shop'    'sleep' 'run'  'eat'   'drink' 'fall'   'meet'  'fight'  'see'  'prefer'    'be'   'swim' 'sing' 'hit' 'strike'},
    { 'shopped' 'slept' 'ran'  'ate'   'drank' 'fell'   'met'   'fought' 'saw'  'preferred' 'was'  'swam' 'sang' 'hit' 'struck'},
    { 'shopped' 'slept' 'ran'  'ate'   'drank' 'fell'   'met'   'fought' 'saw'  'preferred' 'were' 'swum' 'sung' 'hit' 'struck'}
    };

present = {
    { 'be' },
    { 'is' },
    { 'are'}
    };

future = {
    { },
    { },
    { }
    };

pastparticiple = {
    { 'shop'    'sleep' 'run'  'eat'   'drink' 'fall'   'meet'  'fight'  'see'  'prefer'    'be'   'swim' 'sing' 'hit' 'strike'},
    { 'shopped' 'slept' 'run'  'eaten' 'drunk' 'fallen' 'met'   'fought' 'seen' 'preferred' 'been' 'swum' 'sung' 'hit' 'struck'}
    };

% put all irregular plural-forming nouns here... else teh code just adds an s to them when plural      
plurals = {
    { 'man','woman'}; %,'waitress','box','actress' },
    { 'men','women'}; %,'waitresses','boxes','actresses' }
    };

auxiliaries = {
     { 'be'  ,'have'},
     { 'is'  ,'has',},
     { 'are' ,'have'}
     };

 
pronouns = {  %%% in order  singular: masc fem Neutr plural: masc fem; and then vertically, nominative, accusative
    { {'he', 'she', 'it'},{'they','they','they'} },
    { {'him', 'her', 'it'},{'them','them','them'} },
    };
LexList.SingPlur={'$SINGULAR'  '$PLURAL'};
LexList.Gender={'$MASC'  '$FEMI'  '$INANIMATE'};


deictic = {'there','it'};

%determiners = {};  %%% to do this these that those  a 

