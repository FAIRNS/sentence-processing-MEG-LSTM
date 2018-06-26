function [outfile,Counts,wordusecount,TotRemCounts,ProbeFromToCounts] = StimulusGeneration(savedir,language,nsentences,BlockType,Counts,wordusecount,TotRemCounts,ProbeFromToCounts,WMForMain)
%%%% Generation of simple, controlled sentence stimuli
%
%%%  Counts,wordusecount,TotRemCounts are output because these accrue over instances of calling this function and need to be accounted for      

%global language

if nargin < 9 || isempty(WMForMain);       WMForMain=false;        end
if nargin<5
    Counts=[];
    TotRemCounts=[];
end
if nargin<4 || isempty(BlockType)
    BlockType=2;    % Main    
end
% fs_Stim=36;

% clear
% ProbeFromToCounts=[];
% Counts=[];
% wordusecount=[];
% TotRemCounts=[];
% nsentences= 40;
% language=1;     %1=English; 2=French; 3=Dutch; 4=Spanish        
% BlockType=1;

tic

% default is the main task block   
LocalizerFlag=0;
JabberFlag=0;
switch BlockType
    case 1 
        disp('Generating Localizer block stimuli') 
        LocalizerFlag=1;
        Addstr='_Loc';
    case 2
        disp('Generating Main sentence block stimuli')
        
        AllowLexSwitch=1;   % for 'Diff' probe sentences   
        Addstr='_Main';
    case 3
        disp('Generating Jabberwocky block stimuli')
        JabberFlag=1;
        
        AllowLexSwitch=0;   % for 'Diff' probe sentences   
        Addstr='_Jab';
end

DisplayEachSent=0;  %%%%%%%%%%%%  
DisplayShortenedDiff=0; 
DisplayEachSentTree=0;
DisplayReadableSentAtEnd=0; %%%%%%%%
PlotSentLenHists=0;  

DoPostHocCheck=0;


% NeuroSyntax 2.0 options  
CapFirstWord=1;

LocSentLenLims=[4 8];

TurnOffPPs=true;
LimSenLength=true;      % a boolean
MaxWordLim=13;
SentTypeRates=[1/8 1/8 1/4 1/6 1/6 1/6]';  % notethecode assumes taht the first 3fracs sum to 1/2, andtehlast 3fracs sum to 1/2 to maintain balancing of Trans and InTrans verbs                 
NoNumsForSingularNouns=1;   %1 or 0     
MaxOneVeryPerSentence=1;    %1 or 0
NumUseRate=2/3;             %fraction of NPs where nums are possible (ie not NPs in the PP, and (possibly) not singular NPs) that get chosen to have a Num     
PairNumsAndLongNPs=1;       % boolean. useful for creating a some long individual NPs for the node-closing verification analysis    
%nAPwordRates=[9/16 2/16 5/16]';           % numbers correspond to [0 1 2] words in the AP, where AP applies to both Adj and Adv phrases      
nAPwordRates=[1/2 1/4 1/4]';           % numbers correspond to [0 1 2] words in the AP, where AP applies to both Adj and Adv phrases      

SameToDiffRate=.5;          % for probe .... Make the 1/2 for the non-passive case
UseAllPronounsRate=2/3;     % for probe 'Same' sentences
GrammOrLexChangeRate=1/2;   % for probe 'Diff' sentences
AllowAnimacySwitch=1;       % 1 or 0 for whether or not to allow for a switch from it to he/she or vice versa      
GenChangeRate=1/2;          % prop for Gen for probe 'Diff' sentences when Gender switches are possible... the balance including the other two options sum to 1, which are only on certain sentences (with singular animate NPs)  
NumTenseChangeRate=1/2;     % prop for Num for probe 'Diff' sentences when Gender switches are not possible
DiffKeepNPRate=1/4;         % for probe 'Diff' sentences
VerbEllipsisRate=1/2;       % only applied to intransitive verbs when there is no lexicla change of the verb    
ProbeElideAdv=1;            % 1 or 0
MaxOneVeryPerSentence=1;

