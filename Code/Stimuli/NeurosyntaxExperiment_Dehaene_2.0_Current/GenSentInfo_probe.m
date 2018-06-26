%GenSentInfo_probe.m
curType=ChooseFromCounts( Counts.Probe.SameOrDiff, SameToDiffRate );
Counts.Probe.SameOrDiff( curType )= Counts.Probe.SameOrDiff( curType )+1;
SentInfo(isent).Probe.SameOrDiff= curType;  %1 for Same, 2 for Diff

% SentInfo(isent).Probe.SameOrDiff= 1;  %1 for Same, 2 for Diff


VerbLexChange=0;
SentInfo(isent).Probe.NPToRep=[1 1 1];      %  the default... replace all 
SentInfo(isent).Probe.NPToGrammSwitch=[0 0 0];   %  the default... switch 
if SentInfo(isent).Probe.SameOrDiff==1     
    % code to avoid 2 its in a sentence 
    if ismember( curSentType,[1 2 3] ) && TransAnimType==4 && all( SentInfo(isent).NP_SingPlur(1:2)==1 )
        % then we need to ensure keeping the subj or obj NP to avoid 2 its in the same probe sentence
        curType= 2;  
        MustKeepObjOrSubj=1;
    else
        curType=ChooseFromCounts( Counts.Probe.Same_AllPronouns, SameToDiffRate );
        MustKeepObjOrSubj=0;
    end
    Counts.Probe.Same_AllPronouns( curType )= Counts.Probe.Same_AllPronouns( curType )+1;
    SentInfo(isent).Probe.Same_AllPronouns= curType;  %1 for replace all NP, 2 for Keep one NP    
         
    if SentInfo(isent).Probe.Same_AllPronouns==2
        % choose which NP to keep        
        ChooseNPToRepBySentType                        
    end
