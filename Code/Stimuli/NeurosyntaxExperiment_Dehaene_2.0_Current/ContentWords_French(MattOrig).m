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

i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'vite'};r{i}.addi={{'$FAST'}};
%i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'rapidly'};r{i}.addi={{'$FAST'}};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'lentement'};r{i}.addi={{'$SLOW'}};
% i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'gently'};r{i}.addi={{'$SLOW'}};

%%% for verbs, we always put the infinitive form
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'attaquer'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'lutter'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'rencontrer'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'saluer'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'nettoyer'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'polir'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'reparer'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'peindre'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'effrayer'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'terrifier'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'vibrer'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'amuser'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'frapper'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};    % note: tense is ambiguous with hit... so avoid this word   
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'pousser'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};  % strike, block, obstruct  ... or surround cover, but those seem a bit more animate to me 
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'décaler'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'heurter'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'rire'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY_VERB'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'pluerer'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'sourire'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY_VERB'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'sourciller'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD_VERB'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'arriver'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'partir'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};    
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'apparaître'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'disparaître'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'tomber'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'apparaître'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
%i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'emerge'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'exploser'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};


i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'homme'};r{i}.addi={{'$MASC','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'garçon'};r{i}.addi={{'$MASC','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'femme'};r{i}.addi={{'$FEMI','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'fille'};r{i}.addi={{'$FEMI','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'serveur'};r{i}.addi={{'$MASC','$HUMAN_NOUN','$ANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'serveuse'};r{i}.addi={{'$FEMI','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'acteur'};r{i}.addi={{'$MASC','$HUMAN_NOUN','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'actrice'};r{i}.addi={{'$FEMI','$HUMAN_NOUN','$ANIMATE'}}; 

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'voiture'};r{i}.addi={{'$FEMI','$LARGE_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'camion'};r{i}.addi={{'$MASC','$LARGE_NOUN','$INANIMATE'}};  %building or house are other options 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'building'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'house'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'poussette'};r{i}.addi={{'$FEMI','$SMALL_NOUN','$INANIMATE'}};   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'container'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'panier'};r{i}.addi={{'$MASC','$SMALL_NOUN','$INANIMATE'}};   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'stone'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   

i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'heureux'};r{i}.addi={{'$EMOTION','$HAPPY'}};  
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'joyeux'};r{i}.addi={{'$EMOTION','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'content'};r{i}.addi={{'$EMOTION','$HAPPY'}};    
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'triste'};r{i}.addi={{'$EMOTION','$SAD'}};       
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'découragé'};r{i}.addi={{'$EMOTION','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P0';r{i}.subst = {'misérable'};r{i}.addi={{'$EMOTION','$SAD'}};     

i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'petit'};r{i}.addi={{'$PHYSICAL','$SMALL'}};  
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'court'};r{i}.addi={{'$PHYSICAL','$SMALL'}};
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'minuscule'};r{i}.addi={{'$PHYSICAL','$SMALL'}};   
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'grand'};r{i}.addi={{'$PHYSICAL','$LARGE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'gros'};r{i}.addi={{'$PHYSICAL','$LARGE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'énorme'};r{i}.addi={{'$PHYSICAL','$LARGE'}};   
       
