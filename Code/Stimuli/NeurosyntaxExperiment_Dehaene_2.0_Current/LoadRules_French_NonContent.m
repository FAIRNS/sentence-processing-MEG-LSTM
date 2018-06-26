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
i=i+1;r{i}.wt=1; r{i}.match='_CLAUSE';r{i}.subst = {'_T_P2'}; %1

%%% basics of XBAR theory  
%%% here _P2, _P1 and _P0 refer to the three
%%% levels of "bars" or "primes" in the XBAR structure. 
%%% So _T_P2 = TP in the classical sense, _N_P2 = NP
i=i+1;r{i}.wt=1; r{i}.match='_T_P2';r{i}.subst = {'_T_SPEC','_T_P1'}; %2
i=i+1;r{i}.wt=1; r{i}.match='_T_P1';r{i}.subst = {'_T_P0','_T_COMP'}; %3

i=i+1;r{i}.wt=1; r{i}.match='_T_SPEC';r{i}.subst = {'_D_P2'};           r{i}.lab='PPLoc1_Off'; %4          %turn this rule OFF if chossing PPLoc1     
i=i+1;r{i}.wt=1; r{i}.match='_T_SPEC';r{i}.subst = {'_P_P2','_D_P2'};   r{i}.lab='PPLoc1_On'; %5    %turn this rule ON if chossing PPLoc1

i=i+1;r{i}.wt=1; r{i}.match='_T_COMP';r{i}.subst = {'_V_P2'}; %6

i=i+1;r{i}.wt=1; r{i}.match='_D_P2';r{i}.subst = {'_D_SPEC','_D_P1'}; r{i}.addi={{'$NOMINATIVE'}};  %7
i=i+1;r{i}.wt=1; r{i}.match='_D_SPEC';r{i}.subst = {'#empty'}; %8
i=i+1;r{i}.wt=1; r{i}.match='_D_P1';r{i}.subst = {'_D_P0','_D_COMP'}; %9

i=i+1;r{i}.wt=1; r{i}.match='_D_COMP';r{i}.subst = {'_N_P2'}; %10

i=i+1;r{i}.wt=1; r{i}.match='_N_P2';r{i}.subst = {'_N_SPEC','_N_P1'}; %11
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'_NUM'}; %12
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'_NUM_D_P0'}; %13  % To label the cases where the number also serves as the determiner. i.e. "one man slowly cried"          
i=i+1;r{i}.wt=1; r{i}.match='_N_SPEC';r{i}.subst = {'#empty'}; %14

i=i+1;r{i}.wt=1; r{i}.match='_NUM_D_P0';r{i}.subst = {'_NUM'}; %15

i=i+1;r{i}.wt=1; r{i}.match='_N_P1';r{i}.subst = {'_N_P1_B'};  r{i}.lab='PPLoc2_Off';  %19           %turn this rule OFF if chossing PPLoc2 
i=i+1;r{i}.wt=1; r{i}.match='_N_P1';r{i}.subst = {'_N_P1_B','_N_COMP'}; r{i}.lab='PPLoc2_On'; %20           %turn this rule ON if chossing PPLoc2 

i=i+1;r{i}.wt=1; r{i}.match='_N_P1_B';r{i}.subst = {'_N_L_ADJUNCT','_N_P0'}; %16
i=i+1;r{i}.wt=1; r{i}.match='_N_P1_B';r{i}.subst = {'_N_P0','_N_R_ADJUNCT'}; %16...

i=i+1;r{i}.wt=2; r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'_PHYSICAL_A_P2'}; %17
i=i+1;r{i}.wt=1; r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'#empty'}; %18
i=i+1;r{i}.wt=2; r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_EMOTION_A_P2'}; %17
i=i+1;r{i}.wt=1; r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'#empty'}; %18


i=i+1;r{i}.wt=1; r{i}.match='_N_COMP';r{i}.subst = {'_P_P2'}; %21

i=i+1;r{i}.wt=1; r{i}.match='_P_P2';r{i}.subst = {'_P_SPEC','_P_P1'}; r{i}.addi={{'$LOCATIVE'}}; %22
i=i+1;r{i}.wt=1; r{i}.match='_P_SPEC';r{i}.subst = {'#empty'}; %23
i=i+1;r{i}.wt=1; r{i}.match='_P_P1';r{i}.subst = {'_P_P0','_P_COMP'}; %24 
i=i+1;r{i}.wt=1; r{i}.match='_P_COMP';r{i}.subst = {'_LOC_D_P2'}; %25  %% simplified location PP

