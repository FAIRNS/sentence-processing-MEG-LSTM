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
i=i+1;r{i}.match='_T_P2';r{i}.subst = {'_T_SPEC','_T_P1'}; %% allow up to two TPs in the stimuli
%i=i+1;r{i}.match='_T_P1';r{i}.subst = {'_T_L_ADJUNCT','_T_P1'}; 
%i=i+1;r{i}.match='_T_P1';r{i}.subst = {'_T_P1','_T_R_ADJUNCT',}; 
i=i+1;r{i}.match='_T_P1';r{i}.subst = {'_T_P0','_T_COMP'}; 
i=i+1;r{i}.match='_T_P1';r{i}.subst = {'_T_P0','_T_COMP'}; 

i=i+1;r{i}.match='_N_P2';r{i}.subst = {'_N_SPEC','_N_P1'}; 
i=i+1;r{i}.match='_N_P2';r{i}.subst = {'_N_SPEC','_N_P1'}; %% allow up to two NPs in the sentence
i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_N_L_ADJUNCT','_N_P1'}; 
i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_N_P1','_N_R_ADJUNCT',}; 
i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_HUMAN_N_P0'};  %%% different sorts of Nouns, allowing for complements or not
i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_HUMAN_N_P0'};  %%% different sorts of Nouns, allowing for complements or not
i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_ROLE_N_P0'}; 

i=i+1;r{i}.match='_V_P2';r{i}.subst = {'_V_SPEC','_V_P1'}; 
i=i+1;r{i}.match='_V_P2';r{i}.subst = {'_V_SPEC','_V_P1'}; %%% allow up to two VPs, e.g. a relative sentence
i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1'}; 
i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1'};%% repeated to increase its frequency 
i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VT_V_P1'}; 
i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VI_V_P1'}; 
i=i+1;r{i}.match='_VT_V_P1';r{i}.subst = {'_VT_V_P0','_VT_COMP',}; %% different sorts of verbs take different sorts of complements
i=i+1;r{i}.match='_VM_V_P1';r{i}.subst = {'_VM_V_P0','_VM_COMP',}; 
i=i+1;r{i}.match='_VI_V_P1';r{i}.subst = {'_VI_V_P0'}; 

if maxlength>7 %%% simpler rules (without PP) if the sentences need to be short
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VM_V_P1'};
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VM_V_P1'};
    i=i+1;r{i}.match='_N_P1';r{i}.subst = {'_ROLE_N_P0','_N_COMP',}; %%
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1'};
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_V_L_ADJUNCT','_V_P1'};
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VT_V_P1','_V_R_ADJUNCT',};
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_VI_V_P1','_V_R_ADJUNCT',};
    i=i+1;r{i}.match='_V_R_ADJUNCT';r{i}.subst = {'_P_P2'}; %%%% uncomment to include some PPs
end



% i=i+1;r{i}.match='_A_P2';r{i}.subst = {'_A_SPEC','_A_P1'}; 
% i=i+1;r{i}.match='_A_P2';r{i}.subst = {'_A_SPEC','_A_P1'}; 
% %i=i+1;r{i}.match='_A_P1';r{i}.subst = {'_A_L_ADJUNCT','_A_P1'}; 
% %i=i+1;r{i}.match='_A_P1';r{i}.subst = {'_A_P1','_A_R_ADJUNCT',}; 
% i=i+1;r{i}.match='_A_P1';r{i}.subst = {'_A_P0'}; % no complementizer for adjectives that qualify nouns
% i=i+1;r{i}.match='_A_P1';r{i}.subst = {'_A_P0'}; % no complementizer for adjectives that qualify nouns

i=i+1;r{i}.match='_P_P2';r{i}.subst = {'_P_SPEC','_P_P1'}; 
%i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_L_ADJUNCT','_P_P1'}; 
%i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_P1','_P_R_ADJUNCT',}; 
i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_P0','_P_COMP',}; 

i=i+1;r{i}.match='_P_P2';r{i}.subst = {'_CITY_P_P1'}; 
%i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_L_ADJUNCT','_P_P1'}; 
%i=i+1;r{i}.match='_P_P1';r{i}.subst = {'_P_P1','_P_R_ADJUNCT',}; 
i=i+1;r{i}.match='_CITY_P_P1';r{i}.subst = {'en_P_P0','_CITY_P_COMP',}; 

