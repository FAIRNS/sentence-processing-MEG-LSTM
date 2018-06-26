%SetControlBlockStimuli.m     

DisplaySentsAtEnd=1;
SentLenLims=[4 8]; %uniform prob of a control list length between these limits    

%  for makingsure we avoid the most common spurious constituents by limiting our choice of words based on the word immediately preceding it    
%                1           2           3           4         5          6        7         8        9           10  
GrammCats = {'_N_P0',  '_VT_V_P0',  '_VI_V_P0',  '_A_P0',  '_ADV_P0',  'D_P0',  '_T_P0',  '_NUM',  '_P_P0',  '_INTENSIF'};
% each column sums to 1 and corresponds to what do for each previous state         
% but for visual simplicity, I'll enter it here so each row sums to 1, then I'll transpose it    

GrammCat_MarkovMat=ones(10,10); % these are all booleans, so not a proper Markov Matrix with columns summing to 1        



%%%%%%%%%%%%%%%%%%%%%  End of UserInputs

%%% set SentLens given the SentLenLims above  
nSentLens=diff(SentLenLims)+1;
nSentPerType=floor(nsentences/nSentLens);
nRem=nsentences-nSentLens*nSentPerType;

SentLens=zeros(nsentences,1);
for iSL=1:nSentLens
    SentLens( nSentPerType*(iSL-1)+1:nSentPerType*iSL )=SentLenLims(1)+iSL-1;
end
LeftOverCounts=zeros( nSentLens );
for iRem=1:nRem
    curType=ChooseFromCounts( LeftOverCounts );
    LeftOverCounts( curType )=LeftOverCounts( curType )+1;
    
    SentLens(end-(iRem-1))=curType+ SentLenLims(1) -1;
end
SentLens=SentLens( randperm(nsentences) );
ntotwords_Ctrl=sum(SentLens);

%disp('Select one of the existing data sets (''probably the most recent one'')');
%outfile = uigetfile('ExperimentalRun*.mat');
%load(outfile);
ControlExperiment = true;
%%%% begin by listing all the words used in the existing experiment
ntotwords = 0;
TermWord.List={};
TermWord.Count=[];
TermWord.FirstParent={};
for isent=1:nsentences
    nwords = length(wordlist{isent,1});
    for iword=1:nwords
        ntotwords = ntotwords +1;
        
        %giantwordlist{totwords}.word = wordlist{isent,1}{iword};
        %%%% keep track of the original sentence and node from which
        %%%% each word was originally drawn
        
        %giantwordlist{totwords}.sentenceID=isent;
        %giantwordlist{totwords}.nodeID = nodelist{isent,1}{iword};
        
        
        [tf,ind]=ismember( wordlist{isent,1}{iword},TermWord.List );
        if tf
            TermWord.Count(ind)=TermWord.Count(ind)+1;
        else
            TermWord.List{end+1}=wordlist{isent,1}{iword};            
            parents=FindParents( surface{isent},nodelist{isent,1}{iword} );            
            TermWord.FirstParent{end+1}=surface{isent}.node{parents(1)};
            TermWord.Count(end+1)=1;
        end
    end
end

% choose words to keep in the giant word list based on the ratio of word counts for the control to the main block     
KeepRat=ntotwords_Ctrl/ntotwords;
ntw=length(TermWord.Count);
giantwordlist_Inds=zeros( ntotwords_Ctrl,1 );
c=0;
for itw=1:ntw
    nKeep=fix(KeepRat*TermWord.Count(itw));
    if nKeep>0
        giantwordlist_Inds( c+1:c+nKeep )=itw;
        c=c+nKeep;
    end
end

% determine the num of same trials in the main block we're yoking this to        
nsame=sum(samestruct);   % samestruct was loaded above      

%%%% shuffle word order
samestruct=ones(nsentences,1);  % here we're writing over samestruct   
samestruct(1:nsame)=2;
samestruct=samestruct( randperm(nsentences) );

newwordorder = randperm(ntotwords);      


itot = 0;
for isent = 1:nsentences  %% we just change the wordlists
    %%%%% generate a random list replacing the existing one
    inum = 1;
    nwords =SentLenLims(isent);
    
    for iword=1:nwords
        itot = itot+1;
        newword = newwordorder(itot);
        wordlist{isent,inum}{iword} = giantwordlist{newword}.word;
        sentenceIDlist{isent,inum}{iword}=giantwordlist{newword}.sentenceID;
        nodelist{isent,inum}{iword} = giantwordlist{newword}.nodeID;
    end
    
    inum = 2;
    wordlist{isent,2}=cell(1); %%% we reduce the second sentence to one word
    if samestruct(isent)  %%%% draw a word from the previous list
        newword = random('unid',nwords);
        wordlist{isent,inum}{1} = wordlist{isent,1}{newword};
        nodelist{isent,inum}{1} = nodelist{isent,1}{newword};
    else
        %%% draw a word completely at random, but avoiding any existing
        %%% word in the previous list
        notgood = true;
        while notgood
            newword = random('unid',ntotwords);
            notgood = false;
            rootword = surface{giantwordlist{newword}.sentenceID}.node{giantwordlist{newword}.nodeID{1}};
            for iword =1:nwords     % scroll through words in the main sentence     
                %rootwordi = surface{sentlist{isent,1}{iword}}.node{nodelist{isent,1}{iword}{1}};
                
                rootwordi = surface{sentenceIDlist{isent,1}{iword}}.node{nodelist{isent,1}{iword}{1}};                                
                if strcmp(rootword,rootwordi)
                    notgood = true;
                    break
                end
            end
        end
        wordlist{isent,inum}{1} = giantwordlist{newword}.word;
        nodelist{isent,inum}{1} = giantwordlist{newword}.nodeID;
    end
end



%%%%  add in code to shuffle trials and ensure no repetaing of words in consecutive trials (if reasonably possible)    



if DisplaySentsAtEnd
    for isent=1:nsentences
        for inum=1:2
            disp(wordlist{isent,inum})
        end
        disp('************************************');
    end
end
