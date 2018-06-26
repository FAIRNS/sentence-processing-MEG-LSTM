function [s,wordusecount,Counts] = GenerateSentence(r,SentInfo,rmatchlist,rwtlist,wordusecount,Counts,istermword)
%%%%% generate a sentence s, based on the rules r
%
% Adjusted by MJN for Neurosyntax 2.0 150202

%initialize
AlreadyPresent.NAnim=0;
AlreadyPresent.NInAnim=0;
AlreadyPresent.AdjAnim=0;
AlreadyPresent.AdjAnimEmot=0;
AlreadyPresent.AdjPhys=0;
AlreadyPresent.Num=0;
AlreadyPresent.NoNum=0;

verbose = 0;  %% turn to 1 to see all of the temporarily generated structures

nrules = length(r);

% initialize the first node
s.node{1}=r{1}.match;  %%% start with the top-most item in the rules
s.satis{1}=0; % not yet satisfied
s.labels{1}={};

%%% apply successive rules until all nodes are satisfied with the
%%% appropriate children
nonsatis = 1;
totnode=1; %%% total number of nodes
while nonsatis>0;   
    %%% find the first non-satisfied node
    for inode = 1:length(s.node)
        if s.satis{inode}==0
            break
        end
    end    
    
    if strcmp(s.node{inode},'aga') %% track a specific problematic word
        verbose = 1;
        DisplayAllNodes(s,1);
    end
       
    %%% find all the matching rules, and select them by randomly based on their wts   
    % find all matching rules and corresponding wts              
    MatchedrInds=find( strcmp(s.node{inode},rmatchlist));
              
    % Apply pre-set sentenbce configurations in SentInfo...    
    OffLab='';
    % Apply rules for the pre-determined length of the Adj and Adv Phrases   
    if ~isempty(strfind( s.node{inode},'_N_L_ADJUNCT' )) || ismember( s.node{inode},{'_V_L_ADJUNCT','_A_SPEC','_ADV_SPEC'} )
        if ~isempty(strfind( s.node{inode},'_N_L_ADJUNCT' )) || strcmp( s.node{inode},'_A_SPEC' )
            curCase=CalcCurCase( s.labels{inode} );     % creates the variable curCase, of value: 1 for nominative, 2 for accusative, and 3 for locative
        end
        % the subst choices one encounters here are all binary so we only need to record the OffLabs   
        if ~isempty(strfind( s.node{inode},'_N_L_ADJUNCT' ))
            if SentInfo.AdjP_nWords(curCase)==0
                OffLab={'_A_P2'};
            else
                OffLab={'#empty'};
            end
        elseif strcmp( s.node{inode},'_A_SPEC' )
            if SentInfo.AdjP_nWords(curCase)==1      % SentInfo.AdjPnWords is 3x1. Order is: [for the NP, for the Obj, for the PP]   
                OffLab={'_INTENSIF'};
            else
                OffLab={'#empty'};
            end
        elseif strcmp( s.node{inode},'_V_L_ADJUNCT' )
            if SentInfo.AdvP_nWords==0
                OffLab={'_ADV_P2'};
            else
                OffLab={'#empty'};
            end
        elseif strcmp( s.node{inode},'_ADV_SPEC' )
            if SentInfo.AdvP_nWords==1
                OffLab={'_INTENSIF'};
            else
                OffLab={'#empty'};
            end
        end                         
    elseif strcmp( s.node{inode},'_N_SPEC' )
        curCase=CalcCurCase( s.labels{inode} );      % creates the variable curCase, of value: 1 for nominative, 2 for accusative, and 3 for locative
        
        if SentInfo.NP_NumOrNoNum(curCase)==2   % a number is given                
            OffLab={'#empty'};
            if SentInfo.NP_DefType(curCase)==1   % go to '_NUM_D_P0' only in this case      
                OffLab=[OffLab '_NUM'];
            else
                OffLab=[OffLab '_NUM_D_PO'];
            end
        elseif SentInfo.NP_NumOrNoNum(curCase)==1   % a number is not given   
            OffLab={'_NUM','_NUM_D_P0'};
        end
    end
    
    %Remove the OffLabs
    if ~isempty(OffLab)
        RemInds=[];
        for im=1:length( MatchedrInds )
            if ismember( r{MatchedrInds(im)}.subst{1},OffLab )
                RemInds=[RemInds; im];
            end
        end
        MatchedrInds(RemInds)=[];
    end
    
            
    % Remove matches that don't match animacy or verb type specifications     
    KeepLab='';
    if strcmp(s.node{inode},'_N_P0')        
        if ismember( '$NOMINATIVE',s.labels{inode} )
            if SentInfo.AnimSubj
                KeepLab='$ANIMATE';
            else
                KeepLab='$INANIMATE';
            end
        elseif ismember( '$ACCUSATIVE',s.labels{inode} )
            if SentInfo.AnimObj
                KeepLab='$ANIMATE';
            else
                KeepLab='$INANIMATE';
            end
        elseif ismember( '$LOCATIVE',s.labels{inode} )
            if SentInfo.AnimPP_NP
                KeepLab='$ANIMATE';
            else
                KeepLab='$INANIMATE';
            end
        end                                      
    elseif strcmp(s.node{inode},'_VT_V_P0')
        if SentInfo.AnimSubj
            KeepLab{1}='$ANIMATE_SUB';
        else
            KeepLab{1}='$INANIMATE_SUB';
        end
        if SentInfo.AnimObj
            KeepLab{2}='$ANIMATE_OBJ';
        else
            KeepLab{2}='$INANIMATE_OBJ';
        end        
    elseif strcmp(s.node{inode},'_VI_V_P0')
        if SentInfo.AnimSubj
            KeepLab{1}='$ANIMATE_SUB';
        else
            KeepLab{1}='$INANIMATE_SUB';
        end
        if SentInfo.InTransUnErg
            KeepLab{2}='$UNERGATIVE';
        else
            KeepLab{2}='$UNACCUSATIVE';
        end
    elseif strcmp(s.node{inode},'_P_P0')
        if SentInfo.AnimPP_NP
            % remove the words that aren't 'near'     
            RemInds=[];
            for im=1:length( MatchedrInds )
                if ~isfield( r{MatchedrInds(im)},'lab' ) || ~strcmp( r{MatchedrInds(im)}.lab,'ANIMATE_P' )
                    RemInds=[RemInds; im];
                end
            end
            MatchedrInds(RemInds)=[];
        end
    elseif strcmp(s.node{inode},'_A_P0')        
        if (ismember( '$NOMINATIVE',s.labels{inode} ) && SentInfo.AnimSubj) || (ismember( '$ACCUSATIVE',s.labels{inode} ) && SentInfo.AnimObj) || (ismember( '$LOCATIVE',s.labels{inode} ) && SentInfo.AnimPP_NP)
            % this adj is then for an anim NP
            if AlreadyPresent.AdjAnim
                % stay/switch systematically here    
                if Counts.StayOrSwitch.EmotPhys==1    % here we'll stay
                    if AlreadyPresent.AdjAnimEmot;      tmpType=1;      else    tmpType=2;      end
                    Counts.StayOrSwitch.EmotPhys=0;   % switch next time
                else    % here we'll switch
                    if AlreadyPresent.AdjAnimEmot;      tmpType=2;      else    tmpType=1;      end
                    Counts.StayOrSwitch.EmotPhys=1;   % stay next time
                end
            else
                tmpType=ChooseFromCounts( Counts.AnimEmotOrPhys );
                AlreadyPresent.AdjAnim=1;
            end
            
            switch tmpType
                case 1
                    KeepLab='$EMOTION';
                    AdjType='AnimEmot';
                case 2
                    KeepLab='$PHYSICAL';
                    AdjType='AnimPhys';
            end
            Counts.AnimEmotOrPhys(tmpType)=Counts.AnimEmotOrPhys(tmpType)+1;
        else
            % this adj is then for an inanim NP
            KeepLab='$PHYSICAL';
            AdjType='InAnimPhys';
        end
    elseif strcmp(s.node{inode},'_NUM')
        curCase=CalcCurCase( s.labels{inode} );
        
        if SentInfo.NP_SingPlur(curCase)==2
            KeepLab='$PLURAL';
        elseif SentInfo.NP_SingPlur(curCase)==1
            KeepLab='$SINGULAR';
        end
    elseif strcmp( s.node{inode},'_D_P0' )
        curCase=CalcCurCase( s.labels{inode} );
        
        KeepLab={Counts.NP_DefType_List{ SentInfo.NP_DefType(curCase) }};
        % Apply rules for the choice of demonstratives
        switch SentInfo.NP_DefType(curCase)
            case 1  % Indefinite
                if SentInfo.NP_NumOrNoNum(curCase)==2
                    KeepLab=[KeepLab '$NUMBER_GIVEN'];
                elseif SentInfo.NP_NumOrNoNum(curCase)==1
                    KeepLab=[KeepLab Counts.NP_SingPlur_List{ SentInfo.NP_SingPlur(curCase) }];
                end
            case 2 % Definite ... nothing needed
            case 3 % Demonstrative
                KeepLab=[KeepLab Counts.NP_SingPlur_List{ SentInfo.NP_SingPlur(curCase) }];
                KeepLab=[KeepLab Counts.NP_ThisOrThat_List{ SentInfo.NP_ThisOrThat(curCase) }];
        end
    elseif strcmp(s.node{inode},'_T_P0') && isfield(SentInfo,'nToAdd') % nToAdd will only be a field for the Localizer sentences, where we dictate verb tense based on the desired length of the sentences                
        if SentInfo.nToAdd(4)
            % future or present perfect   
            KeepLab='$AUX_YES';
        else
            KeepLab='$AUX_NO';
        end
    end
    
    
    % remove matches that don't have ALL items in the Keep Lab, unless KeepLab is empty   
    if ~isempty(KeepLab)
        RemInds=[];
        for im=1:length( MatchedrInds )
            if ~isfield( r{MatchedrInds(im)},'addi' ) || ~all( ismember( KeepLab,r{MatchedrInds(im)}.addi{1} ) )
                RemInds=[RemInds; im];
            end
        end
        MatchedrInds(RemInds)=[];
    end
        
    % For rules leading always to terminal words: keep only the MatchedrInds equal to the minimum word count for all possible words chosen    
    if all( istermword(MatchedrInds) )           
        ProcessStaySwitch   % A script that when there is a repeat of a word subgroup (ie Animate Nouns) in a sentence will equate the probability of a stay or switch in the type of word, without repeating the same precise word            
        
        if strcmp(s.node{inode},'_A_P0') && length(MatchedrInds)==4     % don't go here if this was already processed above with a stay/switch   
            % adj counts will work differently
            curCounts=Counts.(AdjType);
        else
            curCounts=wordusecount(MatchedrInds);
        end
        MatchedrInds= MatchedrInds( curCounts==min(curCounts) );
    end        

    % now select the rules randomly based on the weights of the remaining matches  
    if ~isempty(MatchedrInds)        
        MatchFound=1;
        MatchedrWts=rwtlist( MatchedrInds );
        
        % randomly select according to the wts given store the rule number and wts for this matching rule    
        tmpwtsum=cumsum(MatchedrWts);
        tmplist= find( tmpwtsum>=(sum(MatchedrWts)*rand) );
        
        ChosenMatchNum=tmplist(1);        
        selrule= MatchedrInds(ChosenMatchNum);
    end
    
    if MatchFound                
        %%%%% apply the rule that was found
        if verbose
            disp(r{selrule});
        end
        s.satis{inode}=1;  %%% the current node is now satisfied
        s.nchildren{inode} = length(r{selrule}.subst);
        %%% create all children and link them to the current node
        for ichild = 1:s.nchildren{inode}
            totnode = totnode +1;
            s.children{inode}(ichild)=totnode;
            s.node{totnode} = r{selrule}.subst{ichild};
            s.nchildren{totnode} = 0; %%% temporarily set the number of children to zero -- will be overriden if needed
            if strcmp(s.node{totnode}(1),'_')  %%% non terminal node
                s.satis{totnode} = 0;
            else
                %%% terminal node
                s.satis{totnode} = 1;
                s.terminalword{totnode} = stripunderscore(s.node{totnode});                                                                
                
                % adjust wordcounts and deal with repeats     
                if istermword(selrule) && ~strcmp(s.node{totnode},'very') % 'very' is dealt with in other code      
                    % deal with repeats for N and Adj and Num  
                    if ismember(s.node{inode},{'_N_P0','_A_P0','_NUM'}) 
                        if sum(strcmp( s.terminalword{totnode},s.terminalword )) >1
                            % this word is a repeat in the sentence. Swap it for the most simlar word  
                            FindAndApplyMatchingRule  % this will adjust selrule, and so the counting following this should remain accurate                                                        
                        end
                    end
                    
                    % adj counts will work differently
                    if strcmp(r{selrule}.match,'_A_P0')                                                                       
                        AdjInd= find( strcmp(s.node{totnode},Counts.([AdjType 'List'])) );                                                
                        Counts.(AdjType)(AdjInd) = Counts.(AdjType)(AdjInd)+1;
                    else                        
                        if ~( strcmp(r{selrule}.match,'_P_P0') && SentInfo.AnimPP_NP )  % Don't let the use of 'near' w an animate PP_NP affect its wordcount so that we balance the prepositions for the inanimate PP_NP's
                            wordusecount(selrule)=wordusecount(selrule)+1;
                        end
                    end                                        
                end
                 
            end
            
            %%%% now prepare the list of additional labels
            %%% make labels from parent apply to children 
            s.labels{totnode}=s.labels{inode};
                        
            % add addi specific to this rule   
            if isfield( r{selrule},'addi' )                                
                % if we've assigned case here, then assign number at this point too  
                if ismember(r{selrule}.addi{1}{1},Counts.CaseList)
                    curCase=CalcCurCase( r{selrule}.addi{1} );
                    
                    % Remove any existing labels for Case, SingOrPlur, Definiteness, Closeness to Speaker                        
                    s.labels{totnode}( ismember( s.labels{totnode},[Counts.CaseList Counts.NP_SingPlur_List, Counts.NP_DefType_List Counts.NP_ThisOrThat_List] ) )=[];                    
                    
                    % Assign labels for SingOrPlur, Definiteness, Closeness to Speaker    
                    s.labels{totnode}=[s.labels{totnode}  Counts.NP_SingPlur_List{SentInfo.NP_SingPlur(curCase)}];
                    s.labels{totnode}=[s.labels{totnode}  Counts.NP_DefType_List{SentInfo.NP_DefType(curCase)}];
                    if SentInfo.NP_ThisOrThat(curCase);         s.labels{totnode}=[s.labels{totnode}  Counts.NP_ThisOrThat_List{SentInfo.NP_ThisOrThat(curCase)}];          
                    end                    
                end       
                
                s.labels{totnode} = [s.labels{totnode} r{selrule}.addi{1}];
            end                        
        end
        
        %%% check the number of non-satisfied nodes
        nonsatis = 0;
        for inode = 1:length(s.node)
            if s.satis{inode}==0
                nonsatis = nonsatis + 1;
            end
        end
        
        reset_all = 0;
    else
        %%% restart the search for a valid sentence?
        disp(sprintf('no remaining matching rule for  %s -- start again',s.node{inode}));
        reset_all = 1;
    end
    

    if reset_all
        clear s;
        %% initialize the rules        
        % reinitialize the first node
        s.node{1}=r{1}.match;  %%% start with the top-most item in the rules
        s.satis{1}=0; % not yet satisfied
        
        %%% apply successive rules until all nodes are satisfied with the
        %%% appropriate children
        nonsatis = 1;
        totnode=1; %%% total number of nodes
    end
end