%%% more specific determination of possible SPECs, _ADJUNCTS and COMPs

i=i+1;r{i}.match='_T_SPEC';r{i}.subst = {'_N_P2'};r{i}.addi={{'$NOMINATIVE'}};
i=i+1;r{i}.match='_T_SPEC';r{i}.subst = {'_N_P2'};r{i}.addi={{'$NOMINATIVE'}};%%% allow up to two TPs in the sentence
i=i+1;r{i}.match='_N_SPEC';r{i}.subst = {'_DET'};
i=i+1;r{i}.match='_N_SPEC';r{i}.subst = {'_NUM'};
i=i+1;r{i}.match='_V_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.match='_V_SPEC';r{i}.subst = {'#empty'};
i=i+1;r{i}.match='_V_SPEC';r{i}.subst = {'#empty'}; %% duplicated to allow multiple TPs
i=i+1;r{i}.match='_A_SPEC';r{i}.subst = {'_DEGREE'};
i=i+1;r{i}.match='_P_SPEC';r{i}.subst = {'_INTENSIF'};

i=i+1;r{i}.match='_N_L_ADJUNCT';r{i}.subst = {'_PHYSICAL_A_P2'};
i=i+1;r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_EMOTION_A_P2'};
%i=i+1;r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'_P_P2'};
%i=i+1;r{i}.match='_N_R_ADJUNCT';r{i}.subst = {'qui','_T_P1'};
i=i+1;r{i}.match='_V_L_ADJUNCT';r{i}.subst = {'_ADV'};

i=i+1;r{i}.match='_T_COMP';r{i}.subst = {'_V_P2'};
i=i+1;r{i}.match='_T_COMP';r{i}.subst = {'_V_P2'};
i=i+1;r{i}.match='_N_COMP';r{i}.subst = {'de_P','_PROPER'};r{i}.addi={{''},{'$GENITIVE'}};
i=i+1;r{i}.match='_VT_COMP';r{i}.subst = {'_N_P2'};r{i}.addi={{'$ACCUSATIVE'}};
i=i+1;r{i}.match='_VM_COMP';r{i}.subst = {'_INF_T_P2'};
i=i+1;r{i}.match='_INF_T_P2';r{i}.subst = {'_INF_T_SPEC','_INF_T_P1'};
i=i+1;r{i}.match='_INF_T_SPEC';r{i}.subst = {'#PRO'};
i=i+1;r{i}.match='_INF_T_P1';r{i}.subst = {'_INF_T_P0','_V_P2'}; %r{i}.addi={{''},{'$INFINITIVE'}};
i=i+1;r{i}.match='_INF_T_P0';r{i}.subst = {'#inf'};
%i=i+1;r{i}.match='_VM_COMP';r{i}.subst = {'qui','_CLAUSE'};
%i=i+1;r{i}.match='_A_COMP';r{i}.subst = {'de_P','_N_P2'};r{i}.addi={{''},{'$GENITIVE'}}; %%% only for predicates
%% suppressed in French, because it creates many problems with "de le", "de les" etc.
%i=i+1;r{i}.match='_A_COMP';r{i}.subst = {'de_P','_PROPER'};r{i}.addi={{''},{'$GENITIVE'}}; %%% only for predicates
i=i+1;r{i}.match='_A_COMP';r{i}.subst = {'de_P','_INF_T_P2'};
%OLDSTUFF i=i+1;r{i}.match='_to_T_P2';r{i}.subst = {'_to_T_SPEC','_to_T_P1'}; 
%i=i+1;r{i}.match='_to_T_SPEC';r{i}.subst = {'#emptysubj'};
%i=i+1;r{i}.match='_to_T_P1';r{i}.subst = {'to_T_P0','_T_COMP'}; 

i=i+1;r{i}.match='_P_COMP';r{i}.subst = {'_LOC_N_P2'}; %% simplified location PP
%i=i+1;r{i}.match='_LOC_N_P2';r{i}.subst = {'el_DET','_LOCN'}; %% simplified location PP 
i=i+1;r{i}.match='_LOC_N_P2';r{i}.subst = {'el_DET','_LOC_N_P0'}; %% simplified location PP

