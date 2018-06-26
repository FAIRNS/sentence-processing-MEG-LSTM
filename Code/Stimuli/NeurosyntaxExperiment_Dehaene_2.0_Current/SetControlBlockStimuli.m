%SetControlBlockStimuli.m     

%%%%%%%%%%%%%%%%%%%%%  User Inputs
DisplaySentsAtEnd=0;

%  for makingsure we avoid the most common spurious constituents by limiting our choice of words based on the word immediately preceding it    
%                1           2           3           4         5          6        7         8        9           10  
%GrammCats = {'_N_P0',  '_VT_V_P0',  '_VI_V_P0',  '_A_P0',  '_ADV_P0',  '_D_P0',  '_T_P0',  '_NUM',  '_P_P0',  '_INTENSIF'};
DefGrammCats; % this script just executes the above line of code    
%DemonRootAdjust={'this','that','these','those'};    % fix these demonstratives to have a common root of 'this' (as they should have)                   
% DemonRootAdjust was incorporated into DefGrammCats above...      

% each column sums corresponds to what do for each previous state            
% these are all booleans, so not a proper Markov Matrix per se with columns summing to 1        
GrammCat_MarkovMat=[    1   0   1   0   1   0   1   0   1   1
                        0   0   0   1   0   1   0   1   1   1
                        0   0   0   1   0   1   0   1   1   1
                        1   0   1   0   0   0   1   0   1   0
                        0   0   0   1   1   0   0   1   1   0
                        1   0   1   1   0   1   0   1   0   1
                        0   1   1   1   0   1   1   1   1   1
                        1   0   0   1   1   0   1   1   0   1
                        0   1   0   1   1   1   1   1   1   1   
                        1   0   0   1   1   0   0   0   1   0
                   ];

VeryRatAdjust=1;   % adjust the ratio of "very" in the control block rel to what it should bc it appears too often in the main stimuli                 
%VTRatAdjust=1.4;    % increase the ratio of Trans verbs chosen by this procedure... put into the giant word list        

%%%%%%%%%%%%%%%%%%%%%  End of User Inputs

oldwordlist=wordlist;
oldrootlist=rootlist;
oldnodelist=nodelist;
oldsamestruct=samestruct;
SentLenLims=LocSentLenLims; %[4 8]; %uniform prob of a control list length between these limits    

%%% if lines below are commented, then this code will use the current wordlist in the space    
% disp('Select one of the existing data sets (''probably the most recent one'')');
% outfile = uigetfile('ExperimentalRun*.mat');
% %outfile='ExperimentalRun_2015_2_24_17_3_22.mat';
% load(outfile);
% ControlExperiment = true;


disp( 'Formulating control block stimuli from previous sentences' )   

nGrammCats=length(GrammCats);
CanFollowTypes=cell(nGrammCats,1);
for iGC=1:nGrammCats
    CanFollowTypes{iGC}=find(GrammCat_MarkovMat(:,iGC));
end

%%% set SentLens given the SentLenLims above  
SetSentLens
ntotwords_Ctrl=sum(SentLens);

CalcBigTermWordList


% this balances a reasonable proportion of the same words are chosen...  with some randomness in choosing the remainders      
% when choosing words to be in the control stimuli, we first choose those in this giantwordlist, then choose from the remainders only if no words are leftover in this list          
% choose words to keep in the giant word list based on the ratio of word counts for the control to the main block     
KeepRat=ntotwords_Ctrl/ntotwords;
giantwordlist_Inds=zeros( ntotwords_Ctrl,1 );
giantwordlist_Type=zeros( ntotwords_Ctrl,1 );
Remainderlist_Inds=zeros( ntotwords-ntotwords_Ctrl,1 );
Remainderlist_Type=zeros( ntotwords-ntotwords_Ctrl,1 );
c=0;
c2=0;
for itw=1:ntw
    if strcmp( TermWord.List{itw},'very' )
        RatAdjust= VeryRatAdjust;
    else
        RatAdjust= 1;
    end
    nKeep=round( RatAdjust*KeepRat*TermWord.Count(itw));
        
    if nKeep>0
        giantwordlist_Inds( c+1:c+nKeep )=itw;
        giantwordlist_Type( c+1:c+nKeep )=TermWord.FirstParentType(itw);
        c=c+nKeep;
    end
    % Assign to Remainder List   
    if nKeep<TermWord.Count(itw) % should essentially always be true   
        if strcmp( TermWord.List{itw},'very' )
            nRem=fix(VeryRatAdjust*TermWord.Count(itw))-nKeep;
        else
            nRem=TermWord.Count(itw)-nKeep;
        end        
        
        Remainderlist_Inds( c2+1:c2+nRem )=itw;
        Remainderlist_Type( c2+1:c2+nRem )=TermWord.FirstParentType(itw);
        c2=c2+nRem;
    end                
end

