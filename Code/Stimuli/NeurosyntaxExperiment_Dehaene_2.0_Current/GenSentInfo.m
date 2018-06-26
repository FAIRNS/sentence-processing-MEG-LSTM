% GenSentInfo(isent).m

if isent==1;        SentInfo=struct;        end
SentInfo(isent).SentType=curSentType;
if ismember( curSentType,[1 2 3] )
    % Trans sents       
    % choose Anim Type
    
    TransAnimType=ChooseFromRemCounts( RemCounts.TransAnim );
    RemCounts.TransAnim( TransAnimType )= RemCounts.TransAnim( TransAnimType )-1;
    
    %TransAnimType=4; % for debugging   
    
    switch TransAnimType
        case 1
            % A to A
            SentInfo(isent).AnimSubj=1;
            SentInfo(isent).AnimObj=1;
        case 2
            % A to IA
            SentInfo(isent).AnimSubj=1;
            SentInfo(isent).AnimObj=0;
        case 3
            % IA to A
            SentInfo(isent).AnimSubj=0;
            SentInfo(isent).AnimObj=1;
        case 4
            % IA to IA
            SentInfo(isent).AnimSubj=0;
            SentInfo(isent).AnimObj=0;
    end               
else
    % InTrans sents  
    % choose Anim and Verb Type
        
    InTransAnimAndVerbType= ChooseFromRemCounts( RemCounts.InTransAnimAndVerb );
    RemCounts.InTransAnimAndVerb( InTransAnimAndVerbType )= RemCounts.InTransAnimAndVerb( InTransAnimAndVerbType )-1;

    switch InTransAnimAndVerbType   % bc unerg w inanim subject is impossible, here we merge the unerg and unaccus possibilities for inanimate subjects  
        case 1
            % A subj unerg
            SentInfo(isent).AnimSubj=1;
            SentInfo(isent).InTransUnErg=1;
        case 2
            % A subj unacc
            SentInfo(isent).AnimSubj=1;
            SentInfo(isent).InTransUnErg=0;
        case {3,4} 
            % IA subj unacc
            SentInfo(isent).AnimSubj=0;
            SentInfo(isent).InTransUnErg=0;
    end
end
    

if curSentType~=3
    % for all sents with a PP    
        
    PPAnimType=ChooseFromRemCounts( RemCounts.PPAnim );
    RemCounts.PPAnim( PPAnimType )= RemCounts.PPAnim( PPAnimType )-1;    
    
    switch PPAnimType
        case 1
            SentInfo(isent).AnimPP_NP=1;
        case 2
            SentInfo(isent).AnimPP_NP=0;
    end
end


% Determine nWords for each Adj Phrase and Adv Phrase
% SentInfo(isent).AdjPnWords is 3x1. Order is: [for the NP, for the Obj, for the PP]   
SentInfo(isent).AdjP_nWords =zeros(3,1);
SentInfo(isent).AdvP_nWords=0;
AlreadyUsedIntens=0;

totn=length( SentInfo(isent).AdjP_nWords ) + length( SentInfo(isent).AdvP_nWords );
tmpiAPs=randperm(totn);
for iiAP=1:totn
    iAP=tmpiAPs(iiAP);  % process the diff adj or adv phrases in a random order
    if iAP==4
        if MaxOneVeryPerSentence && AlreadyUsedIntens
            tmpcounts= Counts.AdvP_nWords(1:2);
        else
            tmpcounts= Counts.AdvP_nWords;
        end
        curnWords=ChooseFromCounts( tmpcounts,nAPwordRates(1:length(tmpcounts)) );
        SentInfo(isent).AdvP_nWords=curnWords-1;    % will be 0,1 or 2
        Counts.AdvP_nWords( curnWords ) = Counts.AdvP_nWords( curnWords )+1;
        
    elseif ~( (iAP==2 && ismember( curSentType,[4 5 6] )) || (iAP==3 && curSentType==3) )
        if MaxOneVeryPerSentence && AlreadyUsedIntens
            tmpcounts= Counts.AdjP_nWords(1:2);
        else
            tmpcounts= Counts.AdjP_nWords;
        end
        curnWords=ChooseFromCounts( tmpcounts,nAPwordRates(1:length(tmpcounts)) );
        SentInfo(isent).AdjP_nWords( iAP )=curnWords-1;    % will be 0,1 or 2
        Counts.AdjP_nWords( curnWords ) = Counts.AdjP_nWords( curnWords )+1;
    else
        % for example, we get here for iAP==3 and curSentType==3   
        curnWords=0;
    end
    
    if MaxOneVeryPerSentence && curnWords==3
        AlreadyUsedIntens=1;
    end