%%% special case of proper names
i=i+1;r{i}.match='_N_P2';r{i}.subst = {'_PROPER'}; 


if maxlength>7 %%% simpler rules (without PP) if the sentences need to be short
    %%% special case of TO BE + predicate
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_BE_2_V_P0','_EMOTION_A_P2'};
    i=i+1;r{i}.match='_EMOTION_A_P2';r{i}.subst = {'_A_SPEC','_EMOTION_A_P1'};
    i=i+1;r{i}.match='_EMOTION_A_P1';r{i}.subst = {'_EMOTION_A_P0','_A_COMP'};
    i=i+1;r{i}.match='_EMOTION_A_P1';r{i}.subst = {'_EMOTION_A_P0'};
    i=i+1;r{i}.match='_V_P1';r{i}.subst = {'_BE_1_V_P0','_PHYSICAL_A_P2'};
    i=i+1;r{i}.match='_PHYSICAL_A_P2';r{i}.subst = {'_A_SPEC','_PHYSICAL_A_P1'};
    i=i+1;r{i}.match='_PHYSICAL_A_P1';r{i}.subst = {'_PHYSICAL_A_P0'};
    i=i+1;r{i}.match='_A_P0';r{i}.subst = {'_PHYSICAL_A_P0'};
end

%i=i+1;r{i}.match='';r{i}.subst = {''};

%%% word categories

i=i+1;r{i}.match='_A_P0';r{i}.subst = {'_EMOTION_A_P0'};
i=i+1;r{i}.match='_A_P0';r{i}.subst = {'_PHYSICAL_A_P0'};

%%% terminals
%%% words are frequent and short (max 8 letters, usually much less)

i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'#empty'}; %% intensifiers can be omitted
i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'#empty'}; %% intensifiers can be omitted
if maxlength>7
%    i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'exactamente'}; %ESP?:exactamente
    i=i+1;r{i}.match='_INTENSIF';r{i}.subst = {'justo'};
end

i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'#empty'}; %%% degrees can be omitted
i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'#empty'}; %%% degrees can be omitted
i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'#empty'}; %%% degrees can be omitted
if maxlength>7
    i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'muy'}; %%% %ESP:muy
    i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'realmente'}; %ESP:realmente
    i=i+1;r{i}.match='_DEGREE';r{i}.subst = {'bastante'};%ESP:bastante
end

%i=i+1;r{i}.match='_ADV';r{i}.subst = {'frecuentemente'};  %ESP:frecuentemente
i=i+1;r{i}.match='_ADV';r{i}.subst = {'a','menudo'};  
%i=i+1;r{i}.match='_ADV';r{i}.subst = {'mucho'};  %%% raises problems because it must be placed after the verb (but between the verb and the following "a"
i=i+1;r{i}.match='_ADV';r{i}.subst = {'siempre'}; %ESP:siempre
i=i+1;r{i}.match='_ADV';r{i}.subst = {'también'}; %ESP:tambien
i=i+1;r{i}.match='_ADV';r{i}.subst = {'a','veces'};  %ESP?:a veces

%%% for verbs, we always put the infinitive form
%%%% ATTENTION !! FRENCH VERBS should not start with a vowel, for fear of d' (apostrophe)
%%% and the first two categories of verbs should be "voluntary" action verbs
%%% (replaceable by "faire") %ESP?:unclear

i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'dormir'}; %ESP:dormir
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'cantar'};%ESP:cantar
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'llorar'}; %ESP:llorar 
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'gritar'}; %ESP:gritar
i=i+1;r{i}.match='_VI_V_P0';r{i}.subst = {'trabajar'}; %ESP:trabajar

i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'atacar','a'}; %f?liciter %ESP:atacar 
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'encontrar','a'}; %ESP?: renuirse con, conocer
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'besar','a'}; % encourager %ESP:besar
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'golpear','a'}; %ESP:golpear
i=i+1;r{i}.match='_VT_V_P0';r{i}.subst = {'ayudar','a'}; %voir %ESP:ayudar

%i=i+1;r{i}.match='_VM_V_P0';r{i}.subst = {'aimer'}; %ESP?:
i=i+1;r{i}.match='_VM_V_P0';r{i}.subst = {'disfrutar'}; %ESP?:
i=i+1;r{i}.match='_VM_V_P0';r{i}.subst = {'preferir'}; %ESP:preferir
i=i+1;r{i}.match='_VM_V_P0';r{i}.subst = {'odiar'}; %ESP:odiar
i=i+1;r{i}.match='_VM_V_P0';r{i}.subst = {'querer'}; %ESP:querer

