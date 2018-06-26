% StimulusGeneration_PassiveStimuli.m 

nsentences=nsent_PerBl;

tic

% default is the main task block   
JabberFlag=0;
LocalizerFlag=0;

switch BlockType
    case 1 
        disp('Generating Localizer block stimuli') 
        LocalizerFlag=1;
        nsentences=nsent_PerLocBl;
        
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



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
    if LocalizerFlag
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

