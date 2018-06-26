% AdjSentTypeRuleWts

switch curSentType
    case 1  % Trans, PP Loc 1        
        OnLabs={'PPLoc1_On','PPLoc2_Off','Trans_On'};
        OffLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
    case 1  % Trans, PP Loc 2
        OnLabs={'PPLoc1_Off','PPLoc2_On','Trans_On'};
        OffLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
    case 1  % Trans, NO PP at all bc it's ambiguous if we put the PP at the end    
        OnLabs={'PPLoc1_Off','PPLoc2_Off','Trans_On'};
        OffLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off','InTrans_PPLoc3_On'};
    case 1  % InTrans, PP Loc 1
        OnLabs={'PPLoc1_On','PPLoc2_Off','InTrans_PPLoc3_Off'};
        OffLabs={'PPLoc1_Off','PPLoc2_On','Trans_On','InTrans_PPLoc3_On'};
    case 1  % InTrans, PP Loc 2
        OnLabs={'PPLoc1_Off','PPLoc2_On','InTrans_PPLoc3_Off'};
        OffLabs={'PPLoc1_On','PPLoc2_Off','Trans_On','InTrans_PPLoc3_On'};
    case 1  % InTrans, PP Loc 3   
        OnLabs={'PPLoc1_Off','PPLoc2_Off','InTrans_PPLoc3_On'};
        OffLabs={'PPLoc1_On','PPLoc2_On','Trans_On','InTrans_PPLoc3_Off'};
end

nrules = length(r);
for irule=1:nrules
    if isfield(r{irule},'lab')
        if ismember(r{irule}.lab,OnLabs)
            r{irule}.wt=10;
        elseif ismember(r{irule}.lab,OffLabs)
            r{irule}.wt=0;
        end
    end    
end