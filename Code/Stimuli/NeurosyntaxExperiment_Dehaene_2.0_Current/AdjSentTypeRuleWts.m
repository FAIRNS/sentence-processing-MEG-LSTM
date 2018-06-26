% AdjSentTypeRuleWts

switch curSentType
    case 1  % Trans, PP Loc 1
        if TurnOffPPs
            OnLabs={'PPLoc1_Off','PPLoc2_Off','Trans_On'};
            OffLabs={'PPLoc1_On','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
        else
            OnLabs={'PPLoc1_On','PPLoc2_Off','Trans_On'};
            OffLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
        end
    case 2  % Trans, PP Loc 2
        if TurnOffPPs
            OnLabs={'PPLoc1_Off','PPLoc2_Off','Trans_On'};
            OffLabs={'PPLoc1_On','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
        else
            OnLabs={'PPLoc1_Off','PPLoc2_On','Trans_On'};
            OffLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
        end
    case 3  % Trans, NO PP at all bc it's ambiguous if we put the PP at the end
        OnLabs={'PPLoc1_Off','PPLoc2_Off','Trans_On'};
        OffLabs={'PPLoc1_On','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
    case 4  % InTrans, PP Loc 1
        if TurnOffPPs
            OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_Off'};
            OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
        else
            OnLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off'};
            OffLabs={'PPLoc1_Off','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
        end
    case 5  % InTrans, PP Loc 2
        if TurnOffPPs
            OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_Off'};
            OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
        else
            OnLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off'};
            OffLabs={'PPLoc1_On','PPLoc2_Off','Trans_On','InTrans_PPLoc3_On'};
        end
    case 6  % InTrans, PP Loc 3
        if TurnOffPPs
            OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_Off'};
            OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
        else
            OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_On'};
            OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_Off'};
        end
end


rwtlist( ismember(rlablist,OnLabs) )=10;
rwtlist( ismember(rlablist,OffLabs) )=0;
