% LoadRules_English.m
%
%%%%% substitution rules for a simple language

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

clear r;
i=0;
%%% _CLAUSE is the start symbol
i=i+1;r{i}.wt=1; r{i}.match='_CLAUSE';r{i}.subst = {'_T_P2'};

%%% basics of XBAR theory  
%%% here _P2, _P1 and _P0 refer to the three
%%% levels of "bars" or "primes" in the XBAR structure. 
%%% So _T_P2 = TP in the classical sense, _N_P2 = NP
i=i+1;r{i}.wt=1; r{i}.match='_T_P2';r{i}.subst = {'_T_SPEC','_T_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_T_P1';r{i}.subst = {'_T_P0','_T_COMP'}; 

i=i+1;r{i}.wt=1; r{i}.match='_T_SPEC';r{i}.subst = {'_D_P2'}; r{i}.lab='PPLoc1_Off';           %turn this rule OFF if chossing PPLoc1     
i=i+1;r{i}.wt=1; r{i}.match='_T_SPEC';r{i}.subst = {'_P_P2','_D_P2'}; r{i}.lab='PPLoc1_On';    %turn this rule ON if chossing PPLoc1

i=i+1;r{i}.wt=1; r{i}.match='_T_COMP';r{i}.subst = {'_V_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_D_P2';r{i}.subst = {'_D_SPEC','_D_P1'}; r{i}.addi={{'$NOMINATIVE'}};  
i=i+1;r{i}.wt=1; r{i}.match='_D_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_D_P1';r{i}.subst = {'_D_P0','_D_COMP'}; 

i=i+1;r{i}.wt=1; r{i}.match='_D_COMP';r{i}.subst = {'_N_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_N_P2';r{i}.subst = {'_N_SPEC','_N_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'_NUM'};
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'_NUM_D_P0'};   % To label the cases where the number also serves as the determiner. i.e. "one man slowly cried"          
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'#empty'};

i=i+1;r{i}.wt=1; r{i}.match='_NUM_D_P0';r{i}.subst = {'_NUM'};

i=i+1;r{i}.wt=1; r{i}.match='_N_P1';r{i}.subst = {'_N_L_ADJUNCT','_N_P1_B'}; 
i=i+1;r{i}.wt=2; r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'_A_P2'};
i=i+1;r{i}.wt=1; r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'#empty'};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P1';r{i}.subst = {'_N_P1','_N_R_ADJUNCT',}; %%% for French perhaps
%i=i+1;r{i}.wt=1; r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_A_P2'};  %%% for French perhaps
i=i+1;r{i}.wt=1; r{i}.match='_N_P1_B';r{i}.subst = {'_N_P0'};  r{i}.lab='PPLoc2_Off';           %turn this rule OFF if chossing PPLoc1 
i=i+1;r{i}.wt=1; r{i}.match='_N_P1_B';r{i}.subst = {'_N_P0','_N_COMP',}; r{i}.lab='PPLoc2_On';           %turn this rule OFF if chossing PPLoc1 