i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_P2';r{i}.subst = {'_LOC_D_P1'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_P1';r{i}.subst = {'_D_P0','_LOC_D_COMP'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_D_COMP';r{i}.subst = {'_LOC_N_P2'};

i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P2';r{i}.subst = {'_LOC_N_SPEC','_LOC_N_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_SPEC';r{i}.subst = {'#empty'};

i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P1';r{i}.subst = {'_N_L_ADJUNCT','_LOC_N_P1_B'}; 
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P1';r{i}.subst = {'_LOC_N_P1_B','_N_R_ADJUNCT'};
% i=i+1;r{i}.wt=2; r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'_PHYSICAL_A_P2'};
% i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_L_ADJUNCT';r{i}.subst = {'#empty'};
% i=i+1;r{i}.wt=2; r{i}.match='_LOC_N_R_ADJUNCT';r{i}.subst = {'_EMOTIONAL_A_P2'};
% i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_R_ADJUNCT';r{i}.subst = {'#empty'};
i=i+1;r{i}.wt=1; r{i}.match='_LOC_N_P1_B';r{i}.subst = {'_N_P0'};  


i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P2';r{i}.subst = {'_A_SPEC','_PHYSICAL_A_P1'}; 
%i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P2';r{i}.subst = {'_A_SPEC','_PHYSICAL_A_P1'}; 
i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'_INTENSIF'};
i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'#empty'};
%i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P1';r{i}.subst = {'_PHYSICAL_A_P0'}; 
i=i+1;r{i}.wt=1; r{i}.match='_PHYSICAL_A_P1';r{i}.subst = {'_PHYSICAL_A_P0'};

i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P2';r{i}.subst = {'_A_SPEC','_EMOTION_A_P1'}; 
% i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P2';r{i}.subst = {'_A_SPEC','_EMOTION_A_P1'};
% i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'_INTENSIF'};
% i=i+1;r{i}.wt=1; r{i}.match='_A_SPEC';r{i}.subst = {'#empty'};
% i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P1';r{i}.subst = {'_EMOTION_A_P0'}; 
i=i+1;r{i}.wt=1; r{i}.match='_EMOTION_A_P1';r{i}.subst = {'_EMOTION_A_P0'}; 


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
i=i+1;r{i}.wt=1; r{i}.match='_OBJ_N_P1';r{i}.subst = {'_N_P0','_N_R_ADJUNCT'}; 


%%% terminals
i=i+1;r{i}.wt=1; r{i}.match='_INTENSIF';r{i}.subst = {'très'};

% 'random' sentences could be detemrined by generating random assignments of values in SentInfo feeding into GenerateSentence.m      
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'un'};r{i}.addi={{'$INDEFINITE','$SINGULAR'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'quelques'};r{i}.addi={{'$INDEFINITE','$PLURAL'}};  
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'le'};r{i}.addi={{'$DEFINITE'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'ce'};r{i}.addi={{'$DEMONSTRATIVE','$SINGULAR','$CLOSE_TO_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'ce'};r{i}.addi={{'$DEMONSTRATIVE','$SINGULAR','$FAR_FROM_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'ces'};r{i}.addi={{'$DEMONSTRATIVE','$PLURAL','$CLOSE_TO_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'ces'};r{i}.addi={{'$DEMONSTRATIVE','$PLURAL','$FAR_FROM_SPEAKER'}};     
i=i+1;r{i}.wt=1; r{i}.match='_D_P0';r{i}.subst = {'#empty'}; r{i}.addi={{'$INDEFINITE','$NUMBER_GIVEN'}}; 

% NOTE: for the Neurosyntax 2.0 for purposes of prespecifying a sentence length ahead of time, we need to keep track of which tenses in each language require an added auxilary verb    
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#future'};   r{i}.addi={{'$AUX_NO'}};
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#perfect'};  r{i}.addi={{'$AUX_YES'}};
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#present'};  r{i}.addi={{'$AUX_NO'}};  
i=i+1;r{i}.wt=1; r{i}.match='_T_P0';r{i}.subst = {'#past'};     r{i}.addi={{'$AUX_NO'}}; % for French, this is the imperfect     

i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'un'};r{i}.addi={{'$SINGULAR'}}; % Will never be called if NoNumsForSingularNouns is set to be 1                       
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'deux'};r{i}.addi={{'$PLURAL','$NUMEROSITY_LOW'}};      
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'trois'};r{i}.addi={{'$PLURAL','$NUMEROSITY_LOW'}};    
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'cinquante'};r{i}.addi={{'$PLURAL','$NUMEROSITY_HIGH'}};   
i=i+1;r{i}.wt=1; r{i}.match='_NUM';r{i}.subst = {'soixante'};r{i}.addi={{'$PLURAL','$NUMEROSITY_HIGH'}};  


i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'sur'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'dans'};
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'devant'}; r{i}.lab='ANIMATE_P';   % we use lab not addi here, bc we dont want this property propogating to all other words lower in the
i=i+1;r{i}.wt=1; r{i}.match='_P_P0';r{i}.subst = {'derrière'}; r{i}.lab='ANIMATE_P';   % we use lab not addi here, bc we dont want this property propogating to all other words lower in the       
