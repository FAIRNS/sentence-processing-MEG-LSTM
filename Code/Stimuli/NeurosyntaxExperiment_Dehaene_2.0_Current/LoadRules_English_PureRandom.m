% LoadRules_English_PureRandom.m
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

setparameters;

clear r;
i=0;
%%% _CLAUSE is the start symbol
i=i+1;r{i}.match='_CLAUSE';r{i}.subst = {'_T_P2'};

%%% basics of XBAR theory  
%%% here _P2, _P1 and _P0 refer to the three
%%% levels of "bars" or "primes" in the XBAR structure. 
%%% So _T_P2 = TP in the classical sense, _N_P2 = NP
i=i+1;r{i}.match='_T_P2';r{i}.subst = {'_T_SPEC','_T_P1'}; 
i=i+1;r{i}.match='_T_P1';r{i}.subst = {'_T_P0','_T_COMP'}; 

i=i+1;r{i}.match='_T_SPEC';r{i}.subst = {'_D_P2'};r{i}.addi={{'$NOMINATIVE'}};

i=i+1;r{i}.match='_T_COMP';r{i}.subst = {'_V_P2'};

i=i+1;r{i}.match='_D_P2';r{i}.subst = {'_D_SPEC','_D_P1'}; 
i=i+1;r{i}.match='_D_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.match='_D_P1';r{i}.subst = {'_D_P0','_D_COMP'}; 

i=i+1;r{i}.match='_D_COMP';r{i}.subst = {'_N_P2'};

i=i+1;r{i}.match='_N_P2';r{i}.subst = {'_N_SPEC','_N_P1'}; 
i=i+1;r{i}.match='_N_SPEC';r{i}.subst = {'_NUM'};
i=i+1;r{i}.match='_N_SPEC';r{i}.subst = {'#empty'};

i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_N_L_ADJUNCT','_N_P1_B'}; 
i=i+1;r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'_A_P2'};
i=i+1;r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'#empty'};
%i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_N_P1','_N_R_ADJUNCT',}; %%% for French perhaps
%i=i+1;r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_A_P2'};  %%% for French perhaps
i=i+1;r{i}.match='_N_P1_B';r{i}.subst = {'_N_P0'};  
i=i+1;r{i}.match='_N_P1_B';r{i}.subst = {'_N_P0','_N_COMP',}; %%

i=i+1;r{i}.match='_N_COMP';r{i}.subst = {'_P_P2'};r{i}.addi={{''},{'$LOCATIVE'}};

i=i+1;r{i}.match='_P_P2';r{i}.subst = {'_P_SPEC','_P_P1'}; 
i=i+1;r{i}.match='_P_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_P0','_P_COMP',}; 
i=i+1;r{i}.match='_P_COMP';r{i}.subst = {'_LOC_N_P2'}; %% simplified location PP

i=i+1;r{i}.match='_LOC_N_P2';r{i}.subst = {'_LOC_N_SPEC','_LOC_N_P1'}; 
i=i+1;r{i}.match='_LOC_N_SPEC';r{i}.subst = {'#empty'};

i=i+1;r{i}.match='_LOC_N_P1';r{i}.subst = {'_LOC_N_L_ADJUNCT','_LOC_N_P1_B'}; 
i=i+1;r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'_A_P2'};
i=i+1;r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'#empty'};
%i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_N_P1','_N_R_ADJUNCT',}; %%% for French perhaps
%i=i+1;r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_A_P2'};  %%% for French perhaps
i=i+1;r{i}.match='_LOC_N_P1_B';r{i}.subst = {'_N_P0'};  


i=i+1;r{i}.match='_A_P2';r{i}.subst = {'_A_SPEC','_A_P1'}; 
i=i+1;r{i}.match='_A_SPEC';r{i}.subst = {'_INTENSIF'};
i=i+1;r{i}.match='_A_P1';r{i}.subst = {'_A_P0'}; 


i=i+1;r{i}.match='_V_P2';r{i}.subst = {'_V_SPEC','_V_P1'}; 
i=i+1;r{i}.match='_V_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1_B'};
i=i+1;r{i}.match='_V_L_ADJUNCT';r{i}.subst = {'_ADV_P2'};
i=i+1;r{i}.match='_V_L_ADJUNCT';r{i}.subst = {'#empty'};

i=i+1;r{i}.match='_ADV_P2';r{i}.subst = {'_ADV_SPEC','_ADV_P1'}; 
i=i+1;r{i}.match='_ADV_SPEC';r{i}.subst = {'_INTENSIF'};
i=i+1;r{i}.match='_ADV_P1';r{i}.subst = {'_ADV_P0'}; % no complementizer for adjectives that qualify nouns