end



% set Sing/Plural and Number for each NP
% have a randomly chosen NP det its val from overall counts, then have the other NPs stay or switch relative to that   
SentInfo(isent).NP_SingPlur =zeros(3,1);   % Order is: [for the NP, for the Obj, for the PP] ... 1 for Sing 2 for Plur
SentInfo(isent).NP_NumOrNoNum =zeros(3,1);   % Order is: [for the NP, for the Obj, for the PP] ... 1 for NoNum, 2 for Num     
SentInfo(isent).NP_DefType= zeros(3,1);    %1 for indef, 2 for def, 3 for demonstrative
SentInfo(isent).NP_ThisOrThat= zeros(3,1);     %1 for this, 2 for that
switch curSentType
    case {1,2}
        %NPsPres=[1 1 1];
        [SentInfo(isent).NP_SingPlur,Counts.NPPatterns111.SingPlural]= AssignDetPatterns( Counts.NPPatterns111.SingPlural );        
        [SentInfo(isent).NP_DefType,Counts.NPPatterns111.DefType]= AssignDetPatterns( Counts.NPPatterns111.DefType );                       
         
        % Dont count numbers like this... assign and count them later independently for each NP      
        %[SentInfo(isent).NP_NumOrNoNum,Counts.NPPatterns111.NumOrNoNum]= AssignDetPatterns( Counts.NPPatterns111.NumOrNoNum );                
        
        %disp([ num2str(Counts.NPPatterns111.DefType')])
        %disp([ num2str(Counts.NPPatterns111.SingPlural') '            ' num2str(Counts.NPPatterns111.NumOrNoNum') ])
    case {3}
        %NPsPres=[1 1 0];
        [SentInfo(isent).NP_SingPlur,Counts.NPPatterns110.SingPlural]= AssignDetPatterns( Counts.NPPatterns110.SingPlural,110 );        
        [SentInfo(isent).NP_DefType,Counts.NPPatterns110.DefType]= AssignDetPatterns( Counts.NPPatterns110.DefType,110 );
        
        % Dont count numbers like this... assign and count them later independently for each NP   
        %[SentInfo(isent).NP_NumOrNoNum,Counts.NPPatterns110.NumOrNoNum]= AssignDetPatterns( Counts.NPPatterns110.NumOrNoNum,110 );
        
        %disp([ num2str(Counts.NPPatterns110.DefType')])
        %disp([ num2str(Counts.NPPatterns110.SingPlural') '            ' num2str(Counts.NPPatterns110.NumOrNoNum') ])
    case {4,5,6}
        %NPsPres=[1 0 1];
        [SentInfo(isent).NP_SingPlur,Counts.NPPatterns101.SingPlural]= AssignDetPatterns( Counts.NPPatterns101.SingPlural,101 );        
        [SentInfo(isent).NP_DefType,Counts.NPPatterns101.DefType]= AssignDetPatterns( Counts.NPPatterns101.DefType,101 );
        
        % Dont count numbers like this... assign and count them later independently for each NP    
        %[SentInfo(isent).NP_NumOrNoNum,Counts.NPPatterns101.NumOrNoNum]= AssignDetPatterns( Counts.NPPatterns101.NumOrNoNum,101 );
        
        %disp([ num2str(Counts.NPPatterns101.DefType')])
        %disp([ num2str(Counts.NPPatterns101.SingPlural') '            ' num2str(Counts.NPPatterns101.NumOrNoNum') ])
end


%SentInfo(isent).NP_SingPlur(1:2)=1; %  for debugging  

% Vary this vs that accordingly when using a demonstrative and vary Num Or NoNum     
SentInfo(isent).NP_NumOrNoNum(3)=1;    % No nums allowed in the PP!!!
for iNP=1:3
    if SentInfo(isent).NP_DefType(iNP)==3
        tmpType=ChooseFromCounts( Counts.ThisVsThat(iNP,:) );
        Counts.ThisVsThat( iNP,tmpType )=Counts.ThisVsThat( iNP,tmpType ) +1;
        SentInfo(isent).NP_ThisOrThat(iNP)=tmpType;
    end   
    
    if iNP==3
        SentInfo(isent).NP_NumOrNoNum(iNP)=1;  % No nums allowed in the PP!!!
    else
        if iNP==1 || (iNP==2 && ismember(curSentType,[1 2 3]))   
            %disp(['iNP: ' num2str(iNP) '   curSentType: '  num2str(curSentType)]) 
            if NoNumsForSingularNouns && SentInfo(isent).NP_SingPlur(iNP)==1
                SentInfo(isent).NP_NumOrNoNum(iNP)=1;
            else
                tmpType=ChooseFromCounts( Counts.NumOrNoNum(iNP,:),1-NumUseRate );  % 1-NumUseRate bc curType=1 corresponds to NoNumber
                Counts.NumOrNoNum( iNP,tmpType )=Counts.NumOrNoNum( iNP,tmpType ) +1;
                SentInfo(isent).NP_NumOrNoNum(iNP)=tmpType;
            end
        end
    end
end

if PairNumsAndLongNPs
    if any( SentInfo(isent).NP_NumOrNoNum==2 )  
        % find the longest NP ... place the number there if it's plural and not indefinite      
        [nWords,sInds]=sort( SentInfo(isent).AdjP_nWords(1:2),'descend' );
        sInds=sInds( nWords==nWords(1) );  % select only those equal to the maximum  
        iP=1;
        while iP<=length(sInds)
            if SentInfo(isent).NP_DefType( sInds(iP) )~=1 && SentInfo(isent).NP_SingPlur( sInds(iP) )==2
                % change the pos of the number, if it's not already where you want it   
                if ~(SentInfo(isent).NP_NumOrNoNum( sInds(iP) )==2)
                    ind2=find(SentInfo(isent).NP_NumOrNoNum==2,1);
                    SentInfo(isent).NP_NumOrNoNum( ind2 )=1;
                    SentInfo(isent).NP_NumOrNoNum( sInds(iP) )=2;
                    break
                end
            end
            iP=iP+1;
        end
    end
end
        

% Record AllnWords and LimitSenLength if desired
AllnWords=[SentInfo(isent).AdjP_nWords; SentInfo(isent).AdvP_nWords];
NumWordAdded=(SentInfo(isent).NP_NumOrNoNum==2) .* ~(SentInfo(isent).NP_DefType==1);
AllnWords(1:3)=  AllnWords(1:3) + NumWordAdded;    
    
if LimSenLength && ismember(curSentType,[1 2])         
    
    % for more interesting stimuli for the node closing analyses, we'll leave untouched the most complex NP(s), and instead limit the other NPs based on the desired MaxSentLength    
    [nWords,sInds]=sort(AllnWords);
    icut=1;    
    while sum( AllnWords )>nAddedAllowed
        curP=sInds(icut);
        if AllnWords( curP )>0                  
            if curP<4 
                % cutting an AdjP    
                % first remove adjs and preserve num words added, then remove num words if needed    
                %if SentInfo(isent).AdjP_nWords( curP )==0 && NumWordAdded( curP )                     
                %    AllnWords( curP )=0;
                %    SentInfo(isent).NP_NumOrNoNum(curP)=1;    %% never remove a number...   
                %    icut=icut+1;
                %else
                    AllnWords( curP )=NumWordAdded(curP);
                    Counts.AdjP_nWords( SentInfo(isent).AdjP_nWords( curP )+1 ) = Counts.AdjP_nWords( SentInfo(isent).AdjP_nWords( curP )+1 ) - 1;
                    Counts.AdjP_nWords( 1 )=Counts.AdjP_nWords( 1 )+1;
                    SentInfo(isent).AdjP_nWords( curP )=0;
                    
                    icut=icut+1;
                %end
            else
                % cutting an AdvP   
                AllnWords( curP )=0;
                Counts.AdvP_nWords( SentInfo(isent).AdvP_nWords+1 ) = Counts.AdvP_nWords( SentInfo(isent).AdvP_nWords+1 ) - 1;
                Counts.AdvP_nWords( 1 )=Counts.AdvP_nWords( 1 )+1;
                SentInfo(isent).AdvP_nWords=0;
                icut=icut+1;
            end            
        else
            icut=icut+1;
        end
    end
end

SentInfo(isent).AllnWords=cell(1,4);
for iP=1:4    
    if iP==3 && curSentType==3
        SentInfo(isent).AllnWords{iP}=[];
    elseif iP==2 && ismember( curSentType,[4 5 6] )
        SentInfo(isent).AllnWords{iP}=[];
    else
        SentInfo(isent).AllnWords{iP}=AllnWords(iP);
    end
end

%disp( ['DefType: ' num2str( SentInfo(isent).NP_DefType' ) '      Clsnss To Spkr: ' num2str(SentInfo(isent).NP_ThisOrThat')])
%disp( ['SingOrPlu: ' num2str( SentInfo(isent).NP_SingPlur' ) '     Num Or No Num   ' num2str( SentInfo(isent).NP_NumOrNoNum' )] )



