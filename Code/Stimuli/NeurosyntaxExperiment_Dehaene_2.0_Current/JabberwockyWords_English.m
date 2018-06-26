% JabberwockyWords_English.m
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

i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'drockly'};r{i}.addi={{'$FAST'}};
%i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'rapidly'};r{i}.addi={{'$FAST'}};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'plagly'};r{i}.addi={{'$SLOW'}};
% i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'gently'};r{i}.addi={{'$SLOW'}};

%%% for verbs, we always put the infinitive form
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'alland'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$UNFRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'firge'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$UNFRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'woat'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$FRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'plurt'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$FRIENDLY'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'sloon'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'rudise'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE1'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'retove'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'praim'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ','$TYPE2'}}; %

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'swire'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'sellify'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'thrimb'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'aldice'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'scrite'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};    %    
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'balt'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};  %  
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'tidge'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};   
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'rask'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'croil'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY'}}; % like broil...  laugh
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'bant'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'trage'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY'}}; % like tag...  smile   
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'frope'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'annake'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'debine'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};    
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'esate'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$COME'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'vetish'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE','$GO'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'roft'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'esate'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
%i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'frope'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$COME'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'belote'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE','$BE_DESTROYED'}};

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'ganter'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'gantress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'donter'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'dontress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'slounder'};r{i}.addi={{'$MASC','$ANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'sloundress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'uptor'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'uptress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'rab'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'flurk'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'delting'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'wabe'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'glirt'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'crisker'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'birk'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};      
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'stone'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   

i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'foddy'};r{i}.addi={{'$EMOTION','$HAPPY'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'altful'};r{i}.addi={{'$EMOTION','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'tenolic'};r{i}.addi={{'$EMOTION','$HAPPY'}};    
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'bap'};r{i}.addi={{'$EMOTION','$SAD'}};       
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'redasted'};r{i}.addi={{'$EMOTION','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'taferable'};r{i}.addi={{'$EMOTION','$SAD'}};     

i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'brell'};r{i}.addi={{'$PHYSICAL','$SMALL'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'brillig'};r{i}.addi={{'$PHYSICAL','$SMALL'}};
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'slithy'};r{i}.addi={{'$PHYSICAL','$SMALL'}};   
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'nedge'};r{i}.addi={{'$PHYSICAL','$LARGE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'rog'};r{i}.addi={{'$PHYSICAL','$LARGE'}};      
i=i+1;r{i}.wt=1; r{i}.match='_A_P0';r{i}.subst = {'dag'};r{i}.addi={{'$PHYSICAL','$LARGE'}};   