% describe Verb Tense switches to avoid   
VerbTenseSwitchesToAvoid=zeros(4,4);
VerbTenseSwitchesToAvoid(2,4)=1;    % don't switch between past and present perfect tenses ... too similar   
VerbTenseSwitchesToAvoid(4,2)=1;
VerbTenseSwitchesToAvoid(1,3)=0;    % don't switch between present and future tenses ... too similar   
VerbTenseSwitchesToAvoid(3,1)=0;

LexSwitchAcrossMajorCat=0;  % if 1, it will allow switches form say "small" to "happy"; else the cetrogry will be retsicted to be the same subtype of word (ie physical adjectives) of different semantic valence. For example "small" to "large" would be enforced    

%%%%%%%%%%%%%%%%%% End of User Inputs        

%clear Counts RemCounts wordusecount ProbeDiffCounts SentInfo

%%% load the substitution rules
LoadRules
LoadRuleLists;      % loads rmatchlist, rwtlist, istermword
SetLexSwitchTargs;

% init everything else
[deepstructure, surface, shortened]=deal( cell(nsentences,1) );
if isempty(Counts)
    InitCounts;     % creates the variables Counts, wordusecount,
end
InitRemCounts;  % creates the variable RemCounts
curSentType=0;

if LimSenLength
    MinFullSenLength=9;             % Determined by hand, but not a user input. This applies to sentTypes 1 and 2... this is the number of words without any numbers, adjective or adverbs    
    nAddedAllowed=MaxWordLim-MinFullSenLength;
end
    
if LocalizerFlag
    nsentences=nsentences/2;        % half will be word-lists, half will be sentences      
    SentLenLims=LocSentLenLims;
    SetSentLens    
    Loc.SentLens=SentLens;
    InitLocCounts
end


outfile = [ 'GeneratedSentences' Addstr sprintf('_%d',fix(clock)) '.mat' ];
tic
for isent = 1:nsentences
    disp(isent)        
    
    if LocalizerFlag
        GenSentInfo_Loc
    else
        % generate senttypes systematically in order... we'll then scramble the order of stimuli presentation later
        % check if we're swicthing sentence types
        if curSentType==0 || RemCounts.SentTypes( curSentType )==0
            curSentType=curSentType+1;
            %curSentType=2;
            AdjSentTypeRuleWts % adjusts rwtlist for current sent type
        end
        GenSentInfo
        GenSentInfo_probe
    end

    
    %%%% create the deep structure from simplified X-bar theory
    [deepstructure{isent},wordusecount,Counts] = GenerateSentence( r,SentInfo(isent),rmatchlist,rwtlist,wordusecount,Counts,istermword );

    % Could do other semantic clean-up here...   
    % Asjust the choise of prepositions based on other items in the sentencs      
    [deepstructure{isent},wordusecount]=RechoosePrep(deepstructure{isent},wordusecount,SentInfo(isent),curSentType,r,rmatchlist);
    
    % check for incompatibility of slowly       
    [deepstructure{isent},wordusecount]=RechooseAdv(deepstructure{isent},wordusecount,r,rmatchlist);

    % feature compatibility check       
    [deepstructure{isent},wordusecount]=CompatibilityCheck(deepstructure{isent},wordusecount,r);
    
    % check for appropriate specificity if the PP_NP and Subj NP are both animate... bc "near the actresses the woman met the man" is a bit weird          
    if SentInfo(isent).AnimSubj && ~isempty(SentInfo(isent).AnimPP_NP) && SentInfo(isent).AnimPP_NP
        [deepstructure{isent},wordusecount]=SpecificityCheck(deepstructure{isent},wordusecount);
    end
    
    %%% from the deep structure, create the final surface structure, arrange the plurals etc
    surface{isent} = DeepToSurface(language,deepstructure{isent});    
    
    if DisplayEachSent
        DisplaySentenceWithLabels(surface{isent},1,{});
    end
    if DisplayEachSentTree
        figure(31);clf;DisplayTree(surface{isent},1);
    end