i=i+1;r{i}.match='_V_P1_B';r{i}.subst = {'_VT_V_P1'}; 
i=i+1;r{i}.match='_V_P1_B';r{i}.subst = {'_VT_V_P1','_V_R_ADJUNCT',};
i=i+1;r{i}.match='_V_P1_B';r{i}.subst = {'_VI_V_P1'}; 
i=i+1;r{i}.match='_V_P1_B';r{i}.subst = {'_VI_V_P1','_V_R_ADJUNCT',};

i=i+1;r{i}.match='_VT_V_P1';r{i}.subst = {'_VT_V_P0','_VT_COMP',}; %% different sorts of verbs take different sorts of complements
i=i+1;r{i}.match='_VI_V_P1';r{i}.subst = {'_VI_V_P0'}; 

i=i+1;r{i}.match='_V_R_ADJUNCT';r{i}.subst = {'_P_P2'};

i=i+1;r{i}.match='_VT_COMP';r{i}.subst = {'_N_P2'};r{i}.addi={{'$ACCUSATIVE'}};


%%% word categories

i=i+1;r{i}.match='_A_P0';r{i}.subst = {'_EMOTION_A_P0'};
i=i+1;r{i}.match='_A_P0';r{i}.subst = {'_PHYSICAL_A_P0'};

%%% terminals

i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'#empty'}; %% intensifiers can be omitted
i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'very'};

i=i+1;r{i}.match='_ADV';r{i}.subst = {'quickly'};
i=i+1;r{i}.match='_ADV';r{i}.subst = {'rapidly'};
i=i+1;r{i}.match='_ADV';r{i}.subst = {'slowly'};
i=i+1;r{i}.match='_ADV';r{i}.subst = {'gently'};

%%% for verbs, we always put the infinitive form
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'attack'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'fight'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'meet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'greet'};r{i}.addi={{'$ANIMATE_SUB','$ANIMATE_OBJ'}};

i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'clean'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'polish'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'repair'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'paint'};r{i}.addi={{'$ANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'scare'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'terrify'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'thrill'};r{i}.addi={{'$INANIMATE_SUB','$ANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'amuse'};r{i}.addi={{'IN$ANIMATE_SUB','$ANIMATE_OBJ'}};

i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'hit'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'knock'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'nudge'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'bump'};r{i}.addi={{'$INANIMATE_SUB','$INANIMATE_OBJ'}};

i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'laugh'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'cry'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'talk'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'sleep'};r{i}.addi={{'$ANIMATE_SUB','$UNERGATIVE'}};

i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'die'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'perish'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'blush'};r{i}.addi={{'$ANIMATE_SUB','$UNACCUSATIVE'}};

i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'decompose'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'appear'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'vibrate'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'explode'};r{i}.addi={{'$INANIMATE_SUB','$UNACCUSATIVE'}};

i=i+1;r{i}.match='_D_P0';r{i}.subst = {'the'}; %%%% singular or plural, definite, demonstrative will ALL be determined by a special function 

i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#future'};
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#perfect'};
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#present'};  %% aux can be omitted but signal present or past -- special case!
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#past'};

i=i+1;r{i}.match='_NUM';r{i}.subst = {'one'};r{i}.addi={{'$SINGULAR'}};
i=i+1;r{i}.match='_NUM';r{i}.subst = {'two'};r{i}.addi={{'$PLURAL'}};
i=i+1;r{i}.match='_NUM';r{i}.subst = {'three'};r{i}.addi={{'$PLURAL'}};
i=i+1;r{i}.match='_NUM';r{i}.subst = {'fifty'};r{i}.addi={{'$PLURAL'}};
i=i+1;r{i}.match='_NUM';r{i}.subst = {'sixty'};r{i}.addi={{'$PLURAL'}};

i=i+1;r{i}.match='_N_P0';r{i}.subst = {'man'};r{i}.addi={{'$MASC','$ANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'woman'};r{i}.addi={{'$FEMI','$ANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'waiter'};r{i}.addi={{'$MASC','$ANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'waitress'};r{i}.addi={{'$FEMI','$ANIMATE'}};

i=i+1;r{i}.match='_N_P0';r{i}.subst = {'car'};r{i}.addi={{'$LARGE','$INANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'boat'};r{i}.addi={{'$LARGE','$INANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'box'};r{i}.addi={{'$SMALL','$INANIMATE'}};
i=i+1;r{i}.match='_N_P0';r{i}.subst = {'crate'};r{i}.addi={{'$SMALL','$INANIMATE'}};


i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'happy'};r{i}.addi={{'$HAPPY'}};
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'ecstatic'};r{i}.addi={{'$HAPPY'}};
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'sad'};r{i}.addi={{'$SAD'}};
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'miserable'};r{i}.addi={{'$SAD'}};

i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'small'};r{i}.addi={{'$SMALL'}};
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'tiny'};r{i}.addi={{'$SMALL'}};
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'large'};r{i}.addi={{'$LARGE'}};
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'huge'};r{i}.addi={{'$LARGE'}};

i=i+1;r{i}.match='_P_P0';r{i}.subst = {'on'};
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'in'};
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'at'};
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'by'};