% adjust final sizes of RemainderList and giantwordlist    
Remainderlist_Inds=Remainderlist_Inds(1:c2);
Remainderlist_Type=Remainderlist_Type(1:c2);
if c>ntotwords_Ctrl
    %  below code is not necessary I think
    %     nExtra=c-ntotwords_Ctrl;
    %     SwitchInds=randi(c,[nExtra,1]);
    %
    %     Remainderlist_Inds=[Remainderlist_Inds; giantwordlist_Inds(SwitchInds)];
    %     Remainderlist_Type=[Remainderlist_Type; giantwordlist_Type(SwitchInds)];
    %
    %     giantwordlist_Inds(SwitchInds)=[];
    %     giantwordlist_Type(SwitchInds)=[];
else
    giantwordlist_Inds=giantwordlist_Inds(1:c);
    giantwordlist_Type=giantwordlist_Type(1:c);
end

% determine the num of same trials in the main block we're yoking this to        
nsame=sum(samestruct);   % samestruct was loaded above ... so automatically the same number of same trials as in the main experimental block        

%%%% shuffle word order
samestruct=zeros(nsentences,1);  % here we're writing over samestruct  
samestruct(1:nsame)=1; %        
samestruct=samestruct( randperm(nsentences) );


%%%%%  generate each sentence randomly
TypeCounts=zeros(1,nGrammCats);
rootlist=wordlist;
for isent = 1:nsentences  %% we just change the wordlists
    %%%%% generate a random list replacing the existing one
    inum = 1;
    nwords =SentLens(isent);
    DontRepeatInds=[];
    
    for iword=1:nwords
        if iword==1;     % can choose any word to start with   
            posTypes=1:nGrammCats;                        
        else
            posTypes=CanFollowTypes{ PrevType };
        end
        
        tmpInds= find(ismember( giantwordlist_Type,posTypes ) & ~ismember( giantwordlist_Inds,DontRepeatInds ));
        if isempty(tmpInds)
            % then we need to go from the remainder list
            tmpInds= find( ismember( Remainderlist_Type,posTypes ) & ~ismember( Remainderlist_Inds,DontRepeatInds ));
            if isempty(tmpInds)     % we ran out of matching words... just pick at random from what's left
                if ~isempty(giantwordlist_Inds)
                    chosenInd=randi(length(giantwordlist_Inds));
                    curtw=giantwordlist_Inds( chosenInd );
                end
                
                % check to make sure this root didn't already exist in this sentence                         
                if isempty(giantwordlist_Inds) || ismember( TermWord.Root{curtw},rootlist{isent,inum}(1:iword-1) )
                    % if so, pick from the original wordlist                     
                    tmpInds= find(ismember( TermWord.OrigList_Types,posTypes ) & ~ismember( TermWord.OrigList_Inds,DontRepeatInds ));
                    
                    % randomly pick a possible word
                    chosenInd=randi(length(tmpInds));
                    curtw=TermWord.OrigList_Inds( tmpInds(chosenInd) );
                else
                    % then the word was good, remove it from the list      
                    giantwordlist_Inds( chosenInd )=[];
                    giantwordlist_Type( chosenInd )=[];
                end
            else
                chosenInd=randi(length(tmpInds));
                curtw= Remainderlist_Inds( tmpInds(chosenInd) );
                
                Remainderlist_Inds( tmpInds(chosenInd) )=[];
                Remainderlist_Type( tmpInds(chosenInd) )=[];
            end
        else
            % randomly pick a possible word
            chosenInd=randi(length(tmpInds));
            curtw=giantwordlist_Inds( tmpInds(chosenInd) );
            
            giantwordlist_Inds( tmpInds(chosenInd) )=[];
            giantwordlist_Type( tmpInds(chosenInd) )=[];
        end
        
        wordlist{isent,inum}{iword} = TermWord.List{curtw};
        rootlist{isent,inum}{iword} = TermWord.Root{curtw};        
        TypeCounts( TermWord.FirstParentType(curtw) )=TypeCounts( TermWord.FirstParentType(curtw) )+1;
        if iword<nwords
            PrevType=TermWord.FirstParentType(curtw);
            DontRepeatInds=[DontRepeatInds TermWord.CommonRootInds{curtw}];
        end
    end
    wordlist{isent,inum}=wordlist{isent,inum}(1:nwords);
    rootlist{isent,inum}=rootlist{isent,inum}(1:nwords);
    
    
    inum = 2;
    if samestruct(isent)  %%%% draw a word from the previous list
        newword = random('unid',nwords);
        wordlist{isent,inum} = { wordlist{isent,1}{newword} };
        rootlist{isent,inum} = { rootlist{isent,1}{newword} };
    else
        FindDiffProbeWord
    end        
end






if DisplaySentsAtEnd
    for isent=1:nsentences
        for inum=1:2
            disp(wordlist{isent,inum})
            if inum==1
                if samestruct(isent)
                    disp('Same')
                else
                    disp('Diff')
                end
            end
        end
        disp('************************************');
    end
end

disp('done')