%%%%%%%%%%%%%%%%%% User Inputs  

%         1= PP 2= Obj 3 =Adj/Adv/NumDef 4= future or present perfect tense 
CostsToAdd=[3 2 1 1];
Reusable=[0 0 1 0];
%%%%%%%%%%%%%%%%%% End of User Inputs    

MinNWords=3;    % bare min for a sentence in this paradigm... not a user input, but entered by hand     

nExtraWords=Loc.SentLens(isent)-MinNWords;   % given num words, determine how many extra words

nopts=length( CostsToAdd );
SentInfo(isent).nToAdd=zeros(1,nopts);
while nExtraWords    
    if nExtraWords>=5
        % choose an Obj NP or a PP   
        curChoice=randi(2); % notethat to get here, we couldn't ever have used one of these before (with LocSentLims set at [4 8] anyway   
    else
        ToChooseFrom=find( CostsToAdd<=nExtraWords & (SentInfo(isent).nToAdd==0 | Reusable) & (SentInfo(isent).nToAdd<5) ); 
        
        curChoice=ToChooseFrom( randi(length(ToChooseFrom)) );
    end
    
    SentInfo(isent).nToAdd( curChoice )=SentInfo(isent).nToAdd( curChoice )+1;
    nExtraWords=nExtraWords- CostsToAdd(curChoice);
end

%Loc.SentLens(isent)
%SentInfo(isent).nToAdd

AdjSentTypeRuleWts_Loc


% Det AnimTypes
if ismember('Trans_On',OnLabs)
    % Trans
    TransAnimType=ChooseFromCounts( Loc.Counts.TransAnim );
    Loc.Counts.TransAnim( TransAnimType )= Loc.Counts.TransAnim( TransAnimType )-1;
    
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
    % InTrans 
    InTransAnimAndVerbType= ChooseFromCounts( Loc.Counts.InTransAnimAndVerb );
    Loc.Counts.InTransAnimAndVerb( InTransAnimAndVerbType )= Loc.Counts.InTransAnimAndVerb( InTransAnimAndVerbType )-1;
    
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


PPAnimType=ChooseFromCounts( Loc.Counts.PPAnim );
Loc.Counts.PPAnim( PPAnimType )= Loc.Counts.PPAnim( PPAnimType )-1;
switch PPAnimType
    case 1
        SentInfo(isent).AnimPP_NP=1;
    case 2
        SentInfo(isent).AnimPP_NP=0;
end


% Verb tense is taken care of within Generate Sentence       
% Assign other extra words     
SentInfo(isent).AdjP_nWords=zeros(3,1);
SentInfo(isent).AdvP_nWords=0;
SentInfo(isent).NP_SingPlur =zeros(3,1);   % Order is: [for the NP, for the Obj, for the PP] ... 1 for Sing 2 for Plur
SentInfo(isent).NP_NumOrNoNum =zeros(3,1);   % Order is: [for the NP, for the Obj, for the PP] ... 1 for NoNum, 2 for Num     
SentInfo(isent).NP_DefType= zeros(3,1);    %1 for indef, 2 for def, 3 for demonstrative
SentInfo(isent).NP_ThisOrThat= zeros(3,1);     %1 for this, 2 for that


