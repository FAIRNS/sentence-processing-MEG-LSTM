function [outfile,Counts,wordusecount,TotRemCounts,ProbeFromToCounts] = StimulusGeneration_PassiveStimuli2(savedir,language,nsentences,BlockType,Counts,wordusecount,TotRemCounts,ProbeFromToCounts)
%%%% Generation of simple, controlled sentence stimuli
%
%%% Counts,wordusecount,TotRemCounts keep track of the counts of various 
%%% things that are balanced across trials. They are sent as outputs because 
%%% these accrue over instances of calling this function and need to be accounted for

%global language

if nargin<5
    Counts=[];
    TotRemCounts=[];
end
if nargin<4 || isempty(BlockType)
    BlockType=2;    % Main
end
fs_Stim=36;    % Font size. This value will be applied to each trial in the ouput of this program. 
               % Code downstream of this to present the stimuli will look to this value per trial when presenting the stimuli.
               % Code within this program could thus be written to change
               % the font-size on every trial if needed, though for now
               % we'll keep it the same for every trial.
               
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

%%% Display options to read-out each sentence during stimuli generation; mainly useful for debugging.    
DisplayEachSent=0;  %%%%%%%%%%%%
DisplayShortenedDiff=0;
DisplayEachSentTree=0;
DisplayReadableSentAtEnd=0; %%%%%%%%
PlotSentLenHists=0;

DoPostHocCheck=0;


%%% NeuroSyntax 2.0 options
% new options just for the passive version     
if ~LocalizerFlag;      CapFirstWord=1;         else      CapFirstWord=0;      end  % When CapFirstWord==1 the code capitalizes the first word of each sentence     
nPressTrsToGen=round(nsentences/10);    % The number of Press trials to insert into the block being generated.     
nPressFlashes=3;                        % Number of times to show PressStr in a "Press" trial    
PressStr='press';                       % The actual Press string the subject receives as a word     

% other options
LocSentLenLims=[4 8];       % The minimum and maximum sentence lengths for the Localizer block    

TurnOffPPs=false;       % true or false to include (or exclude) PPs
LimSenLength=true;      % true or false to limit the maximum sententce length   
MaxWordLim=13;          % if above is true, this is the maximum sentence length     
SentTypeRates=[1/8 1/8 1/4 1/6 1/6 1/6]';  % The proportion of each of the 6 sentence types to generate.
                                           % NOTE: the first 3 fracs and the last 3 numbers here both have to sum to 1/2 to maintain balancing of Trans and InTrans verbs     
NoNumsForSingularNouns=1;   % If set to 0, it allows for a sentence like "One man polished the truck", i.e. the number "one" for the singular "man"    
MaxOneVeryPerSentence=1;    % If set to 0, "very" could be added to any NP or VP in a sentence. e.g. it coudl generate the sentence "a very happy man very quickly met the very sad woman". Set this to 1 to ensure that "very" only shows up once in the sentence
NumUseRate=2/3;             % Fraction of NPs where nums could be added (e.g. "two","three") are possible 
PairNumsAndLongNPs=1;       % boolean. useful for creating a some long individual NPs for the node-closing verification analysis
nAPwordRates=[1/2 1/4 1/4]';           % numbers correspond to [0 1 2] words in the AP, where AP applies to both Adj and Adv phrases
                            % [9/16 2/16 5/16]'   

% Options for the probe senteces                               
SameToDiffRate=1;           % The fraction of "Same" vs. "Different" probe sentences ...
UseAllPronounsRate=2/3;     % for probe 'Same' sentences
GrammOrLexChangeRate=1/2;   % for probe 'Diff' sentences... rtaios of grammatical vs a lexical difference introduced to the "Different" probe sentences     
AllowAnimacySwitch=1;       % 1 or 0 for whether or not to allow for a switch from it to he/she or vice versa
GenChangeRate=1/2;          % prop for Gender changes for probe 'Diff' sentences when Gender switches are possible... the balance including the other two options sum to 1, which are only on certain sentences (with singular animate NPs)
NumTenseChangeRate=1/2;     % prop for Num for probe 'Diff' sentences when Gender switches are not possible
DiffKeepNPRate=1/4;         % for probe 'Diff' sentences
VerbEllipsisRate=1/2;       % only applied to intransitive verbs when there is no lexicla change of the verb
ProbeElideAdv=1;            % 1 or 0