i=i+1;r{i}.wt=1; r{i}.match='_N_COMP';r{i}.subst = {'_P_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_P_P2';r{i}.subst = {'_P_SPEC','_P_P1'}; r{i}.addi={{'$LOCATIVE'}};
i=i+1;r{i}.wt=1; r{i}.match='_P_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P1';r{i}.subst = {'_P_P0','_P_COMP',}; 
i=i+1;r{i}.wt=1; r{i}.match='_P_COMP';r{i}.subst = {'_LOC_D_P2'}; %% simplified location PP

i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_P2';r{i}.subst = {'_LOC_D_P1'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_P1';r{i}.subst = {'_D_P0','_LOC_D_COMP'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_COMP';r{i}.subst = {'_LOC_N_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P2';r{i}.subst = {'_LOC_N_SPEC','_LOC_N_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_SPEC';r{i}.subst = {'#empty'};

i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P1';r{i}.subst = {'_LOC_N_L_ADJUNCT','_LOC_N_P1_B'}; 
i=i+1;r{i}.wt=2; r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'_A_P2'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'#empty'};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P1';r{i}.subst = {'_N_P1','_N_R_ADJUNCT',}; %%% for French perhaps
%i=i+1;r{i}.wt=1; r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_A_P2'};  %%% for French perhaps
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P1_B';r{i}.subst = {'_N_P0'};  


i=i+1;r{i}.wt=1; r{i}.match='_A_P2';r{i}.subst = {'_A_SPEC','_A_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'_INTENSIF'};
i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_A_P1';r{i}.subst = {'_A_P0'}; 


i=i+1;r{i}.wt=1; r{i}.match='_V_P2';r{i}.subst = {'_V_SPEC','_V_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_V_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1_B'};
i=i+1;r{i}.wt=2; r{i}.match='_V_L_ADJUNCT';r{i}.subst = {'_ADV_P2'};
i=i+1;r{i}.wt=1; r{i}.match='_V_L_ADJUNCT';r{i}.subst = {'#empty'};

i=i+1;r{i}.wt=1; r{i}.match='_ADV_P2';r{i}.subst = {'_ADV_SPEC','_ADV_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_ADV_SPEC';r{i}.subst = {'_INTENSIF'};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_P1';r{i}.subst = {'_ADV_P0'}; % no complementizer for adjectives that qualify nouns

i=i+1;r{i}.wt=1; r{i}.match='_V_P1_B';r{i}.subst = {'_VT_V_P1'};                    r{i}.lab='Trans_On';
%i=i+1;r{i}.wt=1; r{i}.match='_V_P1_B';r{i}.subst = {'_VT_V_P1','_V_R_ADJUNCT',};  % we decided no _V_R_ADJUNCT after a transitive verb bc of ambiguity of where the listener should attach the adjunct ... i..e "the man met the woman by the car" ... was it "the woman by the car" or that "the meeting" was by the car     
i=i+1;r{i}.wt=1; r{i}.match='_V_P1_B';r{i}.subst = {'_VI_V_P1'};                    r{i}.lab='InTrans_PPLoc3_Off';           %turn this rule OFF if chossing PPLoc1 
i=i+1;r{i}.wt=1; r{i}.match='_V_P1_B';r{i}.subst = {'_VI_V_P1','_V_R_ADJUNCT',};    r{i}.lab='InTrans_PPLoc3_On';           %turn this rule OFF if chossing PPLoc1 

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P1';r{i}.subst = {'_VT_V_P0','_VT_COMP',}; %% different sorts of verbs take different sorts of complements
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P1';r{i}.subst = {'_VI_V_P0'}; 

i=i+1;r{i}.wt=1; r{i}.match='_V_R_ADJUNCT';r{i}.subst = {'_P_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_VT_COMP';r{i}.subst = {'_OBJ_D_P2'};r{i}.addi={{'$ACCUSATIVE'}};

i=i+1;r{i}.wt=1; r{i}.match='_OBJ_D_P2';r{i}.subst = {'_OBJ_D_P1'};
i=i+1;r{i}.wt=1; r{i}.match='_OBJ_D_P1';r{i}.subst = {'_D_P0','_OBJ_D_COMP'};
i=i+1;r{i}.wt=1; r{i}.match='_OBJ_D_COMP';r{i}.subst = {'_OBJ_N_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_OBJ_N_P2';r{i}.subst = {'_N_SPEC','_OBJ_N_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_OBJ_N_P1';r{i}.subst = {'_N_L_ADJUNCT','_N_P0'}; 


%%% terminals

i=i+1;r{i}.wt=1; r{i}.match='_INTENSIF';r{i}.subst = {'very'};

i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'quickly'};r{i}.addi={{'$FAST'}};
%i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'rapidly'};r{i}.addi={{'$FAST'}};
i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'slowly'};r{i}.addi={{'$SLOW'}};
% i=i+1;r{i}.wt=1; r{i}.match='_ADV_P0';r{i}.subst = {'gently'};r{i}.addi={{'$SLOW'}};

%%% for verbs, we always put the infinitive form
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'attack'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$UNFRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'fight'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$UNFRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'meet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$FRIENDLY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'greet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ','$FRIENDLY'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'clean'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'polish'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'repair'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'paint'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'scare'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'terrify'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'thrill'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'amuse'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ','$HAPPY'}};

%i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'hit'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};    % note: tense is ambiguous with hit... so avoid this word   
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'push'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};  % block, obstruct  ... or surround cover, but those seem a bit more animate to me 
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'nudge'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.wt=1; r{i}.match='_VT_V_P0';r{i}.subst = {'bump'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'mab'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$HAPPY'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'mab'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE','$SAD'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'mab'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'mab'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'arrive'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};     
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'depart'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};    
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'appear'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};     % appear
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'vanish'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};

i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'decompose'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'appear'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'emerge'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.wt=1; r{i}.match='_VI_V_P0';r{i}.subst = {'explode'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};

% 'random' sentences could be detemrined by generating random assignments of values in SentInfo feeding into GenerateSentence.m      
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'a'};r{i}.addi={{'$INDEFINITE','$SINGULAR'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'some'};r{i}.addi={{'$INDEFINITE','$PLURAL'}};  
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'the'};r{i}.addi={{'$DEFINITE'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'this'};r{i}.addi={{'$DEMONSTRATIVE','$SINGULAR','$CLOSE_TO_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'that'};r{i}.addi={{'$DEMONSTRATIVE','$SINGULAR','$FAR_FROM_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'these'};r{i}.addi={{'$DEMONSTRATIVE','$PLURAL','$CLOSE_TO_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'those'};r{i}.addi={{'$DEMONSTRATIVE','$PLURAL','$FAR_FROM_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'#empty'}; r{i}.addi={{'$INDEFINITE','$NUMBER_GIVEN'}}; 

i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#future'};
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#perfect'};
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#present'};  %% aux can be omitted but signal present or past -- special case!
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#past'};

i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'one'};r{i}.addi={{'$SINGULAR'}}; % Will never be called if NoNumsForSingularNouns is set to be 1                       
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'two'};r{i}.addi={{'$PLURAL','$NUMEROSITY_LOW'}};      
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'three'};r{i}.addi={{'$PLURAL','$NUMEROSITY_LOW'}};    
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'fifty'};r{i}.addi={{'$PLURAL','$NUMEROSITY_HIGH'}};   
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'sixty'};r{i}.addi={{'$PLURAL','$NUMEROSITY_HIGH'}};   

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'man'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'boy'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'woman'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'girl'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'waiter'};r{i}.addi={{'$MASC','$ANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'waitress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'actor'};r{i}.addi={{'$MASC','$ANIMATE'}}; 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'actress'};r{i}.addi={{'$FEMI','$ANIMATE'}}; 

i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'car'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'truck'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};  %building or house are other options 
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'building'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
%i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'house'};r{i}.addi={{'$LARGE_NOUN','$INANIMATE'}};
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'box'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};   
i=i+1;r{i}.wt=1; r{i}.match='_N_P0';r{i}.subst = {'container'};r{i}.addi={{'$SMALL_NOUN','$INANIMATE'}};  %or package?... (test this) else go with items like rock that work for everything but the preposition "in"   

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

i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'on'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'in'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'at'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'near'}; r{i}.lab='ANIMATE_P';   % we use lab not addi here, bc we dont want this property propogating to all other words lower in the       