RemToAdd=SentInfo(isent).nToAdd(3);
while RemToAdd>0;
    tmpNPs=find(SentInfo(isent).NPInc);
    if RemToAdd<3   % then we can include the VP ... otherwise to emphasize long NPs for interesting tests of constituent building, keep the added words to one phrase as much as possible  
        tmpNPs=[tmpNPs 4];
    end    
    iAP=tmpNPs( ChooseFromCounts( Loc.Counts.NPToLengthen(tmpNPs) ));
    Loc.Counts.NPToLengthen(iAP)=Loc.Counts.NPToLengthen(iAP)+1;
    
    if iAP==4       
        curToAdd=min(2,RemToAdd);
        SentInfo(isent).AdvP_nWords=curToAdd;
        %disp(['add ' num2str(curToAdd) ' to Adv_P'])
    else
        curToAdd=min(3,RemToAdd);
        if curToAdd==3
            SentInfo(isent).AdjP_nWords(iAP)=2;     % this could not occur in a PP for snets with less than 9 words   
            
            % add in a definite number   
            SentInfo(isent).NP_SingPlur(iAP)=2;
            SentInfo(isent).NP_DefType(iAP)= randi(2)+1;    %Def or Demons
            SentInfo(isent).NP_NumOrNoNum(iAP)=2;
            
            Loc.Counts.SingPlural(iAP,2)=Loc.Counts.SingPlural(iAP,2)+1;
            %Loc.Counts.NumOrNoNum(iNP,2)=Loc.Counts.NumOrNoNum(iNP,2)+1; dont count number in this case to balance out other cases below where numbers are impossible    
            Loc.Counts.DefType(iAP, SentInfo(isent).NP_DefType(iAP) )=Loc.Counts.DefType(iAP, SentInfo(isent).NP_DefType(iAP) )+1;
            
            if SentInfo(isent).NP_DefType(iAP)==3
                % choose this vs that for the demonstratives
                curVal=ChooseFromCounts( Counts.ThisVsThat(iAP,:) );
                Counts.ThisVsThat(iAP,curVal)=Counts.ThisVsThat(iAP,curVal)+1;
                SentInfo(isent).NP_ThisOrThat(iAP)=curVal;
            end
        else
            % det if definite and plural, and thus if an added number is possible   
            
            [SentInfo(isent),Loc.Counts] =ChooseSingAndDef( Loc.Counts,SentInfo(isent),iAP );
            
            % choose number, and subtract 1 from curAdd if it's a definite number   
            if SentInfo(isent).NP_SingPlur(iAP)==2 && iAP~=3
                curVal=ChooseFromCounts( Loc.Counts.NumOrNoNum(iAP,:) );
                Loc.Counts.NumOrNoNum(iAP,curVal)=Loc.Counts.NumOrNoNum(iAP,curVal)+1;
                SentInfo(isent).NP_NumOrNoNum(iAP)=curVal;
                if SentInfo(isent).NP_DefType(iAP)>=2 && curVal==2
                    curToAdd=curToAdd-1;
                    RemToAdd=RemToAdd-1;
                end
            else
                SentInfo(isent).NP_NumOrNoNum(iAP)=1;
            end
            SentInfo(isent).AdjP_nWords(iAP)=curToAdd;
            
            %disp(['add ' num2str(SentInfo(isent).AdjP_nWords(iAP)) ' to Adj_P: ' num2str(iAP)])
        end
    end
    
    RemToAdd=RemToAdd-curToAdd;
end
    
% SentInfo(isent).NP_SingPlur'
% SentInfo(isent).NP_DefType'
% SentInfo(isent).NP_NumOrNoNum'
% SentInfo(isent).AdjP_nWords'
% SentInfo(isent).AdvP_nWords

tmpNPs=find(SentInfo(isent).NPInc);
for iiNP=1:length(tmpNPs)
    iNP=tmpNPs(iiNP);
    
    if SentInfo(isent).NP_SingPlur(iNP)==0    % if this value is 1 0r 2 already, then it was entered above (as a def number to get an extra word) and we should skip assigning it here
        [SentInfo(isent),Loc.Counts] =ChooseSingAndDef( Loc.Counts,SentInfo(isent),iNP );
        
        if iNP==3 || SentInfo(isent).NP_SingPlur(iNP)==1 || SentInfo(isent).NP_DefType(iNP)>=2     
            SentInfo(isent).NP_NumOrNoNum(iNP)=1;    % No nums allowed in the PP, of ir it's singular, or if we have a definite article bc we controlled the number of words above   
        else
            curVal=ChooseFromCounts( Loc.Counts.NumOrNoNum(iNP,:) );
            Loc.Counts.NumOrNoNum(iNP,curVal)=Loc.Counts.NumOrNoNum(iNP,curVal)+1;
            SentInfo(isent).NP_NumOrNoNum(iNP)=curVal;
        end        
    end
end

