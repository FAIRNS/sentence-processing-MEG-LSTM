% ProcessStaySwitch.m
%
% Here the procedure is to forget the word count, and enforce a 50/50 Stay/Switch strategy    

if strcmp(s.node{inode},'_N_P0')         
    if AlreadyPresent.NAnim && strcmp(KeepLab,'$ANIMATE') || AlreadyPresent.NInAnim && strcmp(KeepLab,'$INANIMATE')
        % ignore word counts and wts and choose here among all 4 options evenly. If a repeat is detected, we'll swap it for the most closely related word at the end of GenerateSentence       
        MatchedrInds= MatchedrInds( randi( length(MatchedrInds) ) );    % MatchedrInds will only be 1 element, so the weights later on don't matter    
    elseif strcmp(KeepLab,'$ANIMATE')
        AlreadyPresent.NAnim=1;
    elseif strcmp(KeepLab,'$INANIMATE') 
        AlreadyPresent.NInAnim=1;
    end
elseif strcmp(s.node{inode},'_A_P0')
    if AlreadyPresent.AdjAnimEmot && strcmp(KeepLab,'$EMOTION') || AlreadyPresent.AdjPhys && strcmp(KeepLab,'$PHYSICAL')
        % ignore word counts and wts and choose here among all 4 options evenly. If a repeat is detected, we'll swap it for the most closely related word at teh end of GenerateSentence       
        MatchedrInds= MatchedrInds( randi( length(MatchedrInds) ) );    % MatchedrInds will only be 1 element, so teh weights later on don't matter    
    elseif strcmp(KeepLab,'$EMOTION')
        AlreadyPresent.AdjAnimEmot=1;
    elseif strcmp(KeepLab,'$PHYSICAL') 
        AlreadyPresent.AdjPhys=1;
    end
elseif strcmp(s.node{inode},'_NUM')
    if AlreadyPresent.Num
        MatchedrInds= MatchedrInds( randi( length(MatchedrInds) ) ); 
    else
        AlreadyPresent.Num=1;
    end
end
    