%     Loc.SentLens(isent)
%     SentInfo(isent).nToAdd
%     DisplaySentenceWithLabels(surface{isent},1,{});
            
    %%% from the surface structure, substitute items to get a shortened version   
    if LocalizerFlag || WMForMain
        % program the shortened probe words later when you have the giant wordlist... for now just copy the surface structure      
        shortened{isent}=surface{isent};   
    else
        if SentInfo(isent).Probe.SameOrDiff==2  &&  SentInfo(isent).Probe.Diff_GrammOrLexChange==2
            [shortened{isent}, ProbeFromToCounts] = Substitute(language,surface{isent}, SentInfo(isent).Probe, r, ProbeFromToCounts); %we need to also pass the rules if we have a lexical change
        else
            [shortened{isent}, ProbeFromToCounts] = Substitute(language,surface{isent}, SentInfo(isent).Probe, [], ProbeFromToCounts);
        end
        
        if DisplayEachSent
            disp('********** SHORTENED VERSION **************');
            if DisplayShortenedDiff
                PrintShortenedType(SentInfo(isent).Probe);
            end
            %SentInfo(isent).Probe
            DisplaySentenceWithLabels(shortened{isent},1,{});
        end
        if DisplayEachSentTree
            figure(32);clf;DisplayTree(shortened{isent},1);
        end       
        
        %counts are the number of stimuli of a particular type yet to be generated
        RemCounts.SentTypes( curSentType )= RemCounts.SentTypes( curSentType )-1;
    end
end

if LocalizerFlag || WMForMain
    CalcWordList
    GenLocProbes
    if LocalizerFlag 
        SetControlBlockStimuli
        IntersperseLocTrials
    end
    
    if DisplayReadableSentAtEnd
        PrintSentences_WordList;
    end
else        
    % loop to avoid repeats of content words in consecutive sentences
    disp(['arranging stimulus order'])   
    trialorder = randperm(nsentences);
    
    isent=1;
    RemList=[];
    while isent<length(trialorder)
        while ContentWordRepeatCheck( language,deepstructure{trialorder(isent)},deepstructure{trialorder(isent+1)},[],JabberFlag );
            RemList=[RemList trialorder(isent+1)];
            trialorder(isent+1)=[];
            if length(trialorder)==isent;
                break
            end
        end
        isent=isent+1;
    end
    
    % now go through RemList and Add those back to trialorder if they pass the check
    for iRem=1:length(RemList)
        isent=1;
        if ~ContentWordRepeatCheck( language,surface{ RemList(iRem) },surface{trialorder(isent)},[],JabberFlag );
            trialorder=[RemList(iRem) trialorder]; % put this sent at the beginning
        else
            isent=isent+1;
            while isent<length(trialorder) && ContentWordRepeatCheck( language,deepstructure{ RemList(iRem) },deepstructure{trialorder(isent)},deepstructure{trialorder(isent+1)},JabberFlag )
                isent=isent+1;
            end
            if isent == length(trialorder)
                if ~ContentWordRepeatCheck( language,deepstructure{ RemList(iRem) },deepstructure{trialorder(isent)},[],JabberFlag );
                    trialorder=[trialorder RemList(iRem)];      % here it fits only after the last trial
                else
                    warning('Trouble avoiding a repeat of content words when shuffling trial order!!!')
                    trialorder=[trialorder RemList(iRem)];  % put it at the end even with the repeat
                end
            else
                % put this sent bt isent and isent+1
                trialorder=[trialorder(1:isent)  RemList(iRem)  trialorder(isent+1:end);];
            end
        end
    end
        
    SentInfo=SentInfo(trialorder);
    deepstructure=deepstructure(trialorder);
    surface=surface(trialorder);
    shortened=shortened(trialorder);
    
    CalcWordList; % sets variables wordlist and nodelist
    
    % get samestruct
    samestruct=zeros(nsentences,1);
    for isent=1:nsentences
        samestruct(isent)=SentInfo(isent).Probe.SameOrDiff==1;
    end
    
    if DisplayReadableSentAtEnd
        PrintSentences;
    end
    
    if DoPostHocCheck
        PostHocCount
    end
end

toc

save([savedir filesep outfile],'-mat');  %%% save everything including the rules and vocabulary