elseif SentInfo(isent).Probe.SameOrDiff==2
    % Gramm or Lexical change
    if AllowLexSwitch
        curType=ChooseFromCounts( Counts.Probe.Diff_GrammOrLexChange, GrammOrLexChangeRate );
        Counts.Probe.Diff_GrammOrLexChange( curType )= Counts.Probe.Diff_GrammOrLexChange( curType )+1;
        SentInfo(isent).Probe.Diff_GrammOrLexChange= curType;  %1 for Gramm changes, 2 for Lex change
    else
        SentInfo(isent).Probe.Diff_GrammOrLexChange=1;
    end
    
    
    if SentInfo(isent).Probe.Diff_GrammOrLexChange==1   % Gramm change    
        % Determine if gender change is possible, ie a singular (and possibly animate) noun exists           
        if ~JabberFlag
            PosGenSwitch=SentInfo(isent).NP_SingPlur(1:2)==1;
            if ~AllowAnimacySwitch
                PosGenSwitch(1)= PosGenSwitch(1) && SentInfo(isent).AnimSubj;
                PosGenSwitch(2)= PosGenSwitch(2) && SentInfo(isent).AnimObj;
            end
        else
            PosGenSwitch(1:2)=0;
        end
        
        if any(PosGenSwitch)
            % Gender, Number and Tense changes possible   
            curType=ChooseFromCounts( Counts.Probe.Diff_GenNumTenseChange, GenChangeRate );
            Counts.Probe.Diff_GenNumTenseChange( curType )= Counts.Probe.Diff_GenNumTenseChange( curType )+1;            
            SentInfo(isent).Probe.GrammSwitchType=curType;     % 1 for Gender, 2 for Number, 3 for Tense 
        else
            % only Number and Tense changes possible   
            curType=ChooseFromCounts( Counts.Probe.Diff_NumTenseChange, NumTenseChangeRate );
            Counts.Probe.Diff_NumTenseChange( curType )= Counts.Probe.Diff_NumTenseChange( curType )+1;            
            SentInfo(isent).Probe.GrammSwitchType=curType+1;     % 1 for Gender, 2 for Number, 3 for Tense   
        end
        %SentInfo(isent).Probe.GrammSwitchType=2;
        
        % determine which NPs to switch
        switch SentInfo(isent).Probe.GrammSwitchType
            case 1 % Gender
                % note that the precise genders have not been decided yet at this point... so we won't force them to be balanced we can switch taht on the fly
                if all(PosGenSwitch)
                    curType=ChooseFromCounts( Counts.Probe.NPGenSwitch11, 1/2 );
                    Counts.Probe.NPGenSwitch11( curType )= Counts.Probe.NPGenSwitch11( curType )+1;                                       
                    SentInfo(isent).Probe.NPToGrammSwitch(curType)=1;
                else                    
                    SentInfo(isent).Probe.NPToGrammSwitch( PosGenSwitch==1 )=1;
                end
            case 2 % number
                if curSentType>=4
                    SentInfo(isent).Probe.NPToGrammSwitch(1)=1;
                else
                    % which NP number to change
                    curType=ChooseFromCounts( Counts.Probe.NPNumSwitch11, 1/2 );
                    Counts.Probe.NPNumSwitch11( curType )= Counts.Probe.NPNumSwitch11( curType )+1;
                    SentInfo(isent).Probe.NPToGrammSwitch(curType)=1;
                end
        end
                        
        %SentInfo(isent).Probe.NPToGrammSwitch=[1 0 0];
        
        
        % determine which NPs to keep       
        switch curSentType
            case 1
                PosNPs=[1 1 1];
            case {2,3}
                PosNPs=[1 1 0];
            case {4,6}
                PosNPs=[1 0 1];
            case 5
                PosNPs=[1 0 0];
        end
        if SentInfo(isent).Probe.GrammSwitchType ~= 3
            PosNPs( SentInfo(isent).Probe.NPToGrammSwitch==1 )=0;                        
        end        
                 
        MustKeepObjOrSubj=0;    % to avoid 2 its in the sentence              
        if ismember( curSentType,[1 2 3] )
            if TransAnimType==4 && all( SentInfo(isent).NP_SingPlur(1:2)==1 )
                if SentInfo(isent).Probe.GrammSwitchType==3 || SentInfo(isent).Probe.NPToGrammSwitch(3)
                    MustKeepObjOrSubj=1;
                end
            elseif SentInfo(isent).Probe.GrammSwitchType==2 && TransAnimType==4       % number switch   
                ind=find( SentInfo(isent).Probe.NPToGrammSwitch );
                if SentInfo(isent).NP_SingPlur(ind)==2 && SentInfo(isent).NP_SingPlur(mymod(ind+1,2))==1  
                    MustKeepObjOrSubj=1;
                end
            elseif SentInfo(isent).Probe.GrammSwitchType==1 && all( SentInfo(isent).NP_SingPlur(1:2)==1 ) && AllowAnimacySwitch   % gender switch         
                ind=find( SentInfo(isent).Probe.NPToGrammSwitch );  % write the code assuming that a gender change changed to it...  
                if ind==1
                    if SentInfo(isent).AnimSubj==1 && SentInfo(isent).AnimObj==0
                        MustKeepObjOrSubj=1;
                    end
                elseif ind==2
                    if SentInfo(isent).AnimObj==1 && SentInfo(isent).AnimSubj==0
                        MustKeepObjOrSubj=1;
                    end
                end
            end
        end
             
        if any(PosNPs)
            % det if we keep another NP or not                 
            if MustKeepObjOrSubj
                SentInfo(isent).Probe.NPToRep( randi(2) )=0;
            else
                curType=ChooseFromCounts( Counts.Probe.Diff_NPKept, DiffKeepNPRate );
                Counts.Probe.Diff_NPKept( curType )= Counts.Probe.Diff_NPKept( curType )+1;   % 1 for Keep an NP, two to replace all NPs...
                if curType==1   % Keep an NP ... randomly choose it
                    PosNPInds=find(PosNPs);
                    SentInfo(isent).Probe.NPToRep( PosNPInds( randi(length(PosNPInds)) ) )=0;
                end
            end
        end
            
    elseif SentInfo(isent).Probe.Diff_GrammOrLexChange==2   % Lexical change
        %SentInfo(isent).AdjP_nWords(1)=1;
        
        % Det first if Adj or Adv to choose from exist       
        tmpList=1:length( Counts.Probe.LexChange_PerCat );  
        if ~ProbeElideAdv && ~SentInfo(isent).AdvP_nWords
            tmpList(4)=[];
        end        
        if ~any( SentInfo(isent).AdjP_nWords )
            tmpList(3)=[];
        end
                            
        curType=ChooseFromCounts( Counts.Probe.LexChange_PerCat(tmpList) );
        curType2=tmpList(curType);
        Counts.Probe.LexChange_PerCat( curType2 )=Counts.Probe.LexChange_PerCat( curType2 )+1;
        SentInfo(isent).Probe.LexChangeCat=curType2;
        
        %SentInfo(isent).Probe.LexChangeCat=3;
        
        
        switch SentInfo(isent).Probe.LexChangeCat
            case 1  % nouns... choose NP  
                tmpList=find( SentInfo(isent).NP_SingPlur>0 );
                
                curType=ChooseFromCounts( Counts.Probe.LexChange_NperNP(tmpList) );
                curType2=tmpList(curType);
                Counts.Probe.LexChange_NperNP( curType2 )=Counts.Probe.LexChange_NperNP( curType2 )+1;
                SentInfo(isent).Probe.NPToLexChange=curType2; 
                
                SentInfo(isent).Probe.NPToRep( curType2 )=0;     % 'keep' this NP...  
                if curType2==3 && ismember( curSentType,[2 5] )
                    SentInfo(isent).Probe.NPToRep( 1 )=0;     % In these cases we have to keep the subject NP too... 
                elseif curType2==3 && ismember( curSentType,[1 3] ) && TransAnimType==4 && all( SentInfo(isent).NP_SingPlur(1:2)==1 )  
                    % Code to avoid 2 its in same sent       
                     SentInfo(isent).Probe.NPToRep( randi(2) )=0;                                        
                end                                                    
            case 3 % adjectives... choose NP   
                tmpList=find( SentInfo(isent).AdjP_nWords>0 );
                
                curType=ChooseFromCounts( Counts.Probe.LexChange_AperNP(tmpList) );
                curType2=tmpList(curType);
                Counts.Probe.LexChange_AperNP( curType2 )=Counts.Probe.LexChange_AperNP( curType2 )+1;
                SentInfo(isent).Probe.NPToLexChange=curType2; 
                
                SentInfo(isent).Probe.NPToRep( curType2 )=0;     % 'keep' this NP... 
                if curType2==3 && ismember( curSentType,[2 5] )
                    SentInfo(isent).Probe.NPToRep( 1 )=0;     % In these cases we have to keep the subject NP too... 
                elseif curType2==3 && ismember( curSentType,[1 3] ) && TransAnimType==4 && all( SentInfo(isent).NP_SingPlur(1:2)==1 )  
                    % Code to avoid 2 its in same sent       
                     SentInfo(isent).Probe.NPToRep( randi(2) )=0;                                        
                end  
            case {2,4}  % V or Adv... 
                % randomly choose whether or not to keep an NP, and if so, which one to keep   
                % code to avoid 2 its in a sentence       
                if ismember( curSentType,[1 2 3] ) && TransAnimType==4 && all( SentInfo(isent).NP_SingPlur(1:2)==1 )
                    % then we need to ensure keeping the subj or obj NP to avoid 2 its in the same probe sentence
                    curType= 2;
                    MustKeepObjOrSubj=1;
                else
                    curType=ChooseFromCounts( Counts.Probe.Diff_NPKept, DiffKeepNPRate );
                    MustKeepObjOrSubj=0;
                end
                Counts.Probe.Diff_NPKept( curType )= Counts.Probe.Diff_NPKept( curType )+1;   %1 for replace all NP, 2 for Keep one NP ..  .   
                
                if SentInfo(isent).Probe.LexChangeCat==2
                    VerbLexChange=1; % matter for determining VerbElipsis below...    
                end
                
                if curType==2
                    ChooseNPToRepBySentType
                end
        end                       
    end    
end

SentInfo(isent).Probe.VerbEllipsis=2;  % default of no ellipsis    
if ~VerbLexChange && ~(SentInfo(isent).Probe.SameOrDiff==2 && SentInfo(isent).Probe.Diff_GrammOrLexChange==1 && SentInfo(isent).Probe.GrammSwitchType==3)   && curSentType >= 4
    curType=ChooseFromCounts( Counts.Probe.VerbEllipses, VerbEllipsisRate );
    Counts.Probe.VerbEllipses( curType )= Counts.Probe.VerbEllipses( curType )+1;   % 1 for Verb Ellipsis, 2 for no Verb Ellipsis...
    SentInfo(isent).Probe.VerbEllipsis=curType;    
end

%SentInfo(isent).Probe.VerbEllipsis=1;


SentInfo(isent).Probe.ElideAdv=ProbeElideAdv;