i=i+1;r{i}.match='_BE_1_V_P0';r{i}.subst = {'ser'}; %ESP?: ser/estar  %%% ser = definitional quality estar = temporary state
i=i+1;r{i}.match='_BE_2_V_P0';r{i}.subst = {'estar'}; %ESP?: ser/estar  %%% ser = definitional quality estar = temporary state

i=i+1;r{i}.match='_DET';r{i}.subst = {'los'}; r{i}.addi={{'$PLURAL'}}; %ESP?:los/las
i=i+1;r{i}.match='_DET';r{i}.subst = {'el'}; r{i}.addi={{'$SINGULAR'}};%%%% masculine or feminine will be determined by a special function %ESP:el/la
%i=i+1;r{i}.match='_DET';r{i}.subst = {'#empty'}; r{i}.addi={{'$PLURAL'}};
i=i+1;r{i}.match='_DET';r{i}.subst = {'un'}; r{i}.addi={{'$SINGULAR'}}; %ESP?:un/una
i=i+1;r{i}.match='_DET';r{i}.subst = {'estos'}; r{i}.addi={{'$PLURAL'}}; %ESP?:estos/estas
i=i+1;r{i}.match='_DET';r{i}.subst = {'este'}; r{i}.addi={{'$SINGULAR'}}; %ESP?:este/esta

i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#future'};
%i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#perfect'}; %% perfect has a
%distinct, implausible meaning of "achievement" in Spanish -->  deleted
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#present'};  
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#past'};
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#might'};
i=i+1;r{i}.match='_T_P0';r{i}.subst = {'#should'};

i=i+1;r{i}.match='_NUM';r{i}.subst = {'dos'};r{i}.addi={{'$PLURAL'}}; %ESP:dos
i=i+1;r{i}.match='_NUM';r{i}.subst = {'cinco'};r{i}.addi={{'$PLURAL'}}; %ESP:cinco 
i=i+1;r{i}.match='_NUM';r{i}.subst = {'diez'};r{i}.addi={{'$PLURAL'}}; %ESP:diez 
i=i+1;r{i}.match='_NUM';r{i}.subst = {'once'};r{i}.addi={{'$PLURAL'}}; %ESP:once
i=i+1;r{i}.match='_NUM';r{i}.subst = {'algunos'};r{i}.addi={{'$PLURAL'}}; %ESP?:algunos/algunas

i=i+1;r{i}.match='_PROPER';r{i}.subst = {'Barack_FIRSTNAME','Obama_LASTNAME'};r{i}.addi={{'$SINGULAR','$MASC'},{'$SINGULAR','$MASC'}};
i=i+1;r{i}.match='_PROPER';r{i}.subst = {'Bill_FIRSTNAME','Gates_LASTNAME'};r{i}.addi={{'$SINGULAR','$MASC'},{'$SINGULAR','$MASC'}};
i=i+1;r{i}.match='_PROPER';r{i}.subst = {'George_FIRSTNAME','Bush_LASTNAME'};r{i}.addi={{'$SINGULAR','$MASC'},{'$SINGULAR','$MASC'}};
i=i+1;r{i}.match='_PROPER';r{i}.subst = {'John_FIRSTNAME','Lennon_LASTNAME'};r{i}.addi={{'$SINGULAR','$MASC'},{'$SINGULAR','$MASC'}};
i=i+1;r{i}.match='_PROPER';r{i}.subst = {'Marylin_FIRSTNAME','Monroe_LASTNAME'};r{i}.addi={{'$SINGULAR','$FEMI'},{'$SINGULAR','$FEMI'}};

% i=i+1;r{i}.match='_ANIMAL_N_P0';r{i}.subst = {'lion'};
% i=i+1;r{i}.match='_ANIMAL_N_P0';r{i}.subst = {'dog'};
% i=i+1;r{i}.match='_ANIMAL_N_P0';r{i}.subst = {'whale'};
% i=i+1;r{i}.match='_ANIMAL_N_P0';r{i}.subst = {'bird'};
% i=i+1;r{i}.match='_ANIMAL_N_P0';r{i}.subst = {'snake'};

