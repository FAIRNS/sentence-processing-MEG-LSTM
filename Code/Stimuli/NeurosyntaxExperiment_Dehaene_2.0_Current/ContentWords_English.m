% ContentWords_English.m
%
%%%%% Here the substitution rules just for the terminal Jabberwocky words    

%%% by convention:
%%% each line in the rule matrix r codes for a matching rule of the type: match-->subst
%%% where "match" is a node type and "subst" are its children nodes.
%%% Children can have additional properties which are indicated in the
%%% optional field "addi".
%%%  _ indicates a non-terminal item (the program knows that it should
%%%  continue to expand these nodes, and that if it can't find a match, the
%%%  sentence will be ill-formed)
%%%  # indicates a special, phonologically empty or bound morpheme
%%%  $ indicates additional properties case, number, gender 
%%%  all other items are terminal words


%%% terminals

i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'quickly'};r{i}.addi={{'$FAST'}};
%i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'rapidly'};r{i}.addi={{'$FAST'}};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'slowly'};r{i}.addi={{'$SLOW'}};
% i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'gently'};r{i}.addi={{'$SLOW'}};

%%% for verbs, we always put the infinitive form
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'attack'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'fight'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'meet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'greet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'clean'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'polish'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'repair'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'paint'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'scare'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'terrify'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'thrill'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'amuse'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'strike'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};    % note: tense is ambiguous with hit... so avoid this word   
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'push'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};  % strike, block, obstruct  ... or surround cover, but those seem a bit more animate to me 
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'nudge'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'bump'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'laugh'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY_VERB'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'cry'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'smile'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'frown'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'arrive'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'depart'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};    
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'appear'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'vanish'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'fall'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'appear'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
%i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'emerge'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'explode'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};


%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'guy'};r{i}.addi={{'$MASC','$ANIMATE'}};
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'man'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'boy'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'boy'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'woman'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'girl'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'waiter'};r{i}.addi={{'$MASC','$ANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'waitress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'actor'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'actress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'car'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'truck'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};  %building or house are other options 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'building'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'house'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'stroller'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'container'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'cart'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'stone'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   

i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'happy'};r{i}.addi={{'$EMOTION','$HAPPY'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'joyful'};r{i}.addi={{'$EMOTION','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'ecstatic'};r{i}.addi={{'$EMOTION','$HAPPY'}};    
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'sad'};r{i}.addi={{'$EMOTION','$SAD'}};       
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'dejected'};r{i}.addi={{'$EMOTION','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'miserable'};r{i}.addi={{'$EMOTION','$SAD'}};     

i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'small'};r{i}.addi={{'$PHYSICAL','$SMALL'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'little'};r{i}.addi={{'$PHYSICAL','$SMALL'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'tiny'};r{i}.addi={{'$PHYSICAL','$SMALL'}};   
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'large'};r{i}.addi={{'$PHYSICAL','$LARGE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'big'};r{i}.addi={{'$PHYSICAL','$LARGE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'huge'};r{i}.addi={{'$PHYSICAL','$LARGE'}};   
       
