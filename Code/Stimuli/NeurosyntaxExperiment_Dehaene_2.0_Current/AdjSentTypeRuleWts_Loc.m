% AdjSentTypeRuleWts_Loc

SentInfo(isent).NPInc=[1 0 0];
% determine PP loctaion if it exists   
if SentInfo(isent).nToAdd(1)
    SentInfo(isent).NPInc(3)=1;
    if SentInfo(isent).nToAdd(2)
        % it's Trans... can't have PPLoc 3   
        PPLoc=ChooseFromCounts( Loc.Counts.PPLoc(1:2) );        
    else
        PPLoc=ChooseFromCounts( Loc.Counts.PPLoc );
    end
    Loc.Counts.PPLoc(PPLoc)=Loc.Counts.PPLoc(PPLoc)+1;                
end

% go through each possible combination of PPLoc and Trans/InTrans  
if SentInfo(isent).nToAdd(2)
    SentInfo(isent).NPInc(2)=1;
    % Trans   
    if SentInfo(isent).nToAdd(1)
        % PP   
        switch PPLoc
            case 1
                OnLabs={'PPLoc1_On','PPLoc2_Off','Trans_On'};
                OffLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
            case 2
                OnLabs={'PPLoc1_Off','PPLoc2_On','Trans_On'};
                OffLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
        end
    else
        % No PP
        OnLabs={'PPLoc1_Off','PPLoc2_Off','Trans_On'};
        OffLabs={'PPLoc1_On','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
    end
else
    % InTrans
    if SentInfo(isent).nToAdd(1)
        % PP   
        switch PPLoc
            case 1
                OnLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off'};
                OffLabs={'PPLoc1_Off','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
            case 2
                OnLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off'};
                OffLabs={'PPLoc1_On','PPLoc2_Off','Trans_On','InTrans_PPLoc3_On'};
            case 3                
                OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_On'};
                OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_Off'};
        end
    else
        % No PP
        OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_Off'};
        OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
    end
end       


rwtlist( ismember(rlablist,OnLabs) )=10;
rwtlist( ismember(rlablist,OffLabs) )=0;