%%%% ATTENTION pour ?viter le l' (apostrophe), les noms ne doivent pas
%%%% commencer par une voyelle
i=i+1;r{i}.match='_HUMAN_N_P0';r{i}.subst = {'médico'};r{i}.addi={{'$MASC'}}; %ESP?: enfermera/doctor/m?dico
i=i+1;r{i}.match='_HUMAN_N_P0';r{i}.subst = {'muchacho'};r{i}.addi={{'$MASC'}}; %ESP?:ni?o, muchacho
i=i+1;r{i}.match='_HUMAN_N_P0';r{i}.subst = {'diputado'};r{i}.addi={{'$MASC'}}; %ESP:diputado
i=i+1;r{i}.match='_HUMAN_N_P0';r{i}.subst = {'bailarina'};r{i}.addi={{'$FEMI'}}; %ESP:bailar?na
i=i+1;r{i}.match='_HUMAN_N_P0';r{i}.subst = {'mujer'};r{i}.addi={{'$FEMI'}}; %ESP?: mujer

i=i+1;r{i}.match='_ROLE_N_P0';r{i}.subst = {'competidor'};r{i}.addi={{'$MASC'}}; %ESP?:
i=i+1;r{i}.match='_ROLE_N_P0';r{i}.subst = {'profesor'};r{i}.addi={{'$MASC'}}; %ESP:profesor
i=i+1;r{i}.match='_ROLE_N_P0';r{i}.subst = {'fanático'};r{i}.addi={{'$MASC'}}; %ESP?: fan both genders / admirador / fan?tico
i=i+1;r{i}.match='_ROLE_N_P0';r{i}.subst = {'colega'};r{i}.addi={{'$MASC'}}; %ESP?: colega both genders
i=i+1;r{i}.match='_ROLE_N_P0';r{i}.subst = {'novia'};r{i}.addi={{'$FEMI'}}; %ESP?: amiga/novia

i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'triste'}; %%% all of these adjective can be followed by a complement "de + Infinitive or + ProperName" ESP?:
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'orgulloso'};  %ESP:orgulloso 
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'contento'}; %ESP:contento
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'asustado'}; %ESP:asustado
i=i+1;r{i}.match='_EMOTION_A_P0';r{i}.subst = {'preocupado'}; %ESP?:preocupado/inquieto

i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'amable'};%ESP?: amable o bueno
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'pequeño'};%ESP:peque?o
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'gordo'}; %ESP:gordo
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'alto'}; %ESP:alto
i=i+1;r{i}.match='_PHYSICAL_A_P0';r{i}.subst = {'curioso'}; %ESp?:curioso 

i=i+1;r{i}.match='_P_P0';r{i}.subst = {'sobre'};%ESP:sobre
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'bajo'}; %ESP:bajo
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'delante','de'}; %ESP?: delante de
i=i+1;r{i}.match='_P_P0';r{i}.subst = {'detrás','de'}; %ESP?: detr?s de

i=i+1;r{i}.match='_LOC_N_P0';r{i}.subst = {'puente'};r{i}.addi={{'$MASC'}}; %ESP:puente
i=i+1;r{i}.match='_LOC_N_P0';r{i}.subst = {'techo'};r{i}.addi={{'$MASC'}}; %ESP:techo 
i=i+1;r{i}.match='_LOC_N_P0';r{i}.subst = {'mesa'};r{i}.addi={{'$FEMI'}}; %ESP:mesa
i=i+1;r{i}.match='_LOC_N_P0';r{i}.subst = {'escenario'};r{i}.addi={{'$MASC'}}; %ESP?:escenario, male gender

i=i+1;r{i}.match='_CITY_P_COMP';r{i}.subst = {'New York'};
i=i+1;r{i}.match='_CITY_P_COMP';r{i}.subst = {'Paris'};
i=i+1;r{i}.match='_CITY_P_COMP';r{i}.subst = {'San Francisco'};
i=i+1;r{i}.match='_CITY_P_COMP';r{i}.subst = {'Tokyo'};
i=i+1;r{i}.match='_CITY_P_COMP';r{i}.subst = {'Dallas'};

%%i=i+1;r{i}.match='';r{i}.subst = {''};