% describe Verb Tense switches to avoid (for probe sentence creation
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
    MinFullSenLength=9;     % Determined by hand, but not a user input. This applies to sentTypes 1 and 2... this is the number of words without any numbers, adjective or adverbs
    nAddedAllowed=MaxWordLim-MinFullSenLength;
end

if LocalizerFlag
    nsentences=nsentences/2;    % half will be word-lists, half will be sentences
    SentLenLims=LocSentLenLims;
    SetSentLens
    Loc.SentLens=SentLens;
    InitLocCounts
else
    % nsentences=nsentences+nPressTrsToGen;
    
    %%% ensure no two PressTrs in a row   
    NotGood=1;
    while NotGood
        PressTrInds=randperm(nsentences,nPressTrsToGen);
        NotGood=0;
        for in=1:length(PressTrInds)-1
            dists=abs(PressTrInds-PressTrInds(in));
            if any( dists==1 )
                NotGood=1;
                break
            end
        end
    end
end


outfile = [ 'GeneratedSentences' Addstr sprintf('_%d',fix(clock)) '.mat' ];
tic
for isent = 1:nsentences
    disp(isent)
    
    if LocalizerFlag
        GenSentInfo_Loc
    else
        if ismember(isent,PressTrInds)
            % store all the count variables, then set them back as they were after we've generated the Press trial
            wordusecount_Sav=wordusecount;
            Counts_Sav=Counts;
            ProbeFromToCounts_Sav=ProbeFromToCounts;
            RemCounts_Sav=RemCounts;
            rwtlist_Sav=rwtlist;
        end
        
        % generate senttypes systematically in order... we'll then scramble the order of stimuli presentation later
        % check if we're swicthing sentence types
        if curSentType==0 || RemCounts.SentTypes( curSentType )==0
            curSentType=curSentType+1;            
        end
        AdjSentTypeRuleWts % adjusts rwtlist for current sent type

        GenSentInfo
        GenSentInfo_probe
    end
       
    
    %%%% create the deep structure from simplified X-bar theory
    [deepstructure{isent},wordusecount,Counts] = GenerateSentence( r,SentInfo(isent),rmatchlist,rwtlist,wordusecount,Counts,istermword );
    if DisplayEachSentTree
        figure(30);clf;DisplayTree(deepstructure{isent},1);
        SentInfo(isent)
    end
    
    % Could do other semantic clean-up here...
    if language==1
        % Adjust the choise of prepositions based on other items in the sentencs
        [deepstructure{isent},wordusecount]=RechoosePrep(deepstructure{isent},wordusecount,SentInfo(isent),curSentType,r,rmatchlist);
    end
    
    % check for incompatibility of slowly
    [deepstructure{isent},wordusecount]=RechooseAdv(deepstructure{isent},wordusecount,r,rmatchlist,language);
    
    % feature compatibility check
    [deepstructure{isent},wordusecount]=CompatibilityCheck(deepstructure{isent},wordusecount,r);
    
    % check for appropriate specificity if the PP_NP and Subj NP are both animate... bc "near the actresses the woman met the man" is a bit weird
    if SentInfo(isent).AnimSubj && isfield(SentInfo,'AnimPP_NP') && ~isempty(SentInfo(isent).AnimPP_NP) && SentInfo(isent).AnimPP_NP
        [deepstructure{isent},wordusecount]=SpecificityCheck(deepstructure{isent},wordusecount);
    end
    
    %%% from the deep structure, create the final surface structure, arrange the plurals etc
    surface{isent} = DeepToSurface(language,deepstructure{isent});
    
    if DisplayEachSent
        DisplaySentenceWithLabels(surface{isent},1,{});
    end
    if DisplayEachSentTree
        figure(31); clf; DisplayTree(surface{isent},1);
    end
    
    %     Loc.SentLens(isent)
    %     SentInfo(isent).nToAdd
    %     DisplaySentenceWithLabels(surface{isent},1,{});
    
    %%% from the surface structure, substitute items to get a shortened version
    if LocalizerFlag
        % program the shortened probe words later when you have the giant wordlist... for now just copy the surface structure
        shortened{isent}=surface{isent};
    else
        %counts are the number of stimuli of a particular type yet to be generated
        RemCounts.SentTypes( curSentType )= RemCounts.SentTypes( curSentType )-1;
        
        % code to turn off the probe sentence generation for French because that has not been written yet         
        if language~=2
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
            
            if ismember(isent,PressTrInds)
                % reset all the count variables to what they were before we generated this sentence
                wordusecount=wordusecount_Sav;
                Counts=Counts_Sav;
                ProbeFromToCounts=ProbeFromToCounts_Sav;
                RemCounts=RemCounts_Sav;
                rwtlist=rwtlist_Sav;
            end
        end
    end
end

if LocalizerFlag
    CalcWordList
    GenLocProbes
    SetControlBlockStimuli
    IntersperseLocTrials
    
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

